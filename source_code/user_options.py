import questionary
import traceback
from source_code.database_operations import DatabaseOperations
from source_code.file_operations import FileOperations

file_operations = FileOperations()
database_operations = DatabaseOperations()


class UserOptions:

    def get_database_options(self) -> str:
        db_name = self.get_database_name()
        return db_name

    @staticmethod
    def get_files_in_directory(file_path: str) -> str:
        library_files = file_operations.get_files_in_directory(file_path)

        library_files.append('> Database selection')
        library_files.append('> ..')
        library_files.append('> Abort execution')

        selected_file = questionary.select(
            "Select a file to execute",
            choices=library_files).ask()  # returns value of selection
        return selected_file

    @staticmethod
    def get_yes_no_question(question: str) -> bool:
        yes_no = ['Yes', 'No']
        selected_answer = questionary.select(
            question,
            choices=yes_no).ask()  # returns value of selection
        return selected_answer == 'Yes'

    @staticmethod
    def get_script_output_options() -> str:
        execute_options = ['abort', 'insert', 'update', 'update and insert']
        selected_option = questionary.select(
            "Select an option",
            choices=execute_options).ask()  # returns value of selection
        return selected_option

    def get_database_name(self) -> str:
        try:
            database_name = database_operations.get_database()
            database_selected = questionary.select(
                "Select a database",
                choices=database_name).ask()  # returns value of selection

            return database_selected
        except Exception as exc:
            self.handle_general_exceptions('get_database_name', exc)

    @staticmethod
    def get_database_names() -> list[str]:

        database_name = database_operations.get_database()
        database_selected = questionary.checkbox(
            "Select databases",
            choices=database_name).ask()  # returns value of selection

        return database_selected

    @staticmethod
    def search_table_name(database_name: str, table_name_search: str) -> str:
        schema_table_name = database_operations.search_table_name(database_name, table_name_search)
        schema_table_name.append('Search again')
        table_selected = questionary.select(
            "Select a table",
            choices=schema_table_name).ask()  # returns value of selection
        return table_selected

    @staticmethod
    def handle_general_exceptions(method_name: str, exception: Exception) -> None:
        print(f'UserOptions Method : {method_name}')
        print('ex : ', exception)
        tb = traceback.TracebackException.from_exception(exception)
        print(''.join(tb.stack.format()))

    @staticmethod
    def select_row_or_columns_result() -> bool:
        is_columns = questionary.select(
            "Select a columns or rows result format",
            choices=['Rows', 'Columns']).ask()  # returns value of selection
        return bool(is_columns == 'Columns')
