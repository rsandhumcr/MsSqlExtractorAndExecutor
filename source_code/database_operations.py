from __future__ import annotations

import logging
import struct
from dataclasses import dataclass
from typing import Any, TypeAlias

from azure.identity import AzureCliCredential
from sqlalchemy import MetaData, Table, create_engine, text
from sqlalchemy.engine import Connection, Engine, URL
from sqlalchemy.sql.type_api import TypeEngine


logger = logging.getLogger(__name__)


# Microsoft ODBC constant for an access token.
SQL_COPT_SS_ACCESS_TOKEN = 1256

DatabaseConfigType: TypeAlias = dict[str, str | URL]
DatabaseConnectionString: TypeAlias = str | URL


@dataclass
class ResultSet:
    """A SQL result set."""

    data: list[Any]
    columns: list[TableColumn]
    types: list[str]


@dataclass
class TableColumn:
    """Metadata describing a database table column."""

    name: str
    type: TypeEngine
    autoincrement: bool | str
    foreign_keys: set[Any]
    primary_key: bool


class DatabaseOperations:
    """Database access and metadata operations."""

    def __init__(
        self,
        master_database: str = "master",
        enable_logging: bool = False,
    ) -> None:
        self.master_database = master_database
        self.enable_logging = enable_logging

        self._engines: dict[str, Engine] = {}

        if enable_logging:
            self._configure_logging()

    # ------------------------------------------------------------------
    # Engine / connection handling
    # ------------------------------------------------------------------

    def _configure_logging(self) -> None:
        """Configure SQLAlchemy logging."""

        logging.getLogger("sqlalchemy.engine").setLevel(
            logging.INFO
        )

    def _get_engine(
        self,
        database_config: DatabaseConfigType,
    ) -> Engine:
        """
        Get or create an SQLAlchemy engine for a database configuration.

        Engines are cached because creating an Engine for every query is
        unnecessary and prevents SQLAlchemy from efficiently managing
        its connection pool.
        """

        connection_string = str(
            database_config["connection_str"]
        )

        if connection_string in self._engines:
            return self._engines[connection_string]

        engine = self._create_engine(database_config)

        self._engines[connection_string] = engine

        return engine

    def _create_engine(
        self,
        database_config: DatabaseConfigType,
    ) -> Engine:
        """Create an SQLAlchemy engine."""

        connection_string = database_config["connection_str"]

        if database_config.get(
            "use_azure_identity_entra",
            False,
        ):
            access_token = self.get_azure_cli_auth_token()

            return create_engine(
                connection_string,
                connect_args={
                    "attrs_before": {
                        SQL_COPT_SS_ACCESS_TOKEN: access_token
                    }
                },
            )

        return create_engine(
            connection_string,
            echo=self.enable_logging,
        )

    def get_connection_object(
        self,
        database_config: DatabaseConfigType,
    ) -> Connection:
        """
        Return an SQLAlchemy connection.

        Prefer using the connection as a context manager in new code.
        """

        engine = self._get_engine(database_config)

        return engine.connect()

    def close(self) -> None:
        """Dispose of all cached database engines."""

        for engine in self._engines.values():
            engine.dispose()

        self._engines.clear()

    # ------------------------------------------------------------------
    # Azure authentication
    # ------------------------------------------------------------------

    @staticmethod
    def get_azure_cli_auth_token() -> bytes:
        """
        Get an Azure SQL access token from Azure CLI credentials.

        The SQL Server ODBC driver expects the token in a specific
        UTF-16LE-like structure prefixed by its byte length.
        """

        credential = AzureCliCredential()

        access_token = credential.get_token(
            "https://database.windows.net/"
        )

        token_bytes = access_token.token.encode("utf-16-le")

        return struct.pack(
            "=i",
            len(token_bytes),
        ) + token_bytes

    # ------------------------------------------------------------------
    # Database discovery
    # ------------------------------------------------------------------

    def get_database(
        self,
        database_config: DatabaseConfigType,
    ) -> list[str]:
        """Return available database names."""

        query = text(
            """
            SELECT name
            FROM sys.databases
            ORDER BY name
            """
        )

        result = self._execute_query(
            database_config,
            query,
        )

        return [
            row[0]
            for row in result.data
        ]

    # ------------------------------------------------------------------
    # Table discovery
    # ------------------------------------------------------------------

    def search_table_name(
        self,
        database_config: DatabaseConfigType,
        table_name_search: str,
    ) -> list[str]:
        """Search for tables matching a name."""

        query = text(
            """
            SELECT
                '[' + TABLE_SCHEMA + '].[' + TABLE_NAME + ']'
                    AS table_name
            FROM INFORMATION_SCHEMA.TABLES
            WHERE TABLE_TYPE = 'BASE TABLE'
              AND TABLE_NAME LIKE :search_term
            ORDER BY TABLE_SCHEMA, TABLE_NAME
            """
        )

        result = self._execute_query(
            database_config,
            query,
            {
                "search_term": f"%{table_name_search}%"
            },
        )

        return [
            row[0]
            for row in result.data
        ]

    # ------------------------------------------------------------------
    # Table data
    # ------------------------------------------------------------------

    def get_table_data(
        self,
        database_config: DatabaseConfigType,
        table_name: str,
        where_clause: str = "",
    ) -> dict[str, Any]:
        """Return table data and column metadata."""

        table_data = self.get_table_query_data(
            database_config,
            table_name,
            where_clause,
        )

        table_metadata = (
            self.get_table_meta_data_simple_string(
                database_config,
                table_name,
            )
        )

        return {
            "query": table_data["query"],
            "data": table_data["data"],
            "columns": table_metadata,
        }

    def get_table_query_data(
        self,
        database_config: DatabaseConfigType,
        table_name: str,
        where_clause: str = "",
    ) -> dict[str, Any]:
        """
        Execute SELECT * against a table.

        Note:
            table_name and where_clause are SQL fragments rather than
            normal SQL parameters. They should only come from trusted
            or validated input.
        """

        query = f"SELECT * FROM {table_name}"

        if where_clause:
            query += f" WHERE {where_clause}"

        result = self._execute_query(
            database_config,
            text(query),
        )

        return {
            "query": query,
            "data": result.data,
        }

    # ------------------------------------------------------------------
    # Table metadata
    # ------------------------------------------------------------------

    def get_table_meta_data(
        self,
        database_config: DatabaseConfigType,
        schema_name: str,
        table_name: str,
    ) -> list[TableColumn]:
        """Return SQLAlchemy metadata for a table."""

        engine = self._get_engine(database_config)

        metadata = MetaData()

        with engine.connect() as connection:
            table = Table(
                table_name,
                metadata,
                schema=schema_name,
                autoload_with=connection,
            )

            columns: list[TableColumn] = []

            for column in table.columns:
                columns.append(
                    TableColumn(
                        name=column.name,
                        type=column.type,
                        autoincrement=column.autoincrement,
                        foreign_keys=set(column.foreign_keys),
                        primary_key=column.primary_key,
                    )
                )

        return columns

    def get_table_meta_data_simple_string(
        self,
        database_config: DatabaseConfigType,
        table_name: str,
    ) -> list[TableColumn]:
        """Get table metadata from a schema.table string."""

        schema_name, table_name = (
            self.extract_schema_table_name(
                table_name
            )
        )

        return self.get_table_meta_data(
            database_config,
            schema_name,
            table_name,
        )

    @staticmethod
    def extract_schema_table_name(
        database_table: str,
    ) -> tuple[str, str]:
        """
        Extract schema and table names.

        Examples:
            Sales.Customer -> ("Sales", "Customer")
            [Sales].[Customer] -> ("Sales", "Customer")
            Customer -> ("dbo", "Customer")
        """

        parts = [
            part.strip()
            .strip("[]")
            for part in database_table.split(".")
        ]

        if len(parts) == 1:
            return "dbo", parts[0]

        if len(parts) == 2:
            return parts[0], parts[1]

        raise ValueError(
            f"Invalid table name: {database_table}"
        )

    @staticmethod
    def get_primary_columns(
        table_data: dict[str, Any],
    ) -> list[TableColumn]:
        """Return the primary-key columns from table metadata."""

        return [
            column
            for column in table_data["columns"]
            if column.primary_key
        ]

    # ------------------------------------------------------------------
    # SQL execution
    # ------------------------------------------------------------------

    def execute_sql_script_no_data(
        self,
        database_config: DatabaseConfigType,
        sql_script: str,
    ) -> None:
        """Execute a SQL script without returning results."""

        engine = self._get_engine(database_config)

        with engine.begin() as connection:
            connection.execute(
                text(sql_script)
            )

    def execute_sql_script(
        self,
        database_config: DatabaseConfigType,
        sql_script: str,
        parameters: dict[str, Any] | None = None,
    ) -> ResultSet:
        """Execute SQL and return its result set."""

        return self._execute_query(
            database_config,
            text(sql_script),
            parameters,
        )

    def _execute_query(
        self,
        database_config: DatabaseConfigType,
        query: Any,
        parameters: dict[str, Any] | None = None,
    ) -> ResultSet:
        """Execute a query and return a ResultSet."""

        engine = self._get_engine(database_config)

        with engine.connect() as connection:
            result = connection.execute(
                query,
                parameters or {},
            )

            columns = list(
                result.keys()
            )

            data = result.fetchall()

        return ResultSet(
            data=data,
            columns=columns,
            types=[
                type(value).__name__
                for value in data[0]
            ] if data else [],
        )

    # ------------------------------------------------------------------
    # Raw DB-API execution
    # ------------------------------------------------------------------

    def execute_sql_script_raw_connection(
        self,
        database_config: DatabaseConfigType,
        sql_script: str,
    ) -> list[ResultSet]:
        """
        Execute SQL through the underlying DB-API connection.

        This is useful for SQL Server scripts returning multiple
        result sets.
        """

        engine = self._get_engine(database_config)

        result_sets: list[ResultSet] = []

        #with engine.raw_connection() as raw_connection:
        raw_connection = engine.raw_connection()
        cursor = raw_connection.cursor()

        try:
            cursor.execute(sql_script)

            while True:
                if cursor.description is not None:
                    rows = cursor.fetchall()

                    result_sets.append(
                        self.extract_result_data(
                            rows,
                            cursor.description,
                        )
                    )

                if not cursor.nextset():
                    break

            #raw_connection.commit()

        finally:
            cursor.close()

        return result_sets

    @staticmethod
    def extract_result_data(
        result_set: Any,
        description: Any,
    ) -> ResultSet:
        """Convert DB-API result data into a ResultSet."""

        columns = [
            column[0]
            for column in description
        ]

        types = [
            getattr(
                column[1],
                "__name__",
                str(column[1]),
            )
            for column in description
        ]

        return ResultSet(
            data=list(result_set or []),
            columns=columns,
            types=types,
        )

    # ------------------------------------------------------------------
    # Cleanup
    # ------------------------------------------------------------------

    def __enter__(self) -> DatabaseOperations:
        return self

    def __exit__(
        self,
        exc_type: Any,
        exc_value: Any,
        traceback_value: Any,
    ) -> None:
        self.close()
