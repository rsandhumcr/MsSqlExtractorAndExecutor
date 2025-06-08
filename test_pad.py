from source_code.database_operations import DatabaseOperations
from source_code.file_operations import FileOperations
from source_code.parse_sql_parameters import ParseSqlParameters
from source_code.sql_operations import SqlOperations
from source_code.script_generator import ScriptGenerator
from source_code.user_options import UserOptions

import questionary
from source_code.database_config import  DatabaseConfig
import pyodbc
import sys
databaseSelector = DatabaseOperations()
file_operations = FileOperations()
parse_sql_parameters = ParseSqlParameters()
user_options = UserOptions()
SqlOperations = SqlOperations()

#db_name= 'AdventureWorksLT2019'
#full_path = 'library/adworks/Select_product2.sql'
#sql_script = file_operations.read_file(full_path)

#script_data = parse_sql_parameters.replace_parameters_with_prompts(sql_script)

#data_rows = databaseSelector.execute_sql_script(db_name, script_data['sql_script'])
#data_rows = databaseSelector.execute_sql_script_raw_connection(db_name, script_data['sql_script'])

#print(data_rows)

