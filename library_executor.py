from datetime import datetime
from source_code.database_operations import DatabaseOperations
from source_code.file_operations import FileOperations
from source_code.parse_sql_parameters import ParseSqlParameters
from source_code.user_options import UserOptions
from source_code.sql_operations import SqlOperations
library_path = 'library'

databaseSelector = DatabaseOperations()
file_operations = FileOperations()
parse_sql_parameters = ParseSqlParameters()
user_options = UserOptions()
SqlOperations = SqlOperations()


def get_current_timestamp() -> str:
    return f"--- {datetime.today().strftime('%Y-%m-%d %H:%M:%S')}  \r\n"


def execute_scripts() -> None:
    db_name = user_options.get_database_options()
    selected_file = 'initial'

    new_path = library_path

    while selected_file != '> Abort execution':
        selected_file = user_options.get_files_in_directory(new_path)
        if selected_file == '> Abort execution':
            exit()
        if selected_file == '> Database selection':
            db_name = user_options.get_database_name()
        elif selected_file == '> ..':
            if library_path != new_path:
                new_path = file_operations.get_parent_directory(new_path)
                print(f"==> Switching up to directory {new_path}")
        elif file_operations.is_directory(new_path, selected_file):
            new_path = f'{new_path}\\{selected_file}'
            print(f"==> Switching down to directory {new_path}")
        else:
            full_path = f"{new_path}\\{selected_file}"
            sql_script = file_operations.read_file(full_path)
            script_data = parse_sql_parameters.replace_parameters_with_prompts(sql_script)
            if script_data['return_results']:
                # data_rows = databaseSelector.execute_sql_script(db_name, script_data['sql_script'])
                data_rows = databaseSelector.execute_sql_script_raw_connection(db_name, script_data['sql_script'])
                if len(data_rows) > 0:
                    no_of_result_sets = len(data_rows)
                    no_of_rows = len(data_rows[0]['data'])
                    if no_of_result_sets == 1 and no_of_result_sets == 1:
                        print(f'You have {no_of_rows} row/s')
                    else:
                        print(f'You have:')
                        for result_index, data_row in enumerate(data_rows):
                            no_of_rows = len(data_rows[result_index]['data'])
                            no_of_columns = len(data_rows[result_index]['columns'])
                            row_label = 'rows'
                            if no_of_rows == 1:
                                row_label = 'row '
                            print(f'   {no_of_rows} {row_label}, {no_of_columns} columns in result set {result_index + 1}')

                    is_columns = True
                    if script_data['result_in_columns'] is None:
                        if no_of_rows > 1 or no_of_result_sets > 1:
                            is_columns = user_options.select_row_or_columns_result()
                    else:
                        is_columns = script_data['result_in_columns']
                    result_set_count = 0
                    show_headers = not script_data['no_headers']
                    for data_row in data_rows:
                        result_set_count += 1
                        if no_of_result_sets > 1:
                            print(f"Result set {result_set_count}")
                        data_output_str = SqlOperations.show_table_results(result_set_count, selected_file,
                                                                           is_columns, data_row, show_headers)
                        print(data_output_str)
                    print(get_current_timestamp())
                else:
                    print('No Data Returned')
            else:
                databaseSelector.execute_sql_script_no_data(db_name, script_data['sql_script'])


if __name__ == '__main__':
    execute_scripts()
