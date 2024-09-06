from datetime import datetime
import traceback
from source_code.database_operations import DatabaseOperations


def get_current_timestamp() -> str:
    return f"--- {datetime.today().strftime('%Y-%m-%d %H:%M:%S')}  \r\n\r\n"


class CSharpObjectGenerator:

    def create_object_statement(self, database_name: str, table_name: str,
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

            output_sql = f' /// {database_name}  {query} \n'
            for row_data in table_data['data']:
                loop_break_index = 5
                loop_counter = 0
                object_name = self.format_name(table_name)
                output_sql += f'    {object_name}.Add( new {object_name}'
                output_sql += 'Row {\n'
                column_text = ''

                for loop_columns in range(0, number_of_columns):
                    if len(column_text) > 0:
                        column_text += ' ,'
                    column = table_data['columns'][loop_columns]['name']
                    value = self.format_row_data_type_with_column(row_data[loop_columns],
                                                                  table_data['columns'][loop_columns])
                    property_name =  self.format_name(column)
                    column_text += f" {property_name} = {value}"
                    loop_counter += 1
                    if loop_counter >= loop_break_index:
                        column_text += '\n    '
                        loop_counter = 0

                output_sql += f'  {column_text}\n'
                output_sql += '}'


            output_sql += f');  \n\n'
            output_sql += get_current_timestamp()
            return output_sql
        except Exception as exc:
            self.handle_general_exceptions('create_object_statement', exc)

    def format_row_data_type_with_column(self, row_data: any,
                                         column_data: DatabaseOperations.TableMetadataItem) -> str:
        try:
            if row_data is None:
                return 'null'

            type_description = str(column_data['type'])

            is_integer = False
            is_uniqueidentifier = False
            is_long = False
            is_decimal = False
            is_string = False
            is_datetime = False
            is_datetimeoffset = False
            is_varbinary = False
            is_xml = False

            is_bool = type_description.startswith(('BOOLEAN', 'BIT'))
            if not is_bool:
                is_string = type_description.startswith(('TEXT', 'NVARCHAR', 'VARCHAR', 'NCHAR', 'CHAR'))
                if not is_string:
                    is_uniqueidentifier = type_description.startswith(('UNIQUEIDENTIFIER'))
                    if not is_uniqueidentifier:
                        is_datetimeoffset = type_description.startswith(('DATETIMEOFFSET'))
                        if not is_datetimeoffset:
                            is_datetime = type_description.startswith(('DATETIMEOFFSET', 'DATETIME', 'DATE',
                                                                       'TIMESTAMP', 'TIME'))
                            if not is_datetime:
                                integers_types = ('INTEGER','BIGINT', 'INT', 'NUMERIC', 'SMALLINT','TINYINT')
                                is_integer = type_description.startswith(integers_types)
                                if not is_integer:
                                    longs_types = ('BIGINT')
                                    is_long = type_description.startswith(longs_types)
                                    if not is_long:
                                        decimals = ('DECIMAL', 'FLOAT','REAL', 'MONEY')
                                        is_decimal = type_description.startswith(decimals)
                                        if not is_decimal:
                                            is_varbinary = type_description.startswith('VARBINARY')
                                            if not is_varbinary:
                                                is_xml = type_description.startswith('XML')
                                                if not is_xml:
                                                    print(f"Warning unknown type '{row_data}' : '{type_description}'")

            if is_integer:
                output_text = str(row_data)
            elif is_long:
                output_text = f"{row_data}L"
            elif is_decimal:
                output_text = f"{row_data}M"
            elif is_string:
                output_text = f'"{row_data}"'
            elif is_uniqueidentifier:
                output_text = f'Guid.Parse("{row_data}")'
            elif is_datetime:
                datetime_with_extra = str(row_data)
                datetime = datetime_with_extra.split('.')
                row_item = str(datetime[0])
                output_text = f'DateTime.Parse("{row_item}")'
            elif is_datetimeoffset:
                datetime_with_extra = str(row_data)
                datetime = datetime_with_extra.split('.')
                row_item = str(datetime[0])
                output_text = f'new DateTimeOffSet(DateTime.Parse("{row_item}"))'
            elif is_bool:
                row_item = 'false'
                if row_data == 'True':
                    row_item = 'true'
                output_text = row_item
            elif is_varbinary:
                row_item = str(row_data).replace('"', '""')
                output_text = f'"{row_item}"'
            elif is_xml:
                row_item = str(row_data).replace('"', '""')
                output_text = f'"{row_item}"'
            else:
                row_item = str(row_data).replace('"', '""')
                output_text = f'"{row_item}"'

            return output_text
        except Exception as exc:
            self.handle_general_exceptions('format_row_data_type_with_column', exc)

    @staticmethod
    def format_name(name: str) -> str:
        name_parts = name.split('.')
        if len(name_parts) == 1:
            output = name
        else:
            output = name_parts[1]
        output = output.replace('[', '').replace(']', '')
        return output

    @staticmethod
    def handle_general_exceptions(method_name: str, exception: Exception) -> None:
        print(f'CSharpObjectGenerator Method : {method_name}')
        print('ex : ', exception)
        tb = traceback.TracebackException.from_exception(exception)
        print(''.join(tb.stack.format()))