import csv
import io
import traceback
from typing import Any

from sqlalchemy import ForeignKey, URL
from tabulate import tabulate

from source_code.file_operations import FileOperations
from source_code.script_generator import ScriptGenerator
from source_code.database_operations import DatabaseOperations, TableColumn, ResultSet
from source_code.csharp_object_generator import CSharpObjectGenerator
from source_code.csharp_object_generatorV2 import CSharpObjectGeneratorV2

file_operations = FileOperations()
databaseSelector = DatabaseOperations()
script_generator = ScriptGenerator()
csharp_generator = CSharpObjectGenerator()
csharp_generatorV2 = CSharpObjectGeneratorV2()

OUTPUT_FILE = 'output\\execution.txt'

# output_option values that trigger each generator (was a long chain of `or` comparisons)
UPDATE_OPTIONS = {'update', 'update and insert', 'update and insertAdd', 'update and insertPk'}
INSERT_ADD_OPTIONS = {'insertAdd', 'update and insertAdd'}
INSERT_PK_OPTIONS = {'insertPk', 'update and insertPk'}
INSERT_OPTIONS = {'insert', 'update and insert'}


class SqlOperations:
    type RelationQuery = list[dict[str, str]]
    type RelationQueryItem = dict[str, str]

    def print_table_info(self, table_name: str, table_info: TableColumn) -> bool:
        has_foreign_keys = False
        table_column_description = []

        for column_index, table_columns in enumerate(table_info):
            key_marker = ''
            if table_columns.primary_key:
                key_marker += '+'
            if table_columns.autoincrement:
                key_marker += '*'

            foreign_keys_str = ''
            if table_columns.foreign_keys:
                foreign_keys_str = self.format_foreign_keys(table_columns.foreign_keys)
                has_foreign_keys = True

            table_column_description.append([
                f"{column_index} {key_marker}",
                table_columns.name,
                self.format_table_type(table_columns.type),
                foreign_keys_str,
            ])

        count_columns = len(table_column_description)
        headers = ['Index', 'Name', 'Type', 'Foreign Keys']
        legend = '(+ = primary key, * = autoincrement)'

        print(legend)
        print(tabulate(table_column_description, headers, tablefmt="simple_grid"))
        print(f'Table : {table_name} has {count_columns} columns')

        # Single write through the existing file-write abstraction instead of
        # file_operations.write_to_file(...) followed by a raw open(..., 'a').
        report = (
            f'\nTable : {table_name}\n{legend}\n'
            f'{tabulate(table_column_description, headers, tablefmt="simple")}'
            f'\nTable : {table_name} has {count_columns} columns\n'
        )
        file_operations.write_to_file(OUTPUT_FILE, report)

        return has_foreign_keys

    def format_table_type(self, table_type: str) -> str:
        return str(table_type).replace(" COLLATE ", " COLLATE \n")

    def format_foreign_keys(self, foreign_keys: set[ForeignKey]) -> list[str]:
        return [self.format_foreign_key(fk) for fk in foreign_keys]

    @staticmethod
    def format_foreign_key(foreign_key: ForeignKey) -> str:
        return str(foreign_key).replace("ForeignKey('", '').replace("')", '')

    def generate_selects_from_relationships(self, table_info: ResultSet) -> RelationQuery | None:
        if not self.table_has_relations(table_info):
            return None
        relationships = self.extract_relationship_data(table_info)
        return self.generate_sql_from_relations(relationships)

    @staticmethod
    def extract_relationship_data(table_info: ResultSet) -> list[list]:
        relationship_data = []
        for column_index, column in enumerate(table_info['columns']):
            if not column.foreign_keys:
                continue
            for row in table_info['data']:
                fk_id = row[column_index]
                for foreign_key in column.foreign_keys:
                    relationship_data.append([fk_id, SqlOperations.format_foreign_key(foreign_key)])
        return relationship_data

    @staticmethod
    def table_has_relations(table_info: ResultSet) -> bool:
        return any(column.foreign_keys for column in table_info['columns'])

    def generate_sql_from_relations(self, relationships_data: list[list]) -> RelationQuery:
        output_selects: SqlOperations.RelationQuery = []
        for fk_id, foreign_key_str in relationships_data:
            id_value = str(fk_id)
            if not id_value or id_value == 'None':
                continue
            schema, table, key_column = foreign_key_str.split('.')
            if not id_value.isnumeric():
                id_value = f"'{id_value}'"
            select_data = {'schema': schema, 'table': table, 'where': f"{key_column} = {id_value}"}
            self.add_unique_relationships(output_selects, select_data)
        return output_selects

    def add_unique_relationships(self, existing: RelationQuery, candidate: RelationQueryItem) -> None:
        if not self.is_unique_relationships(existing, candidate):
            existing.append(candidate)

    @staticmethod
    def is_unique_relationships(existing: RelationQuery, candidate: RelationQueryItem) -> bool:
        return any(
            item['schema'] == candidate['schema']
            and item['table'] == candidate['table']
            and item['where'] == candidate['where']
            for item in existing
        )

    def extract_table_data(self, output_path_file: str, database_config: dict[str, str | URL], table_name: str,
                           where_clause: str, output_option: str, include_relationships: bool,
                           previous_relationship_selects: RelationQuery) -> RelationQuery:
        row_data = databaseSelector.get_table_data(database_config, table_name, where_clause)

        if len(row_data['data']) == 0:
            print('No data found')
            return previous_relationship_selects

        if include_relationships and where_clause:
            current_relationship_selects = self.generate_selects_from_relationships(row_data)
            current_relationship_selects = self.combine_relationships(current_relationship_selects)

            if current_relationship_selects:
                unique_relationship_selects = [
                    relationship for relationship in current_relationship_selects
                    if not self.is_unique_relationships(previous_relationship_selects, relationship)
                ]
                previous_relationship_selects.extend(unique_relationship_selects)

                for relationship in unique_relationship_selects:
                    self.extract_table_data(
                        output_path_file, database_config,
                        f"{relationship['schema']}.{relationship['table']}",
                        relationship['where'], output_option, include_relationships,
                        previous_relationship_selects,
                    )

        self.generate_output_data(database_config['db_name'], table_name, where_clause, row_data,
                                   output_option, output_path_file)
        return previous_relationship_selects

    @staticmethod
    def combine_relationships(relationships: RelationQuery | None) -> RelationQuery | None:
        """Merge relationships that target the same (schema, table) into one WHERE clause,
        ANDing together clauses that key off different columns.

        Rewritten: the original version removed items from a list while iterating over
        that same list (`cp_current_relationship_selects01.remove(...)` inside a loop
        enumerating it), which can skip elements depending on ordering.
        """
        if not relationships:
            return relationships

        grouped: dict[tuple[str, str], dict[str, str]] = {}
        for relationship in relationships:
            table_key = (relationship['schema'], relationship['table'])
            where_key = relationship['where'].split('=')[0].strip()
            # first clause for a given key column wins; distinct key columns get ANDed
            grouped.setdefault(table_key, {}).setdefault(where_key, relationship['where'])

        return [
            {'schema': schema, 'table': table, 'where': ' AND '.join(wheres.values())}
            for (schema, table), wheres in grouped.items()
        ]

    @staticmethod
    def generate_output_data(db_name: str, table_name: str, where_clause: str, row_data: ResultSet,
                             output_option: str, output_path_file: str) -> None:
        primary_columns = databaseSelector.get_primary_columns(row_data)
        print(f'Extracting : {db_name}.{table_name} WHERE {where_clause}')

        def run(label: str, generate) -> None:
            print(script_generator.time_stamp_message(f"Start {label}"))
            file_operations.write_to_file(output_path_file, generate())
            print(script_generator.time_stamp_message(f"End {label}"))

        if output_option in UPDATE_OPTIONS:
            run('update', lambda: script_generator.create_update_statement(
                db_name, table_name, row_data, primary_columns))

        if output_option in INSERT_ADD_OPTIONS:
            run('insertAdd', lambda: script_generator.create_insert_statement(
                db_name, table_name, row_data, True))

        if output_option in INSERT_PK_OPTIONS:
            run('insertPk', lambda: script_generator.create_insert_pk_statement(
                db_name, table_name, row_data, primary_columns))

        if output_option in INSERT_OPTIONS:
            run('insert', lambda: script_generator.create_insert_statement(
                db_name, table_name, row_data, False))

        if output_option == 'csharp':
            run('csharp', lambda: csharp_generator.create_object_statement(db_name, table_name, row_data))

        if output_option == 'csharpV2':
            run('csharpV2', lambda: csharp_generatorV2.create_object_statement(db_name, table_name, row_data))

    def check_database_table_names(self, db_config: dict[str, str | URL], table_name: str) -> bool:
        try:
            if db_config is None:
                print(f"Database '{db_config}' not found\nDatabase names :")
                return False

            table_name_parts = table_name.split('.')
            table_name_part = table_name_parts[1] if len(table_name_parts) == 2 else table_name_parts[0]

            schema_table_name = databaseSelector.search_table_name(db_config, table_name_part)
            search_name = self.format_table_names(table_name)
            if search_name in str(schema_table_name):
                return True

            print(f"Table '{table_name}' not found")
            similar_tables = databaseSelector.search_table_name(db_config, table_name_part[:3])
            if similar_tables:
                print("Table/s with similar name")
                print(similar_tables)
            return False

        except Exception as exc:
            self.handle_general_exceptions('check_database_table_names', exc)
            return False

    @staticmethod
    def format_table_names(table_name: str) -> str:
        if '[' in table_name:
            return table_name
        return '.'.join(f'[{part}]' for part in table_name.split('.'))

    @staticmethod
    def show_table_result_rows(result_set_index: int, data_rows: dict[str, list[Any]], show_headers: bool) -> str:
        rows = data_rows['data']
        if not rows:
            return ''

        lines = []
        if show_headers:
            lines.append('Columns \r\n')
            lines.append(f"{data_rows['columns']} \r\n")
            lines.append(f"{data_rows['types']} \r\n")
        lines.append('Rows \r\n')

        for row_no, data_row in enumerate(rows, start=1):
            if show_headers:
                lines.append(f'---- Result Set {result_set_index} Row {row_no} \r\n')
            lines.append(f'{data_row} \r\n')

        lines.append(f'Result Set {result_set_index}, No. Of Rows : {len(rows)} \r\n')
        return ''.join(lines)

    @staticmethod
    def show_table_result_columns(result_set_index: int, script_name: str,
                                   data_rows: ResultSet, show_headers: bool) -> str:
        if not data_rows.data:
            return ''

        max_len_column = max(len(str(column)) for column in data_rows.columns)
        max_len_type = max(len(str(type_name)) for type_name in data_rows.types)

        lines = [f'---- Start {script_name} \r\n']
        for row_no, data_row in enumerate(data_rows.data, start=1):
            lines.append(f'---- Result Set {result_set_index} Row {row_no} \r\n')
            for col_index, value in enumerate(data_row):
                column_name = str(data_rows.columns[col_index]).ljust(max_len_column)
                type_name = str(data_rows.types[col_index]).ljust(max_len_type)
                lines.append(f'{column_name}  :  {type_name}  :  {value} \r\n')
        lines.append(f'---- End {script_name}  \r\n')
        lines.append(f'Result Set {result_set_index}, No. Of Rows : {len(data_rows.data)} \r\n')
        return ''.join(lines)

    @staticmethod
    def show_table_result_csv(data_rows: ResultSet) -> str:
        # Was hand-built with str(...) + ',' .join-style concatenation, which corrupts
        # any field containing a comma, quote, or newline. csv.writer quotes correctly.
        if not data_rows.data:
            return ''
        buffer = io.StringIO()
        writer = csv.writer(buffer, lineterminator='\r\n')
        writer.writerow(data_rows.columns)
        writer.writerows(data_rows.data)
        return buffer.getvalue()

    @staticmethod
    def handle_general_exceptions(method_name: str, exception: Exception) -> None:
        print(f'SqlOperations Method : {method_name}')
        print('ex : ', exception)
        tb = traceback.TracebackException.from_exception(exception)
        print(''.join(tb.stack.format()))
