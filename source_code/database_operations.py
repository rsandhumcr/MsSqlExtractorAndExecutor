import traceback
import logging
import sqlalchemy
from sqlalchemy import text, create_engine, PoolProxiedConnection, Sequence
from sqlalchemy.engine.interfaces import DBAPICursor
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

        # ms_sql_driver = "SQL+Server+Native+Client+11.0"
        ms_sql_driver = "ODBC+Driver+17+for+SQL+Server"

        if is_connection_local:
            # Local connection
            connection_string_value = f'mssql+pyodbc://./{database_name}?driver={ms_sql_driver}'
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
                "driver": ms_sql_driver,
                "Encrypt": "yes",
                "TrustServerCertificate": "yes",
            },
        )
        return connection_url

    def get_connection_object(self, database_name: str) -> sqlalchemy.engine.Connection:
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

    def get_raw_connection_object(self, database_name: str) -> PoolProxiedConnection:
        try:
            connection_info = self.get_connection_info(database_name)
            raw_connection: PoolProxiedConnection = create_engine(connection_info, echo=False).raw_connection()
            return raw_connection
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
            for row in result_set['data']:
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
            for row in result_set['data']:
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
            for row in result_set['data']:
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

    def execute_sql_script(self, database_name: str | None, sql_script: str) -> dict[str, list[any]]:
        try:
            if self.enable_logging:
                logging.basicConfig()
                logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
            connection = self.get_connection_object(database_name)

            result_set = connection.execute(text(sql_script))
            columns = []
            for column in result_set._metadata.keys:
                columns.append(column)
            data_row = []
            if result_set is not None:
                for row in result_set:
                    data_row.append(row)

            connection.commit()
            connection.close()
            return {'data': data_row, 'columns': columns}
        except Exception as exc:
            self.handle_general_exceptions('execute_sql_script', exc)

    def execute_sql_script_raw_connection(self, database_name: str | None, sql_script: str) -> list[dict[str, list[any]]]:
        result = []
        try:
            if self.enable_logging:
                logging.basicConfig()
                logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
            raw_connection = self.get_raw_connection_object(database_name)

            cursor = raw_connection.cursor()
            cursor.execute(sql_script)

            if cursor.description is not None:
                result_set = cursor.fetchall()
                data_first = self.extract_result_data(result_set, cursor)
                result.append(data_first)

            while cursor.nextset():
                if cursor.description is not None:
                    result_set = cursor.fetchall()
                    data_second = self.extract_result_data(result_set, cursor)
                    result.append(data_second)

            raw_connection.commit()
            raw_connection.close()
            return result

        except Exception as exc:
            self.handle_general_exceptions('execute_sql_script_raw_connection', exc)

    @staticmethod
    def extract_result_data(result_set: Sequence, cursor: DBAPICursor) -> dict[str, list[any]]:
        columns = []
        for column in cursor.description:
            columns.append(column[0])
        types = []
        for column in cursor.description:
            types.append(column[1].__name__)
        data_row = []
        if result_set is not None:
            for row in result_set:
                data_row.append(row)
        return {'data': data_row, 'columns': columns, 'types': types}

    @staticmethod
    def handle_general_exceptions(method_name: str, exception: Exception) -> None:
        print(f'DatabaseOperations Method : {method_name}')
        print('ex : ', exception)
        tb = traceback.TracebackException.from_exception(exception)
        print(''.join(tb.stack.format()))
