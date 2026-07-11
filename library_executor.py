import sys
from datetime import datetime
from source_code.database_operations import DatabaseOperations
from source_code.file_operations import FileOperations
from source_code.parse_sql_parameters import ParseSqlParameters
from source_code.user_options import UserOptions
from source_code.sql_operations import SqlOperations
from sqlalchemy.engine import URL

library_path = 'library'
output_file = 'output\\execution.txt'

databaseSelector = DatabaseOperations()
file_operations = FileOperations()
parse_sql_parameters = ParseSqlParameters()
user_options = UserOptions()
SqlOperations = SqlOperations()

def get_current_timestamp() -> str:
    return f"--- {datetime.today().strftime('%Y-%m-%d %H:%M:%S')}  \r\n"

def get_file_timestamp() -> str:
    return f"{datetime.today().strftime('%Y%m%d_%H%M%S')}"

def execute_command_selection() -> None:
    db_config = user_options.get_database_config()
    selected_file = 'initial'

    new_path = library_path

    while selected_file != '> Abort execution':
        print(f"Database (name) : {db_config['db_name']}")
        selected_file = user_options.get_files_in_directory(new_path)
        if selected_file == '> Abort execution':
            exit()
        if selected_file == '> Database selection':
            #db_name = user_options.get_database_name()
            db_config = user_options.get_database_config()
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
            if db_config == None:
                print("There was an issue with the database configuration. Please check the configuration file and try again.")
            if script_data['return_results']:
                execute_script_with_result(db_config, script_data, selected_file)
            else:
                databaseSelector.execute_sql_script_no_data(db_config, script_data['sql_script'])


def execute_script_with_result(db_config: dict[str, str|URL], script_data: dict[str, str], selected_file : str, specific_output_file:str|None) -> None:
    windows_end_line = True
    data_rows = databaseSelector.execute_sql_script_raw_connection(db_config, script_data['sql_script'])
    print_and_write_to_file(output_file, f"Db : {db_config['db_name']}\r\n", windows_end_line)
    if len(data_rows) == 0:
        print_and_write_to_file(output_file, 'No Data Returned', windows_end_line)
        return

    no_of_result_sets = len(data_rows)
    no_of_rows: int = len(data_rows[0]['data'])
    if no_of_result_sets == 1 and no_of_result_sets == 1:
        data_output = f'{selected_file}\r\nYou have {no_of_rows} row/s\r\n' + script_data['parameter_values']
        print_and_write_to_file(output_file, data_output, windows_end_line)
    else:
        print_and_write_to_file(output_file, f'You have:', windows_end_line)
        for result_index, data_row in enumerate(data_rows):
            no_of_rows = len(data_rows[result_index]['data'])
            no_of_columns = len(data_rows[result_index]['columns'])
            row_label = 'rows'
            if no_of_rows == 1:
                row_label = 'row '
            data_output = f'   {no_of_rows} {row_label}, {no_of_columns} columns in result set {result_index + 1}'
            print_and_write_to_file(output_file, data_output, True)

    is_columns = 'Columns'
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
            print_and_write_to_file(output_file, f"Result set {result_set_count}\r\n", windows_end_line)

        outputted_data = False
        if is_columns == 'Columns':
            data_output_str = SqlOperations.show_table_result_columns(result_set_count, selected_file, data_row, show_headers)
            outputted_data=True

        if is_columns == 'Rows':
            data_output_str = SqlOperations.show_table_result_rows(result_set_count, data_row, show_headers)
            outputted_data = True

        if is_columns == 'CSV':
            data_output_str = SqlOperations.show_table_result_csv(data_row)
            outputted_data = True

        if not outputted_data:
            data_output_str = SqlOperations.show_table_result_csv(data_row)

        if data_output_str is not None:
            write_to_file(specific_output_file, data_output_str, windows_end_line)

        current_time = get_current_timestamp()
        output_data = f'Start {current_time} \r\n{data_output_str} \r\nEnd {current_time}'
        print_and_write_to_file(output_file, output_data, windows_end_line)


def write_to_file(file_name: str, data_output_str: str, make_windows_end_line: bool) -> None:
    if make_windows_end_line:
        data_output_str = data_output_str.replace('\r\n', '\n')
    file_operations.write_to_file(file_name, data_output_str)

def print_and_write_to_file(file_name: str, data_output_str: str, make_windows_end_line: bool) -> None:
    print(data_output_str)
    write_to_file(file_name, data_output_str, make_windows_end_line)

def execute_commandline() -> None:
    args = sys.argv

    db_name = args[1]
    db_config = user_options.get_database_config_via_name(db_name)
    if db_config is None:
        print("There was an issue with the database configuration. Please check the configuration file and try again.")

    new_path = args[2]
    selected_file = args[3]

    specific_output_file = None
    if len(args) > 4:
        specific_output_file = args[4]
        if specific_output_file.find("TIMESTAMP") != -1:
            timestamp = get_file_timestamp()
            specific_output_file = specific_output_file.replace("TIMESTAMP", timestamp)
        specific_output_file = f".\\output\\{specific_output_file}"

    full_path = f".\\library\\{new_path}\\{selected_file}"
    sql_script = file_operations.read_file(full_path)
    script_data = parse_sql_parameters.replace_parameters_with_prompts(sql_script)
    if script_data['return_results']:
        execute_script_with_result(db_config, script_data, selected_file, specific_output_file)
    else:
        databaseSelector.execute_sql_script_no_data(db_config, script_data['sql_script'])

if __name__ == '__main__':
    no_of_args = len(sys.argv)
    if no_of_args == 1:
        execute_command_selection()
    else:
        if no_of_args == 4 or no_of_args == 5 :
            execute_commandline()
        else:
            print("Invalid number of arguments. Please provide 4 or 5 arguments.\npy .\\library_executor.py <DbConfig> <directory> <script> [output file | 'TIMESTAMP' ]")