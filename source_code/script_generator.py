from __future__ import annotations

import logging
from collections.abc import Sequence
from datetime import datetime
from typing import Any

from tqdm import tqdm

from source_code.database_operations import ResultSet, TableColumn


logger = logging.getLogger(__name__)


def get_current_timestamp() -> str:
    """Return the current timestamp used by generated scripts."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"--- {timestamp}\r\n\r\n"


class ScriptGenerator:
    """Generate INSERT and UPDATE SQL scripts from query results."""

    _VALUES_PER_LINE = 5
    _ROWS_PER_INSERT = 100

    _BOOLEAN_TYPES = (
        "BOOLEAN",
        "BIT",
    )

    _STRING_TYPES = (
        "UNIQUEIDENTIFIER",
        "TEXT",
        "NVARCHAR",
        "VARCHAR",
        "NCHAR",
        "CHAR",
    )

    _DATETIME_TYPES = (
        "DATETIMEOFFSET",
        "DATETIME",
        "DATE",
        "TIMESTAMP",
        "TIME",
    )

    _NUMERIC_TYPES = (
        "INTEGER",
        "DECIMAL",
        "BIGINT",
        "FLOAT",
        "INT",
        "NUMERIC",
        "REAL",
        "SMALLINT",
        "TINYINT",
        "MONEY",
    )

    def create_insert_statement(
        self,
        database_name: str,
        table_name: str,
        table_data: ResultSet,
        add_record: bool,
    ) -> str:
        """Generate an INSERT statement for the supplied rows."""

        columns = table_data["columns"]
        rows = table_data["data"]
        query = table_data["query"]

        auto_columns = self.get_table_columns_are_autoincrement(
            table_data
        )

        include_identity = (
            not add_record
            and bool(auto_columns)
        )

        insert_columns = [
            column.name
            for column in columns
            if not (add_record and column.name in auto_columns)
        ]

        output: list[str] = [
            f"---   {query}\n",
        ]

        if not add_record:
            output.extend(
                [
                    f"IF NOT EXISTS ({query})\n",
                    "BEGIN\n",
                ]
            )

        if include_identity:
            output.append(
                f"    SET IDENTITY_INSERT {table_name} ON;\n"
            )

        output.extend(
            self._build_insert_batches(
                table_name=table_name,
                columns=insert_columns,
                rows=rows,
                table_columns=columns,
                auto_columns=auto_columns,
                skip_auto_columns=add_record,
            )
        )

        if include_identity:
            output.append(
                f"    SET IDENTITY_INSERT {table_name} OFF;\n"
            )

        if not add_record:
            output.append("END\n\n")

        output.append(get_current_timestamp())

        return "".join(output)

    def _build_insert_batches(
        self,
        table_name: str,
        columns: list[str],
        rows: Sequence[Sequence[Any]],
        table_columns: Sequence[TableColumn],
        auto_columns: list[str],
        skip_auto_columns: bool,
    ) -> list[str]:
        """Build INSERT statements in batches."""

        output: list[str] = []

        for start in range(
            0,
            len(rows),
            self._ROWS_PER_INSERT,
        ):
            batch = rows[
                start:start + self._ROWS_PER_INSERT
            ]

            output.append(
                self._build_insert_header(
                    table_name,
                    columns,
                )
            )

            values = [
                self._format_insert_row(
                    row=row,
                    table_columns=table_columns,
                    auto_columns=auto_columns,
                    skip_auto_columns=skip_auto_columns,
                )
                for row in tqdm(batch)
            ]

            output.append(
                ",\n".join(values)
            )

            output.append(";\n\n")

        return output

    def _build_insert_header(
        self,
        table_name: str,
        columns: Sequence[str],
    ) -> str:
        """Build the INSERT INTO section."""

        formatted_columns = self._format_columns(
            columns
        )

        return (
            f"    INSERT INTO {table_name} (\n"
            f"{formatted_columns}\n"
            f"    )\n"
            f"    VALUES\n"
        )

    def _format_insert_row(
        self,
        row: Sequence[Any],
        table_columns: Sequence[TableColumn],
        auto_columns: Sequence[str],
        skip_auto_columns: bool,
    ) -> str:
        """Format one SQL VALUES row."""

        values: list[str] = []

        for column, value in zip(
            table_columns,
            row,
            strict=True,
        ):
            if (
                skip_auto_columns
                and column.name in auto_columns
            ):
                continue

            values.append(
                self.format_row_data_type_with_column(
                    value,
                    column,
                )
            )

        formatted_values = self._format_values(
            values
        )

        return f"    ({formatted_values})"

    def create_update_statement(
        self,
        database_name: str,
        table_name: str,
        table_data: ResultSet,
        primary_columns: Sequence[TableColumn],
    ) -> str:
        """Generate UPDATE statements for the supplied rows."""

        primary_indexes = self.find_column_primary_indexes(
            primary_columns,
            table_data,
        )

        query = table_data["query"]

        output: list[str] = [
            f"---   {query}\n",
            f"IF EXISTS ({query})\n",
            "BEGIN\n\n",
        ]

        for row_data in tqdm(table_data["data"]):
            set_values = [
                self._format_assignment(
                    column,
                    row_data[index],
                )
                for index, column in enumerate(
                    table_data["columns"]
                )
                if index not in primary_indexes
            ]

            where_values = [
                self._format_assignment(
                    column,
                    row_data[index],
                )
                for index, column in enumerate(
                    table_data["columns"]
                )
                if index in primary_indexes
            ]

            output.extend(
                [
                    f"    UPDATE {table_name}\n",
                    "    SET\n     ",
                    self._format_conditions(
                        set_values,
                        separator=",",
                    ),
                    "\n",
                    "    WHERE\n     ",
                    self._format_conditions(
                        where_values,
                        separator=" AND",
                    ),
                    ";\n\n",
                ]
            )

        output.extend(
            [
                "END\n\n",
                get_current_timestamp(),
            ]
        )

        return "".join(output)

    def create_insert_pk_statement(
        self,
        database_name: str,
        table_name: str,
        table_data: ResultSet,
        primary_columns: Sequence[TableColumn],
    ) -> str:
        """Generate INSERT statements guarded by primary-key checks."""

        primary_indexes = self.find_column_primary_indexes(
            primary_columns,
            table_data,
        )

        columns = table_data["columns"]

        output: list[str] = [
            f"---   {table_data['query']}\n",
        ]

        for row_index, row_data in enumerate(
            tqdm(table_data["data"])
        ):
            where_values = [
                self._format_assignment(
                    columns[index],
                    row_data[index],
                )
                for index in primary_indexes
            ]

            output.extend(
                [
                    f"IF NOT EXISTS (\n",
                    f"    SELECT 1\n",
                    f"    FROM {table_name}\n",
                    f"    WHERE\n",
                    self._format_conditions(
                        where_values,
                        separator=" AND",
                    ),
                    "\n",
                    ")\n",
                    "BEGIN\n",
                    f"    SET IDENTITY_INSERT "
                    f"{table_name} ON;\n",
                    self._build_insert_header(
                        table_name,
                        [
                            column.name
                            for column in columns
                        ],
                    ),
                    self._format_insert_row(
                        row=row_data,
                        table_columns=columns,
                        auto_columns=[],
                        skip_auto_columns=False,
                    ),
                    ";\n",
                    f"    SET IDENTITY_INSERT "
                    f"{table_name} OFF;\n",
                    "END\n",
                    f"---- Row {row_index}\n\n",
                ]
            )

        output.append(get_current_timestamp())

        return "".join(output)

    def find_column_primary_indexes(
        self,
        primary_columns: Sequence[TableColumn],
        table_data: ResultSet,
    ) -> list[int]:
        """Return indexes of primary-key columns."""

        primary_names = {
            column.name
            for column in primary_columns
        }

        return [
            index
            for index, column in enumerate(
                table_data["columns"]
            )
            if column.name in primary_names
        ]

    @staticmethod
    def has_table_columns_have_autoincrement(
        table_data: ResultSet,
    ) -> bool:
        """Return whether the table contains an auto-increment column."""

        return any(
            column.autoincrement
            for column in table_data["columns"]
        )

    @staticmethod
    def get_table_columns_are_autoincrement(
        table_data: ResultSet,
    ) -> list[str]:
        """Return names of auto-increment columns."""

        return [
            column.name
            for column in table_data["columns"]
            if column.autoincrement
        ]

    def format_row_data_type_with_column(
        self,
        row_data: Any,
        column_data: TableColumn,
    ) -> str:
        """Convert a database value into a SQL literal."""

        if row_data is None:
            return "NULL"

        type_description = str(
            column_data.type
        ).upper()

        if type_description.startswith(
            self._BOOLEAN_TYPES
        ):
            return self._format_boolean(row_data)

        if type_description.startswith(
            self._NUMERIC_TYPES
        ):
            return str(row_data)

        if type_description.startswith(
            self._STRING_TYPES
        ):
            return self._format_sql_string(row_data)

        if type_description.startswith(
            self._DATETIME_TYPES
        ):
            return self._format_datetime(row_data)

        if type_description.startswith("VARBINARY"):
            return self._format_varbinary(row_data)

        if type_description.startswith("XML"):
            return self._format_xml(row_data)

        logger.warning(
            "Unknown database type '%s' for value '%s'",
            type_description,
            row_data,
        )

        return self._format_sql_string(row_data)

    @staticmethod
    def _format_boolean(value: Any) -> str:
        """Convert a database boolean to SQL 0/1."""

        if isinstance(value, bool):
            return "1" if value else "0"

        return (
            "1"
            if str(value).strip().lower() == "true"
            else "0"
        )

    @staticmethod
    def _format_sql_string(value: Any) -> str:
        """Escape and quote a SQL string."""

        escaped = str(value).replace("'", "''")

        return f"'{escaped}'"

    @staticmethod
    def _format_datetime(value: Any) -> str:
        """Format a datetime value as a SQL literal."""

        value_text = str(value).split(
            ".",
            maxsplit=1,
        )[0]

        escaped = value_text.replace(
            "'",
            "''",
        )

        return f"'{escaped}'"

    @staticmethod
    def _format_varbinary(value: Any) -> str:
        """Format a VARBINARY value."""

        escaped = str(value).replace("'", "''")

        return (
            f"CONVERT(varbinary, '{escaped}')"
        )

    @staticmethod
    def _format_xml(value: Any) -> str:
        """Format an XML value."""

        escaped = str(value).replace("'", "''")

        return f"CONVERT(XML, '{escaped}')"

    @staticmethod
    def _format_columns(
        columns: Sequence[str],
    ) -> str:
        """Format column names for an INSERT statement."""
        output ="      "
        for index, column in enumerate(columns):
            if index > 0 and index % ScriptGenerator._VALUES_PER_LINE == 0:
                output += '\n      '
            output += f"{column}, "
        return output

    @staticmethod
    def _format_values(
        values: Sequence[str],
    ) -> str:
        """Format values into groups of five per line."""

        lines: list[str] = []

        for start in range(
            0,
            len(values),
            ScriptGenerator._VALUES_PER_LINE,
        ):
            lines.append(
                "        "
                + " ,".join(
                    values[
                        start:start
                        + ScriptGenerator._VALUES_PER_LINE
                    ]
                )
            )

        return "\n".join(lines)

    def _format_assignment(
        self,
        column: TableColumn,
        value: Any,
    ) -> str:
        """Format a column = value expression."""

        return (
            f"[{column.name}] = "
            f"{self.format_row_data_type_with_column(value, column)}"
        )

    @staticmethod
    def _format_conditions(
        conditions: Sequence[str],
        separator: str,
    ) -> str:
        """Format SQL SET/WHERE conditions."""

        return (
            f" {separator}\n     ".join(
                conditions
            )
        )

    @staticmethod
    def time_stamp_message(message: str) -> str:
        """Append a timestamp to a message."""

        timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        return f"{message} - {timestamp}"