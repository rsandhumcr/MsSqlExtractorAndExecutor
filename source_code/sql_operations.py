from sqlalchemy import ForeignKey
from tabulate import tabulate
import traceback
from source_code.file_operations import FileOperations
from source_code.script_generator import ScriptGenerator
from source_code.database_operations import DatabaseOperations

file_operations = FileOperations()
databaseSelector = DatabaseOperations()
script_generator = ScriptGenerator()


class SqlOperations:
    type RelationQuery = list[dict[str, str] | None]
    type RelationQueryItem = dict[str, str] | None

    def print_table_info(self, table_name: str, table_info: DatabaseOperations.TableMetadata) -> bool:
        has_foreign_keys = False
        table_column_description = []
        count_columns = 0
        for column_index, table_columns in enumerate(table_info):
            key_marker = ''
            if table_columns['primary_key']:
                key_marker += '+'
            if table_columns['autoincrement']:
                key_marker += '*'
            foreign_keys_str = ''
            foreign_keys = table_columns['foreign_keys']
            if foreign_keys:
                foreign_keys_str = self.format_foreign_keys(foreign_keys)
                has_foreign_keys = True
            columns_info = [f"{column_index} {key_marker}", table_columns['name'],
                            table_columns['type'], foreign_keys_str]

            table_column_description.append(columns_info)
            count_columns += 1
        headers = ['Index', 'Name', 'Type', 'Foreign Keys']
        print('(+ = primary key, * = autoincrement)')
        print(tabulate(table_column_description, headers, tablefmt="simple_grid"))
        print(f'Table : {table_name} has {count_columns} columns')
        return has_foreign_keys

    def format_foreign_keys(self, foreign_keys: set[ForeignKey]) -> list[str]:
        data_output = []
        for foreign_key in foreign_keys:
            key_info = self.format_foreign_key(foreign_key)
            data_output.append(key_info)
        return data_output

    @staticmethod
    def format_foreign_key(foreign_key: ForeignKey) -> str:
        fk_str = str(foreign_key)
        cleaned_str = fk_str.replace('ForeignKey(\'', '').replace('\')', '')
        return cleaned_str

    def generate_selects_from_relationships(self, table_info: DatabaseOperations.TableRecords) -> RelationQuery | None:
        has_relations = self.table_has_relations(table_info)
        if not has_relations:
            return
        relationships = self.extract_relationship_data(table_info)
        sql_selects = self.generate_sql_from_relations(relationships)
        return sql_selects

    def extract_relationship_data(self, table_info: DatabaseOperations.TableRecords) -> RelationQuery:
        relationship_data = []
        for column_index, columns in enumerate(table_info['columns']):
            if columns['foreign_keys']:
                for row_index, row in enumerate(table_info['data']):
                    fk_id = row[column_index]
                    for fk_index, foreign_key in enumerate(columns['foreign_keys']):
                        new_rel = [fk_id, self.format_foreign_key(foreign_key)]
                        relationship_data.append(new_rel)
        return relationship_data

    @staticmethod
    def table_has_relations(table_info: DatabaseOperations.TableRecords) -> bool:
        table_columns = table_info['columns']
        has_relations = False
        for columns in table_columns:
            if columns['foreign_keys']:
                has_relations = True
                break
        return has_relations

    def generate_sql_from_relations(self, relationships_data: DatabaseOperations.TableMetadata) -> RelationQuery:
        output_selects = []
        for relationship in relationships_data:
            id_value = str(relationship[0])
            if id_value and id_value != 'None':
                split_table = relationship[1].split('.')
                if not id_value.isnumeric():
                    id_value = f"'{id_value}'"
                select_data = {'schema': split_table[0], 'table': split_table[1],
                               'where': f"{split_table[2]} = {id_value}"}
                self.add_unique_relationships(output_selects, select_data)
        return output_selects

    def add_unique_relationships(self, old_list: RelationQuery, new_list_item: RelationQueryItem) -> None:
        in_found_in_list = self.is_unique_relationships(old_list, new_list_item)
        if not in_found_in_list:
            old_list.append(new_list_item)

    @staticmethod
    def is_unique_relationships(old_list: RelationQuery, new_list_item: RelationQueryItem) -> bool:
        in_found_in_list = False
        for current_select in old_list:
            if current_select['schema'] == new_list_item['schema']:
                if current_select['table'] == new_list_item['table']:
                    if current_select['where'] == new_list_item['where']:
                        in_found_in_list = True
                        break
        return in_found_in_list

    def extract_table_data(self, output_path_file: str, db_name: str, table_name: str, where_clause: str,
                           output_option: str, include_relationships: bool,
                           previous_relationship_selects: RelationQuery):
        row_data = databaseSelector.get_table_data(db_name, table_name, where_clause)

        if len(row_data['data']) == 0:
            print('No data found')
            return

        previous_relationship_selects_output = []
        if include_relationships:
            if where_clause:
                current_relationship_selects = self.generate_selects_from_relationships(row_data)
                if current_relationship_selects:
                    unique_relationship_selects = []

                    for current_relationship in current_relationship_selects:
                        found_in_previous_relationships = self.is_unique_relationships(previous_relationship_selects,
                                                                                       current_relationship)
                        if not found_in_previous_relationships:
                            unique_relationship_selects.append(current_relationship)

                    previous_relationship_selects.extend(unique_relationship_selects)
                    for current_relationship in unique_relationship_selects:
                        previous_relationship_selects_output = self.extract_table_data(output_path_file,
                                   db_name,
                                   f"{current_relationship['schema']}.{current_relationship['table']}",
                                   current_relationship['where'],
                                   output_option,
                                   include_relationships,
                                   previous_relationship_selects)

        self.generate_output_data(db_name, table_name, where_clause, row_data, output_option, output_path_file)
        return previous_relationship_selects_output

    @staticmethod
    def generate_output_data(db_name: str, table_name: str, where_clause: str,
                             row_data: DatabaseOperations.TableRecords,
                             output_option: str, output_path_file: str) -> None:
        primary_columns = databaseSelector.get_primary_columns(row_data)

        print(f'Extracting : {db_name}.{table_name} WHERE {where_clause}')
        if output_option == 'update' or output_option == 'update and insert':
            update_statement = script_generator.create_update_statement(db_name, table_name, row_data, primary_columns)
            file_operations.write_to_file(output_path_file, update_statement)

        if output_option == 'insert' or output_option == 'update and insert':
            insert_statement = script_generator.create_insert_statement(db_name, table_name, row_data)
            file_operations.write_to_file(output_path_file, insert_statement)

    def check_database_table_names(self, db_name: str, table_name: str) -> bool:
        try:
            database_name = databaseSelector.get_database()
            data_is_ok = True
            if db_name not in str(database_name):
                data_is_ok = False
                print(f"Database '{db_name}' not found\nDatabase names :")
                print(database_name)
            else:
                table_name_parts = table_name.split('.')
                table_name_part = table_name_parts[0]
                if len(table_name_parts) == 2:
                    table_name_part = table_name_parts[1]
                schema_table_name = databaseSelector.search_table_name(db_name, table_name_part)
                search_name = self.format_table_names(table_name)
                if search_name not in str(schema_table_name):
                    data_is_ok = False
                    print(f"Table '{table_name}' not found")
                    schema_table_name = databaseSelector.search_table_name(db_name, table_name_part[:3])
                    if len(schema_table_name) > 0:
                        print("Table/s with similar name")
                        print(schema_table_name)
            return data_is_ok
        except Exception as exc:
            self.handle_general_exceptions('check_database_table_names', exc)

    @staticmethod
    def format_table_names(table_name: str) -> str:
        output_table_name = table_name
        found_char = table_name.find("[")
        if found_char == -1:
            table_name_parts = table_name.split('.')
            output_table_name = ''
            for name_part in table_name_parts:
                if output_table_name:
                    output_table_name += '.'
                output_table_name += f"[{name_part}]"
        return output_table_name

    @staticmethod
    def show_table_results(result_set_index: int,script_name: str, show_columns: bool, data_rows: dict[str, list[any]]) -> str:
        row_no = 1
        no_of_records = len(data_rows['data'])
        if no_of_records == 0:
            return ''
        data_output = ''
        if show_columns:
            max_len_column = 0
            data_row = data_rows['data'][0]
            for colindex, column in enumerate(data_row):
                current_len = len(data_rows['columns'][colindex])
                if max_len_column < current_len:
                    max_len_column = current_len

            max_len_type = 0
            for typeindex, type in enumerate(data_row):
                current_len = len(data_rows['types'][typeindex])
                if max_len_type < current_len:
                    max_len_type = current_len
            data_output += f'---- Start {script_name} \r\n'
            for data_row in data_rows['data']:
                data_output += '---- Result Set ' + str(result_set_index) + ' Row ' + str(row_no)+ ' \r\n'
                for colindex, column in enumerate(data_row):
                    column_name = str(data_rows['columns'][colindex])
                    extended_column_name = column_name.ljust(max_len_column, ' ')
                    type_name = str(data_rows['types'][colindex])
                    extended_type_name = type_name.ljust(max_len_type, ' ')
                    data_output += extended_column_name + '  :  ' + str(extended_type_name) + '  :  ' + str(column) + ' \r\n'
                row_no += 1
            data_output += f'---- End {script_name}  \r\n'
        else:
            data_output += 'Columns \r\n'
            data_output += str(data_rows['columns']) + ' \r\n'
            data_output += str(data_rows['types']) + ' \r\n'
            data_output += 'Rows \r\n'
            for data_row in data_rows['data']:
                data_output += '---- Result Set ' + str(result_set_index) + ' Row ' + str(row_no)+ ' \r\n'
                data_output += str(data_row) + ' \r\n'
                row_no += 1
        data_output += 'Result Set ' + str(result_set_index) + ', No. Of Rows : ' + str(no_of_records) + ' \r\n'
        return data_output

    @staticmethod
    def handle_general_exceptions(method_name: str, exception: Exception):
        print(f'SqlOperations Method : {method_name}')
        print('ex : ', exception)
        tb = traceback.TracebackException.from_exception(exception)
        print(''.join(tb.stack.format()))
