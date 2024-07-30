from source_code.database_operations import DatabaseOperations
from source_code.file_operations import FileOperations
from source_code.parse_sql_parameters import ParseSqlParameters
from source_code.user_options import UserOptions

library_path = 'library'

databaseSelector = DatabaseOperations()
file_operations = FileOperations()
parse_sql_parameters = ParseSqlParameters()
user_options = UserOptions()


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
                data_rows = databaseSelector.execute_sql_script(db_name, script_data['sql_script'])
                print(data_rows)
            else:
                databaseSelector.execute_sql_script_no_data(db_name, script_data['sql_script'])


if __name__ == '__main__':
    execute_scripts()
