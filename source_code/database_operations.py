import traceback
import logging
import sqlalchemy
from sqlalchemy import text, create_engine
from sqlalchemy.sql.base import ReadOnlyColumnCollection
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.engine import Engine, URL
from sqlalchemy.sql.type_api import TypeEngine
from typing import Literal, Callable, Any


class DatabaseOperations:
    enable_logging = False

    type TableMetadata = list[dict[str | int, Literal["auto", "ignore_fk"] | str | set[ForeignKey] | TypeEngine | bool]]
    type TableMetadataItem = dict[str | int, Literal["auto", "ignore_fk"] | str | set[ForeignKey] | TypeEngine | bool]
    type TableRecords = dict[str | int, list[any] | list[dict[str, Literal["auto", "ignore_fk"] | str | set[ForeignKey] | TypeEngine | bool]]]
    type ConnectionType = URL | str

    def __init__(self, master_database='master'):
        self.master_database = master_database

    def get_connection_info(self, database_name: str = None) -> ConnectionType:

        if database_name is None:
            database_name = self.master_database

        is_connection_local = True

        if is_connection_local:
            # Local connection
            connection_string_value = f'mssql+pyodbc://./{database_name}?driver=SQL+Server+Native+Client+11.0'
            return connection_string_value

        # Remote connection
        connection_url = URL.create(
            "mssql+pyodbc",
            username="TestUser",
            password="TestPassword",
            host="127.0.0.1",
            port=1433,
            database=database_name,
            query={
                "driver": "SQL Server Native Client 11.0",
                "Encrypt": "yes",
                "TrustServerCertificate": "yes",
            },
        )
        return connection_url


    def get_connection_object(self, database_name) -> sqlalchemy.engine.Connection:
        try:
            connection_info = self.get_connection_info(database_name)
            engine: Engine = create_engine(connection_info, echo=False)
            conn: sqlalchemy.engine.Connection = engine.connect()
            return conn
        except Exception as exc:
            print(f'DatabaseOperations Method : get_connection_object')
            print('ex : ', exc)
            print(f"Method 'DatabaseOperations.get_connection_info' contains connection string settings.")
            exit()


    def get_database(self) -> list[str]:
        try:
            query = 'SELECT name FROM sys.sysdatabases ORDER BY name'
            result_set = self.execute_sql_script(None, query)
            database_names = []
            for row in result_set:
                database_names.append(row[0])
            return database_names
        except Exception as exc:
            self.handle_general_exceptions('get_database', exc)

    def search_table_name(self, database_name: str, table_name_search: str) -> list[str]:
        try:
            query = f"SELECT '[' + [TABLE_SCHEMA] + '].[' + [TABLE_NAME] + ']' NAME"
            query += f" FROM {database_name}.INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'"
            query += f"AND TABLE_NAME LIKE '%{table_name_search}%'"
            result_set = self.execute_sql_script(database_name, query)

            schema_table_names = []
            for row in result_set:
                schema_table_names.append(row[0])

            return schema_table_names
        except Exception as exc:
            self.handle_general_exceptions('search_table_name', exc)

    def get_table_data(self, database_name: str, table_name: str, where_clause: str) -> TableRecords:
        table_data = self.get_table_query_data(database_name, table_name, where_clause)
        table_meta_data = self.get_table_meta_data_simple_string(database_name, table_name)

        return {
            'query': table_data['query'],
            'data': table_data['data'],
            'columns': table_meta_data
        }

    def get_table_query_data(self, database_name: str, table_name: str, where_clause: str) -> dict[str, list[any]]:
        try:
            query: str = f"SELECT * FROM {table_name} "
            if where_clause:
                query += f"WHERE {where_clause}"

            result_set = self.execute_sql_script(database_name, query)

            table_data_rows = []
            for row in result_set:
                table_data_rows.append(row)

            return {
                'query': query,
                'data': table_data_rows,
            }
        except Exception as exc:
            self.handle_general_exceptions('get_table_data', exc)

    def get_table_meta_data(self, database_name: str, schema_name: str, table_name: str) -> TableMetadata:
        try:
            connection = self.get_connection_object(database_name)

            meta_data = sqlalchemy.MetaData()
            table_data = sqlalchemy.Table(table_name, meta_data, schema=schema_name, autoload_with=connection)

            columns = []
            columns_db: Callable[[], ReadOnlyColumnCollection[str, Column[Any]]] = table_data.columns
            column_db: sqlalchemy.Column
            for column_db in columns_db:
                foreign_keys = column_db.foreign_keys

                columns.append({'name': column_db.name,
                                'type': column_db.type,
                                'autoincrement': column_db.autoincrement,
                                'foreign_keys': foreign_keys,
                                'primary_key': column_db.primary_key})
            return columns
        except Exception as exc:
            self.handle_general_exceptions('get_table_meta_data', exc)

    @staticmethod
    def extract_schema_table_name(database_table: str) -> dict[str, str]:
        database_names = database_table.replace('[', '').replace(']', '').split('.')
        if len(database_names) == 1:
            return {'schema': 'dbo', 'table': database_names}
        return {'schema': database_names[0], 'table': database_names[1]}

    def get_table_meta_data_simple_string(self, database_name: str, table_name: str) -> TableMetadata:
        table_data = self.extract_schema_table_name(table_name)
        return self.get_table_meta_data(database_name, table_data['schema'], table_data['table'])

    @staticmethod
    def get_primary_columns(table_data: TableRecords) -> TableMetadata:
        primary_columns = []
        for dataRow in table_data['columns']:
            if dataRow['primary_key']:
                primary_columns.append(dataRow)
        return primary_columns

    def execute_sql_script_no_data(self, database_name: str, sql_script: str) -> None:
        try:
            if self.enable_logging:
                logging.basicConfig()
                logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
            connection = self.get_connection_object(database_name)
            connection.execute(text(sql_script))
            connection.commit()
            connection.close()
        except Exception as exc:
            self.handle_general_exceptions('execute_sql_script_no_data', exc)

    def execute_sql_script(self, database_name: str | None, sql_script: str) -> list[any]:
        try:
            if self.enable_logging:
                logging.basicConfig()
                logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
            connection = self.get_connection_object(database_name)
            result_set = connection.execute(text(sql_script))
            data_row = []
            if result_set is not None:
                for row in result_set:
                    data_row.append(row)
            connection.commit()
            connection.close()
            return data_row
        except Exception as exc:
            self.handle_general_exceptions('execute_sql_script', exc)

    @staticmethod
    def handle_general_exceptions(method_name: str, exception: Exception) -> None:
        print(f'DatabaseOperations Method : {method_name}')
        print('ex : ', exception)
        tb = traceback.TracebackException.from_exception(exception)
        print(''.join(tb.stack.format()))
