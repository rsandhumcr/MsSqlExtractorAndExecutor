from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Final


PARAMETER_SECTION_START: Final = "--- parameters start"
PARAMETER_SECTION_END: Final = "--- parameters end"

WITH_RESULTS: Final = "--- with results"
WITH_RESULTS_COLUMNS: Final = "--- with results columns"
WITH_RESULTS_ROWS: Final = "--- with results rows"
WITH_RESULTS_CSV: Final = "--- with results csv"
WITH_RESULTS_NO_HEADERS: Final = "--- with results rows no headers"


@dataclass
class SqlParameter:
    """Represents a parameter declaration in a SQL script."""

    original_line: str
    parameter: str
    parameter_type: str
    prompt: str
    default_value: str = ""
    response: str = ""


class ParseSqlParameters:
    """
    Parse and replace interactive SQL parameters.

    Expected parameter syntax:

        --- parameters start
        DECLARE @Parameter1 INT = <value>; --- Prompt for input1 ?
        DECLARE @Parameter2 VARCHAR(100) = <value>; --- Prompt for input2 ?
        --- parameters end

    Supported result markers:

        --- with results
        --- with results columns
        --- with results rows
        --- with results csv
        --- with results rows no headers
    """

    _PARAMETER_PATTERN: Final = re.compile(
        r"""
        ^\s*
        DECLARE
        \s+
        (?P<parameter>@\w+)
        \s+
        (?P<type>[\w]+(?:\s*\([^)]*\))?)
        \s*=
        \s*
        <value>
        \s*;
        (?P<prompt>.*)
        $
        """,
        re.IGNORECASE | re.VERBOSE,
    )

    _DEFAULT_PATTERN: Final = re.compile(
        r"\[([^\]]*)\]"
    )

    def find_parameter_section_start_end(
        self,
        file_data: str,
    ) -> dict[str, int]:
        """Return the start and end positions of the parameter section."""

        return {
            "start_index": file_data.find(
                PARAMETER_SECTION_START
            ),
            "end_index": file_data.find(
                PARAMETER_SECTION_END
            ),
        }

    def has_parameter_section(
        self,
        file_data: str,
    ) -> bool:
        """Return whether a complete parameter section exists."""

        indexes = self.find_parameter_section_start_end(file_data)

        start_index = indexes["start_index"]
        end_index = indexes["end_index"]

        return (
            start_index >= 0
            and end_index >= 0
            and start_index < end_index
        )

    def extract_parameters_section(
        self,
        file_data: str,
    ) -> list[str]:
        """Extract individual lines from the parameter section."""

        indexes = self.find_parameter_section_start_end(file_data)

        start_index = indexes["start_index"]
        end_index = indexes["end_index"]

        if (
            start_index < 0
            or end_index < 0
            or start_index >= end_index
        ):
            return []

        section_start = (
            start_index + len(PARAMETER_SECTION_START)
        )

        section = file_data[section_start:end_index]

        return [
            line.strip()
            for line in section.splitlines()
            if line.strip()
        ]

    @classmethod
    def find_parameter_default(
        cls,
        parameter_data: str,
    ) -> str:
        """Extract an optional default value from [value]."""

        match = cls._DEFAULT_PATTERN.search(parameter_data)

        if match is None:
            return ""

        return match.group(1)

    @classmethod
    def extract_parameters(
        cls,
        parameter_line: str,
    ) -> SqlParameter:
        """Parse a parameter declaration."""

        match = cls._PARAMETER_PATTERN.match(parameter_line)

        if match is None:
            raise ValueError(
                f"Invalid SQL parameter declaration: "
                f"{parameter_line!r}"
            )

        prompt = match.group("prompt").strip()
        default_value = cls.find_parameter_default(
            parameter_line
        )

        return SqlParameter(
            original_line=parameter_line,
            parameter=match.group("parameter"),
            parameter_type=match.group("type"),
            prompt=prompt,
            default_value=default_value,
        )

    @staticmethod
    def prompt_user(
        parameters: list[SqlParameter],
    ) -> None:
        """Prompt the user for each SQL parameter value."""

        print(
            "You can enter the string NULL (uppercase) "
            "for a NULL value."
        )

        for parameter in parameters:
            prompt = ParseSqlParameters._build_prompt(
                parameter
            )

            response = input(prompt).strip()

            parameter.response = (
                parameter.original_line.replace(
                    "<value>",
                    ParseSqlParameters._format_response(
                        response,
                        parameter.default_value,
                    ),
                    1,
                )
            )

    @staticmethod
    def _build_prompt(
        parameter: SqlParameter,
    ) -> str:
        """Build the text displayed to the user."""

        if parameter.prompt:
            prompt = parameter.prompt.replace(
                "?",
                f"({parameter.parameter_type}) ?",
                1,
            )
        else:
            prompt = (
                f"Enter value for "
                f"{parameter.parameter} "
                f"({parameter.parameter_type}) ?"
            )

        return prompt.lstrip("- ").strip() + " "

    @staticmethod
    def _format_response(
        response: str,
        default_value: str,
    ) -> str:
        """Convert user input into a SQL value."""

        if not response:
            if default_value:
                response = default_value
            else:
                return "NULL"

        if response.upper() == "NULL":
            return "NULL"

        if ParseSqlParameters._is_numeric(response):
            return response

        return ParseSqlParameters._quote_sql_string(response)

    @staticmethod
    def _is_numeric(value: str) -> bool:
        """Return whether a value is a valid integer/decimal."""

        try:
            float(value)
        except ValueError:
            return False

        return True

    @staticmethod
    def _quote_sql_string(value: str) -> str:
        """Quote and escape a SQL string literal."""

        escaped = value.replace("'", "''")

        return f"'{escaped}'"

    @staticmethod
    def replace_parameter_values(
        parameters: list[SqlParameter],
        sql_script: str,
    ) -> str:
        """Replace parameter declarations with user values."""

        for parameter in parameters:
            sql_script = sql_script.replace(
                parameter.original_line,
                parameter.response,
                1,
            )

        return sql_script

    def replace_parameters_with_prompts(
        self,
        sql_script_input: str,
    ) -> dict[str, str | bool | None]:
        """Prompt for parameters and determine script options."""

        parameters: list[SqlParameter] = []

        if self.has_parameter_section(sql_script_input):
            parameter_lines = self.extract_parameters_section(
                sql_script_input
            )

            parameters = [
                self.extract_parameters(line)
                for line in parameter_lines
            ]

            self.prompt_user(parameters)

        adjusted_sql = self.replace_parameter_values(
            parameters,
            sql_script_input,
        )

        result_type = self._get_result_type(
            sql_script_input
        )

        parameter_values = "".join(
            f"{parameter.response}\n"
            for parameter in parameters
        )

        return {
            "sql_script": adjusted_sql,
            "return_results": self.check_for_return_results_marker(
                sql_script_input
            ),
            "result_in_columns": result_type,
            "no_headers": self.check_for_columns_no_headers_marker(
                sql_script_input
            ),
            "parameter_values": parameter_values,
        }

    @staticmethod
    def _get_result_type(
        sql_script: str,
    ) -> str | None:
        """Determine how query results should be displayed."""

        if WITH_RESULTS_CSV in sql_script:
            return "CSV"

        if WITH_RESULTS_ROWS in sql_script:
            return "Rows"

        if WITH_RESULTS_COLUMNS in sql_script:
            return "Columns"

        return None

    @staticmethod
    def check_for_return_results_marker(
        sql_script_input: str,
    ) -> bool:
        """Check whether the script requests query results."""

        return ParseSqlParameters.search_script_for_text(
            sql_script_input,
            WITH_RESULTS,
        )

    @staticmethod
    def check_for_columns_results_marker(
        sql_script_input: str,
    ) -> bool:
        """Check whether results should be displayed as columns."""

        return ParseSqlParameters.search_script_for_text(
            sql_script_input,
            WITH_RESULTS_COLUMNS,
        )

    @staticmethod
    def check_for_rows_results_marker(
        sql_script_input: str,
    ) -> bool:
        """Check whether results should be displayed as rows."""

        return ParseSqlParameters.search_script_for_text(
            sql_script_input,
            WITH_RESULTS_ROWS,
        )

    @staticmethod
    def check_for_csv_results_marker(
        sql_script_input: str,
    ) -> bool:
        """Check whether results should be exported as CSV."""

        return ParseSqlParameters.search_script_for_text(
            sql_script_input,
            WITH_RESULTS_CSV,
        )

    @staticmethod
    def check_for_columns_no_headers_marker(
        sql_script_input: str,
    ) -> bool:
        """Check whether column headers should be omitted."""

        return ParseSqlParameters.search_script_for_text(
            sql_script_input,
            WITH_RESULTS_NO_HEADERS,
        )

    @staticmethod
    def search_script_for_text(
        sql_script_input: str,
        search_text: str,
    ) -> bool:
        """Return whether the specified marker exists."""

        return search_text in sql_script_input

    @staticmethod
    def read_file(path_file: str) -> str:
        """Read a SQL script from disk."""

        return Path(path_file).read_text(
            encoding="utf-8"
        )