from __future__ import annotations

import logging
from datetime import datetime
from typing import Any

from source_code.database_operations import ResultSet, TableColumn


logger = logging.getLogger(__name__)


def get_current_timestamp() -> str:
    """Return the current timestamp in the generator's output format."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"--- {timestamp}  \r\n\r\n"


class CSharpObjectGenerator:
    """Generate C# object initialisation statements from database results."""

    _INTEGER_TYPES = (
        "INTEGER",
        "INT",
        "SMALLINT",
        "TINYINT",
    )

    _LONG_TYPES = (
        "BIGINT",
    )

    _DECIMAL_TYPES = (
        "DECIMAL",
        "FLOAT",
        "REAL",
        "MONEY",
    )

    _STRING_TYPES = (
        "TEXT",
        "NVARCHAR",
        "VARCHAR",
        "NCHAR",
        "CHAR",
    )

    _DATETIME_TYPES = (
        "DATETIME",
        "DATE",
        "TIMESTAMP",
        "TIME",
    )

    _BOOL_TYPES = (
        "BOOLEAN",
        "BIT",
    )

    def create_object_statement(
        self,
        database_name: str,
        table_name: str,
        table_data: ResultSet,
    ) -> str:
        """Generate C# object initialisation statements."""
        try:
            columns = table_data["columns"]
            rows = table_data["data"]
            query = table_data["query"]

            object_name = self.format_name(table_name)
            output: list[str] = [
                f" /// {database_name}  {query}\n"
            ]

            for row_data in rows:
                output.append(
                    self._format_row(
                        object_name,
                        row_data,
                        columns,
                    )
                )

            output.append(");  \n\n")
            output.append(get_current_timestamp())

            return "".join(output)

        except Exception:
            logger.exception(
                "Failed to create C# object statement"
            )
            raise

    def _format_row(
        self,
        object_name: str,
        row_data: list[Any],
        columns: list[TableColumn],
    ) -> str:
        """Format a single database row as a C# object."""
        properties = [
            self._format_property(row_data[index], column)
            for index, column in enumerate(columns)
        ]

        formatted_properties = self._format_properties(
            properties
        )

        return (
            f"    {object_name}.Add(new {object_name}Row {{\n"
            f"{formatted_properties}\n"
            f"    }}"
        )

    def _format_property(
        self,
        row_value: Any,
        column: TableColumn,
    ) -> str:
        """Format a single C# property assignment."""
        column_name = self.format_name(column.name)
        value = self.format_row_data_type_with_column(
            row_value,
            column,
        )

        return f"{column_name} = {value}"

    @staticmethod
    def _format_properties(
        properties: list[str],
        properties_per_line: int = 5,
    ) -> str:
        """Format properties with a configurable number per line."""
        lines: list[str] = []
        current_line: list[str] = []

        for property_text in properties:
            current_line.append(property_text)

            if len(current_line) == properties_per_line:
                lines.append("        , ".join(current_line))
                current_line = []

        if current_line:
            lines.append("        , ".join(current_line))

        return "\n".join(lines)

    def format_row_data_type_with_column(
        self,
        row_data: Any,
        column_data: TableColumn,
    ) -> str:
        """Convert a database value into a C# representation."""
        if row_data is None:
            return "null"

        type_description = str(column_data.type).upper()

        if type_description.startswith(self._BOOL_TYPES):
            return self._format_bool(row_data)

        if type_description.startswith(self._INTEGER_TYPES):
            return str(row_data)

        if type_description.startswith(self._LONG_TYPES):
            return f"{row_data}L"

        if type_description.startswith(self._DECIMAL_TYPES):
            return f"{row_data}M"

        if type_description.startswith(self._STRING_TYPES):
            return self._format_csharp_string(row_data)

        if type_description.startswith("UNIQUEIDENTIFIER"):
            return (
                f'Guid.Parse("{self._escape_string(row_data)}")'
            )

        if type_description.startswith("DATETIMEOFFSET"):
            return self._format_datetime_offset(row_data)

        if type_description.startswith(self._DATETIME_TYPES):
            return self._format_datetime(row_data)

        if type_description.startswith("VARBINARY"):
            return self._format_csharp_string(row_data)

        if type_description.startswith("XML"):
            return self._format_csharp_string(row_data)

        logger.warning(
            "Unknown database type '%s' for value '%s'",
            type_description,
            row_data,
        )

        return self._format_csharp_string(row_data)

    @staticmethod
    def _format_bool(value: Any) -> str:
        """Convert a database boolean value to C# syntax."""
        if isinstance(value, bool):
            return str(value).lower()

        return "true" if str(value).lower() == "true" else "false"

    @classmethod
    def _format_datetime(cls, value: Any) -> str:
        """Format a database datetime as C# DateTime.Parse."""
        value_text = cls._remove_fractional_seconds(value)

        return f'DateTime.Parse("{value_text}")'

    @classmethod
    def _format_datetime_offset(cls, value: Any) -> str:
        """Format a database datetime offset as C#."""
        value_text = cls._remove_fractional_seconds(value)

        return (
            "new DateTimeOffset("
            f'DateTime.Parse("{value_text}")'
            ")"
        )

    @staticmethod
    def _remove_fractional_seconds(value: Any) -> str:
        """Remove fractional seconds from a datetime value."""
        return str(value).split(".", maxsplit=1)[0]

    @classmethod
    def _format_csharp_string(cls, value: Any) -> str:
        """Escape and quote a value for use as a C# string."""
        return f'"{cls._escape_string(value)}"'

    @staticmethod
    def _escape_string(value: Any) -> str:
        """Escape quotes for a C# string literal."""
        return str(value).replace("\\", "\\\\").replace('"', '\\"')

    @staticmethod
    def format_name(name: str) -> str:
        """Remove schema/table brackets and return the final name."""
        return name.split(".")[-1].replace("[", "").replace("]", "")

    @staticmethod
    def convert_snake_to_pascal_case(input_text: str) -> str:
        """Convert snake_case text to PascalCase."""
        return "".join(
            word.capitalize()
            for word in input_text.split("_")
            if word
        )

    @classmethod
    def convert_snake_to_camel_case(cls, input_text: str) -> str:
        """Convert snake_case text to camelCase."""
        pascal_case = cls.convert_snake_to_pascal_case(input_text)

        if not pascal_case:
            return ""

        return pascal_case[0].lower() + pascal_case[1:]

    @staticmethod
    def convert_pascal_to_snake_case(input_text: str) -> str:
        """Convert PascalCase text to snake_case."""
        output: list[str] = []

        for index, letter in enumerate(input_text):
            if letter.isupper() and index > 0:
                output.append("_")

            output.append(letter.lower())

        return "".join(output)