from datetime import datetime
import traceback
from typing import Any, Literal

from sqlalchemy import ForeignKey
from sqlalchemy.sql.type_api import TypeEngine

from source_code.database_operations import DatabaseOperations
from tqdm import tqdm

def get_current_timestamp() -> str:
    return f"--- {datetime.today().strftime('%Y-%m-%d %H:%M:%S')}  \r\n\r\n"


class ScriptGenerator:

    def create_insert_statement(self, database_name: str, table_name: str,
                                table_data: DatabaseOperations.TableRecords, add_record: bool) -> str:
        try:
            show_identity_statement = self.has_table_columns_have_autoincrement(table_data)
            auto_columns = self.get_table_columns_are_autoincrement(table_data)
            query = table_data['query']
            output_sql = f'---   {query} \n'
            if not add_record:
                output_sql += f'IF NOT EXISTS( {query})   \n'
                output_sql += f' BEGIN  \n'
            if add_record == False and show_identity_statement:
                output_sql += f'   SET IDENTITY_INSERT {table_name} ON; \n'
            insert_start_text = f'   INSERT INTO {table_name} (\n  '
            loop_break_index = 5
            loop_counter = 0

            column_text = ''
            auto_row_index = []
            for row_index, column in enumerate(table_data['columns']):
                if len(column_text) > 0:
                    column_text += ' ,'
                is_auto_row = column['name'] in auto_columns
                if is_auto_row:
                    auto_row_index.append(row_index)
                if add_record and is_auto_row == False:
                    column_text += f"[{column['name']}] "
                if not add_record:
                    column_text += f"[{column['name']}] "
                loop_counter += 1
                if loop_counter >= loop_break_index:
                    column_text += '\n    '
                    loop_counter = 0

            columns_section_text = f' {column_text})\n    VALUES \n'
            head_section_text = f' {insert_start_text} {columns_section_text}'
            output_sql += head_section_text
            loop_counter = 0
            data_text = ''
            bundle_count =0
            # for row_data in table_data['data']:
            #for row_data in tqdm(table_data['data']):
            for row_index, dataRow in enumerate(tqdm(table_data['data'])):
                if bundle_count > 0:
                    data_text += ', \n    '
                data_text += '    ('
                add_to_new_row = False
                for column_index, data in enumerate(dataRow):
                    is_auto_row = column_index in auto_row_index
                    if add_to_new_row:
                        data_text += ' ,'
                    if add_record and is_auto_row == False:
                        data_text += self.format_row_data_type_with_column(data, table_data['columns'][column_index])
                        add_to_new_row = True
                    if not add_record:
                        data_text += self.format_row_data_type_with_column(data, table_data['columns'][column_index])
                        add_to_new_row = True
                    loop_counter += 1
                    if loop_counter >= loop_break_index:
                        data_text += '\n    '
                        loop_counter = 0
                data_text += ')'
                bundle_count +=1
                if bundle_count >= 100:
                    bundle_count =0
                    data_text += f";\n   {head_section_text}"
                loop_counter = 0

            output_sql += f'  {data_text};\n\n'
            if add_record == False and show_identity_statement:
                output_sql += f'   SET IDENTITY_INSERT {table_name} OFF; \n'
            if not add_record:
                output_sql += f' END  \n\n'
            output_sql += get_current_timestamp()
            return output_sql
        except Exception as exc:
            self.handle_general_exceptions('create_insert_statement', exc)

    def create_update_statement(self, database_name: str, table_name: str,
                                table_data: DatabaseOperations.TableRecords,
                                primary_columns: DatabaseOperations.TableMetadata) -> str:
        try:
            primary_column_index = self.find_column_primary_indexes(primary_columns, table_data)

            number_of_columns = len(table_data['columns'])

            query = table_data['query']

            output_sql = f' ---   {query} \n'
            output_sql += f'IF EXISTS( {query} ) \n'
            output_sql += f'BEGIN  \n\n'

            # for row_data in table_data['data']:
            for row_data in tqdm(table_data['data']):

                loop_break_index = 5
                loop_counter = 0
                output_sql += f'   UPDATE {table_name} \n'
                output_sql += '    SET '
                column_text = ''

                for loop_columns in range(0, number_of_columns):
                    if loop_columns not in primary_column_index:
                        if len(column_text) > 0:
                            column_text += ' ,'
                        column = table_data['columns'][loop_columns]['name']
                        value = self.format_row_data_type_with_column(row_data[loop_columns],
                                                                      table_data['columns'][loop_columns])
                        column_text += f" {column} = {value}"
                        loop_counter += 1
                        if loop_counter >= loop_break_index:
                            column_text += '\n    '
                            loop_counter = 0

                output_sql += f'  {column_text}\n'

                where_text = ''

                for loop_columns in range(0, number_of_columns):
                    if loop_columns in primary_column_index:
                        if len(where_text) > 0:
                            where_text += '\n    AND ,'
                        column = table_data['columns'][loop_columns]['name']
                        value = self.format_row_data_type_with_column(
                            row_data[loop_columns], table_data['columns'][loop_columns])
                        where_text += f"{column} = {value}"
                output_sql += f'    WHERE {where_text};\n'
            output_sql += f'END  \n\n'
            output_sql += get_current_timestamp()
            return output_sql
        except Exception as exc:
            self.handle_general_exceptions('create_update_statement', exc)

    def create_insert_pk_statement(self, database_name: str, table_name: str,
                                table_data: DatabaseOperations.TableRecords,
                                primary_columns: DatabaseOperations.TableMetadata) -> str:
        try:
            primary_column_index = self.find_column_primary_indexes(primary_columns, table_data)

            number_of_columns = len(table_data['columns'])

            query = table_data['query']

            output_sql = f' ---   {query} \n'

            #for row_data in table_data['data']:
            for row_index_outter, row_data in enumerate(tqdm(table_data['data'])):
            #for row_data in tqdm(table_data['data']):

                where_text = ''
                for loop_columns in range(0, number_of_columns):
                    if loop_columns in primary_column_index:
                        if len(where_text) > 0:
                            where_text += '\n    AND ,'
                        column = table_data['columns'][loop_columns]['name']
                        value = self.format_row_data_type_with_column(
                            row_data[loop_columns], table_data['columns'][loop_columns])
                        where_text += f"{column} = {value}"
                output_sql += f'IF NOT EXISTS( SELECT * FROM {table_name} WHERE {where_text})\n'
                output_sql +=f"BEGIN \n"

                output_sql += f'   SET IDENTITY_INSERT {table_name} ON; \n'
                insert_start_text = f'   INSERT INTO {table_name} (\n  '
                loop_break_index = 5
                loop_counter = 0

                column_text = ''
                for row_index, column in enumerate(table_data['columns']):
                    if len(column_text) > 0:
                        column_text += ' ,'
                    column_text += f"[{column['name']}] "
                    loop_counter += 1
                    if loop_counter >= loop_break_index:
                        column_text += '\n    '
                        loop_counter = 0

                columns_section_text = f' {column_text})\n    VALUES \n'
                head_section_text = f' {insert_start_text} {columns_section_text}'
                output_sql += head_section_text
                loop_counter = 0
                data_text = ''

                data_text += '   ('
                add_to_new_row = False
                for column_index, data in enumerate(row_data):
                    if add_to_new_row:
                        data_text += ' ,'
                    data_text += self.format_row_data_type_with_column(data, table_data['columns'][column_index])
                    add_to_new_row = True
                    loop_counter += 1
                    if loop_counter >= loop_break_index:
                        data_text += '\n    '
                        loop_counter = 0
                data_text += ')'

                output_sql += f'  {data_text};\n\n'
                output_sql += f'   SET IDENTITY_INSERT {table_name} OFF; \n'
                output_sql += f' END \n'
                output_sql += f' ----Row {row_index_outter}\n\n'

            output_sql += get_current_timestamp()
            return output_sql
        except Exception as exc:
            self.handle_general_exceptions('create_update_statement', exc)

    def find_column_primary_indexes(self, primary_columns: list[
        dict[str | int, Literal["auto", "ignore_fk"] | str | set[ForeignKey] | TypeEngine | bool]], table_data: dict[
        str | int, list[Any] | list[
            dict[str, Literal["auto", "ignore_fk"] | str | set[ForeignKey] | TypeEngine | bool]]]) -> list[Any]:
        primary_column_index = []
        for index, columns in enumerate(table_data['columns']):
            for primary_column in primary_columns:
                if columns['name'] == primary_column['name']:
                    primary_column_index.append(index)
        return primary_column_index

    @staticmethod
    def has_table_columns_have_autoincrement(table_data: DatabaseOperations.TableRecords) -> bool:
        has_autoincrement = False
        for dataRow in table_data['columns']:
            if dataRow['autoincrement']:
                if not has_autoincrement:
                    has_autoincrement = True
                    break
        return has_autoincrement

    @staticmethod
    def get_table_columns_are_autoincrement(table_data: DatabaseOperations.TableRecords) -> [str]:
        autoincrement_columns = []
        for dataRow in table_data['columns']:
            if dataRow['autoincrement']:
                autoincrement_columns.append(dataRow['name'])
        return autoincrement_columns

    def format_row_data_type_with_column(self, row_data: any,
                                         column_data: DatabaseOperations.TableMetadataItem) -> str:
        try:
            if row_data is None:
                return 'NULL'

            type_description = str(column_data['type'])

            is_numeric = False
            is_string = False
            is_datetime = False
            is_varbinary = False
            is_xml = False

            is_bool = type_description.startswith(('BOOLEAN', 'BIT'))
            if not is_bool:
                is_string = type_description.startswith(('UNIQUEIDENTIFIER', 'TEXT', 'NVARCHAR', 'VARCHAR', 'NCHAR', 'CHAR'))
                if not is_string:
                    is_datetime = type_description.startswith(('DATETIMEOFFSET', 'DATETIME', 'DATE',
                                                               'TIMESTAMP', 'TIME'))
                    if not is_datetime:
                        numbers_types = ('INTEGER', 'DECIMAL', 'BIGINT', 'FLOAT', 'INT', 'NUMERIC', 'REAL', 'SMALLINT',
                                         'TINYINT', 'MONEY')
                        is_numeric = type_description.startswith(numbers_types)
                        if not is_numeric:
                            is_varbinary = type_description.startswith('VARBINARY')
                            if not is_varbinary:
                                is_xml = type_description.startswith('XML')
                                if not is_xml:
                                    print(f"Warning unknown type '{row_data}' : '{type_description}'")

            if is_numeric:
                output_text = str(row_data)
            elif is_string:
                row_item = row_data.replace("'", "''")
                output_text = f"'{row_item}'"
            elif is_datetime:
                datetime_with_extra = str(row_data)
                datetime = datetime_with_extra.split('.')
                row_item = str(datetime[0])
                output_text = f"'{row_item}'"
            elif is_bool:
                row_item = '0'
                if row_data == 'True':
                    row_item = '1'
                output_text = row_item
            elif is_varbinary:
                row_item = str(row_data).replace("'", "''")
                output_text = f"CONVERT(varbinary, '{row_item}')"
            elif is_xml:
                row_item = str(row_data).replace("'", "''")
                output_text = f"CONVERT(XML, '{row_item}')"
            else:
                row_item = str(row_data).replace("'", "''")
                output_text = f"'{row_item}'"

            return output_text
        except Exception as exc:
            self.handle_general_exceptions('format_row_data_type_with_column', exc)

    @staticmethod
    def handle_general_exceptions(method_name: str, exception: Exception) -> None:
        print(f'ScriptGenerator Method : {method_name}')
        print('ex : ', exception)
        tb = traceback.TracebackException.from_exception(exception)
        print(''.join(tb.stack.format()))