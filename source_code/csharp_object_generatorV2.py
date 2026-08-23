from __future__ import annotations

import logging
from datetime import datetime
from typing import Any

from source_code.database_operations import ResultSet, TableColumn


logger = logging.getLogger(__name__)


def get_current_timestamp() -> str:
    """Return the current timestamp in the generated output."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"--- {timestamp}  \r\n\r\n"


class CSharpObjectGeneratorV2:
    """Generate C# object initialisation code from database results."""

    _INTEGER_TYPES = (
        "INTEGER",
        "INT",
        "NUMERIC",
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

    _BOOLEAN_TYPES = (
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

        object_name = self.convert_snake_to_pascal_case(
            self.format_name(table_name)
        )

        query = table_data["query"]
        columns = table_data["columns"]
        rows = table_data["data"]

        output: list[str] = [
            f" /// {database_name}  {query}\n",
        ]

        for row_data in rows:
            output.append(
                self._format_row(
                    object_name=object_name,
                    row_data=row_data,
                    columns=columns,
                )
            )

        output.append(get_current_timestamp())

        return "".join(output)

    def _format_row(
        self,
        object_name: str,
        row_data: list[Any],
        columns: list[TableColumn],
    ) -> str:
        """Format one database row as a C# object."""

        properties: list[str] = []

        for column, value in zip(columns, row_data, strict=True):
            property_name = self.convert_snake_to_pascal_case(
                self.format_name(column.name)
            )

            formatted_value = (
                self.format_row_data_type_with_column(
                    value,
                    column,
                )
            )

            properties.append(
                f"{property_name} = {formatted_value}"
            )

        formatted_properties = self._format_properties(
            properties
        )

        return (
            f"    {object_name}List.Add(new {object_name}\n"
            f"    {{\n"
            f"{formatted_properties}\n"
            f"    }});\n\n"
        )

    @staticmethod
    def _format_properties(
        properties: list[str],
        properties_per_line: int = 5,
    ) -> str:
        """Format C# properties across multiple lines."""

        lines: list[str] = []

        for start in range(0, len(properties), properties_per_line):
            property_group = properties[
                start:start + properties_per_line
            ]

            lines.append(
                "        "
                + ", ".join(property_group)
            )

        return "\n".join(lines)

    def format_row_data_type_with_column(
        self,
        row_data: Any,
        column_data: TableColumn,
    ) -> str:
        """Convert a database value to a C# expression."""

        if row_data is None:
            return "null"

        type_description = str(
            column_data.type
        ).upper()

        if type_description.startswith(self._BOOLEAN_TYPES):
            return self._format_boolean(row_data)

        if type_description.startswith(self._LONG_TYPES):
            return f"{row_data}L"

        if type_description.startswith(self._INTEGER_TYPES):
            return str(row_data)

        if type_description.startswith(self._DECIMAL_TYPES):
            return f"{row_data}M"

        if type_description.startswith(self._STRING_TYPES):
            return self._format_string(row_data)

        if type_description.startswith("UNIQUEIDENTIFIER"):
            return (
                "Guid.Parse("
                f'"{self._escape_string(row_data)}"'
                ")"
            )

        if type_description.startswith("DATETIMEOFFSET"):
            return self._format_datetime_offset(row_data)

        if type_description.startswith(self._DATETIME_TYPES):
            return self._format_datetime(row_data)

        if type_description.startswith("VARBINARY"):
            return self._format_string(row_data)

        if type_description.startswith("XML"):
            return self._format_string(row_data)

        logger.warning(
            "Unknown database type '%s' for value '%s'",
            type_description,
            row_data,
        )

        return self._format_string(row_data)

    @staticmethod
    def _format_boolean(value: Any) -> str:
        """Convert a database boolean value to C# syntax."""

        if isinstance(value, bool):
            return str(value).lower()

        return (
            "true"
            if str(value).strip().lower() == "true"
            else "false"
        )

    @classmethod
    def _format_datetime(cls, value: Any) -> str:
        """Format a value as a C# DateTime expression."""

        value_text = cls._remove_fractional_seconds(value)

        return f'DateTime.Parse("{cls._escape_string(value_text)}")'

    @classmethod
    def _format_datetime_offset(cls, value: Any) -> str:
        """Format a value as a C# DateTimeOffset expression."""

        value_text = cls._remove_fractional_seconds(value)

        return (
            "DateTimeOffset.Parse("
            f'"{cls._escape_string(value_text)}"'
            ")"
        )

    @staticmethod
    def _remove_fractional_seconds(value: Any) -> str:
        """Remove fractional seconds from a datetime value."""

        return str(value).split(".", maxsplit=1)[0]

    @classmethod
    def _format_string(cls, value: Any) -> str:
        """Format a value as an escaped C# string."""

        return f'"{cls._escape_string(value)}"'

    @staticmethod
    def _escape_string(value: Any) -> str:
        """Escape characters that have special meaning in C# strings."""

        return (
            str(value)
            .replace("\\", "\\\\")
            .replace('"', '\\"')
        )

    @staticmethod
    def format_name(name: str) -> str:
        """Remove schema prefixes and SQL identifier brackets."""

        return (
            name.split(".")[-1]
            .replace("[", "")
            .replace("]", "")
        )

    @staticmethod
    def convert_snake_to_pascal_case(input_text: str) -> str:
        """Convert snake_case to PascalCase."""

        return "".join(
            word[:1].upper() + word[1:].lower()
            for word in input_text.split("_")
            if word
        )

    @classmethod
    def convert_snake_to_camel_case(
        cls,
        input_text: str,
    ) -> str:
        """Convert snake_case to camelCase."""

        pascal_case = cls.convert_snake_to_pascal_case(
            input_text
        )

        if not pascal_case:
            return ""

        return pascal_case[0].lower() + pascal_case[1:]

    @staticmethod
    def convert_pascal_to_snake_case(
        input_text: str,
    ) -> str:
        """Convert PascalCase to snake_case."""

        output: list[str] = []

        for index, letter in enumerate(input_text):
            if letter.isupper() and index > 0:
                output.append("_")

            output.append(letter.lower())

        return "".join(output)