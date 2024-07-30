import sys
import questionary
from source_code.database_operations import DatabaseOperations
from source_code.file_operations import FileOperations
from source_code.script_generator import ScriptGenerator
from source_code.user_options import UserOptions
from source_code.sql_operations import SqlOperations

output_path_file = 'output/testfile.sql'
databaseSelector = DatabaseOperations()
file_operations = FileOperations()
script_generator = ScriptGenerator()
sql_operations: SqlOperations = SqlOperations()
user_options = UserOptions()


def extract_data() -> None:
    db_name = user_options.get_database_name()

    table_name = 'Search again'
    while table_name == 'Search again':
        table_search_name = input('Enter search term for database table name ? ')
        table_name = user_options.search_table_name(db_name, table_search_name)

    table_info = databaseSelector.get_table_meta_data_simple_string(db_name, table_name)

    has_fk_relationships = sql_operations.print_table_info(table_name, table_info)

    where_clause = input(f'Where clause for table {table_name} (not including WHERE keyword) ? ')

    include_relationships = False
    if has_fk_relationships:
        if where_clause:
            include_relationships = user_options.get_yes_no_question('Do you want related tables data ?')
    selected_option = user_options.get_script_output_options()
    if selected_option == 'abort':
        return
    sql_operations.extract_table_data(output_path_file, db_name, table_name, where_clause,
                                      selected_option, include_relationships, [])


def user_options_input() -> None:
    user_option = 'extract another'
    while user_option != 'abort':
        if user_option == 'abort':
            exit()
        if user_option == 'extract another':
            extract_data()
        user_option = questionary.select(
            "Select an option",
            choices=user_options).ask()  # returns value of selection


def execute_commandline() -> None:
    if len(sys.argv) == 6 or len(sys.argv) == 7:
        execute_extract_from_cmdline()
    elif len(sys.argv) == 3:
        show_table_info()
    else:
        show_argument_options()


def execute_extract_from_cmdline() -> None:
    args = sys.argv
    include_mapped_tables = False
    if args[5] == 'True':
        include_mapped_tables = True
    output_file = output_path_file
    if len(sys.argv) == 7:
        output_file = args[6]
    db_name = args[1]
    table_name = args[2]
    name_check = sql_operations.check_database_table_names(db_name, table_name)
    if name_check:
        sql_operations.extract_table_data(output_file, db_name, table_name, args[3], args[4], include_mapped_tables, [])
        print(f"Output file : {output_file}")


def show_table_info() -> None:
    args = sys.argv
    db_name = args[1]
    table_name = args[2]
    table_name_parts = table_name.split('.')
    if len(table_name_parts) == 1:
        table_name = 'dbo.' + table_name
    name_check = sql_operations.check_database_table_names(db_name, table_name)
    if name_check:
        table_info = databaseSelector.get_table_meta_data_simple_string(db_name, table_name)
        sql_operations.print_table_info(table_name, table_info)


def show_argument_options() -> None:
    print(f"Arguments passed : {sys.argv}")
    print("Command line parameters required : ")
    print("Extracting data")
    print("> py extract_data.py <db name> <table name with schema> <where clause> <insert/update/update and insert> "
          "<Include related tables True/False> [output file]")
    print("e.g")
    print(" > py extract_data.py AdventureWorksLT2019  SalesLT.SalesOrderHeader 'SalesOrderID = 71774' insert True")
    print("Show table info")
    print(" > extract_data.py <db name> <table name with schema>")
    print("e.g")
    print(" > py extract_data.py AdventureWorksLT2019  SalesLT.SalesOrderHeader")
    exit()


if __name__ == '__main__':
    if len(sys.argv) == 1:
        user_options = ['abort', 'extract another']
        user_options_input()
    else:
        execute_commandline()
