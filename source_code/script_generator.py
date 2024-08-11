from datetime import datetime
import traceback
from source_code.database_operations import DatabaseOperations

def get_current_timestamp() -> str:
    return f"--- {datetime.today().strftime('%Y-%m-%d %H:%M:%S')}  \r\n"

class ScriptGenerator:

    def create_insert_statement(self, database_name: str, table_name: str,
                                table_data: DatabaseOperations.TableRecords) -> str:
        try:
            show_identity_statement = self.has_table_columns_have_autoincrement(table_data)

            query = table_data['query']
            output_sql = f'---   {query} \n'
            output_sql += f'---   USE {database_name}; \n'
            output_sql += f'IF NOT EXISTS( {query})   \n'
            output_sql += f' BEGIN  \n'
            if show_identity_statement:
                output_sql += f'   SET IDENTITY_INSERT {table_name} ON; \n'
            output_sql += f'--- INSERT INTO   [{database_name}].{table_name} (\n '
            output_sql += f'   INSERT INTO   {table_name} \n      ('
            loop_break_index = 5
            loop_counter = 0

            column_text = ''
            for column in table_data['columns']:
                if len(column_text) > 0:
                    column_text += ' ,'
                column_text += f"[{column['name']}] "
                loop_counter += 1
                if loop_counter >= loop_break_index:
                    column_text += '\n    '
                    loop_counter = 0

            output_sql += f' {column_text})\n    VALUES \n'

            loop_counter = 0
            data_text = ''
            for row_index, dataRow in enumerate(table_data['data']):
                if row_index > 0:
                    data_text += ', \n    '
                data_text += '    ('
                for column_index, data in enumerate(dataRow):
                    if column_index > 0:
                        data_text += ' ,'
                    data_text += self.format_row_data_type_with_column(data, table_data['columns'][column_index])
                    loop_counter += 1
                    if loop_counter >= loop_break_index:
                        data_text += '\n    '
                        loop_counter = 0
                data_text += ')'
                loop_counter = 0

            output_sql += f'  {data_text};\n\n'
            if show_identity_statement:
                output_sql += f'   SET IDENTITY_INSERT {table_name} OFF; \n'
            output_sql += f' END  \n\n'
            output_sql += get_current_timestamp()
            return output_sql
        except Exception as exc:
            self.handle_general_exceptions('create_insert_statement', exc)

    def create_update_statement(self, database_name: str, table_name: str,
                                table_data: DatabaseOperations.TableRecords,
                                primary_columns: DatabaseOperations.TableMetadata) -> str:
        try:
            primary_column_index = []
            for index, columns in enumerate(table_data['columns']):
                for primary_column in primary_columns:
                    if columns['name'] == primary_column['name']:
                        primary_column_index.append(index)

            number_of_columns = len(table_data['columns'])

            query = table_data['query']

            output_sql = f' ---   {query} \n'
            output_sql += f'IF EXISTS( {query} ) \n'
            output_sql += f'BEGIN  \n\n'
            output_sql += f'--- UPDATE [{database_name}].{table_name} (\n'

            for row_data in table_data['data']:
                loop_break_index = 5
                loop_counter = 0
                output_sql += f'   UPDATE {table_name} \n    SET '
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

    @staticmethod
    def has_table_columns_have_autoincrement(table_data: DatabaseOperations.TableRecords) -> bool:
        has_autoincrement = False
        for dataRow in table_data['columns']:
            if dataRow['autoincrement']:
                if not has_autoincrement:
                    has_autoincrement = True
                    break
        return has_autoincrement

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
                is_string = type_description.startswith(('UNIQUEIDENTIFIER', 'NVARCHAR', 'VARCHAR', 'NCHAR', 'CHAR'))
                if not is_string:
                    is_datetime = type_description.startswith(('DATETIMEOFFSET', 'DATETIME', 'DATE'
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
                                    print(f'Warning unknown type {row_data} : {type_description}')
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
