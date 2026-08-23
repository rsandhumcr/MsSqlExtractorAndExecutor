import argparse
from pathlib import Path

import questionary

from source_code.database_config import DatabaseConfig
from source_code.database_operations import DatabaseOperations
from source_code.file_operations import FileOperations
from source_code.script_generator import ScriptGenerator
from source_code.sql_operations import SqlOperations
from source_code.user_options import UserOptions


DEFAULT_OUTPUT_FILE = Path("output/testfile.sql")
SEARCH_AGAIN = "Search again"
ABORT = "abort"
EXTRACT_ANOTHER = "extract another"


class DataExtractor:
    def __init__(self) -> None:
        self.database_operations = DatabaseOperations()
        self.file_operations = FileOperations()
        self.script_generator = ScriptGenerator()
        self.sql_operations = SqlOperations()
        self.user_options = UserOptions()
        self.database_config = DatabaseConfig()

    def extract_interactively(self) -> None:
        """Run the interactive data extraction workflow."""
        db_config = self.user_options.get_database_config()
        table_name = self._select_table(db_config)

        if not table_name:
            return

        table_info = (
            self.database_operations.get_table_meta_data_simple_string(db_config, table_name)
        )

        has_relationships = self.sql_operations.print_table_info(table_name, table_info)

        where_clause = input(f"Where clause for table {table_name} "
            "(not including WHERE keyword)? ")

        include_relationships = self._should_include_relationships(has_relationships, where_clause)

        selected_option = self.user_options.get_script_output_options()

        if selected_option == ABORT:
            return

        self.sql_operations.extract_table_data(str(DEFAULT_OUTPUT_FILE), db_config,
            table_name, where_clause, selected_option, include_relationships, [])

    def _select_table(self, db_config) -> str | None:
        """Prompt the user until a valid table is selected."""
        while True:
            search_term = input("Enter search term for database table name? ")

            table_name = self.user_options.search_table_name(db_config, search_term)

            if table_name != SEARCH_AGAIN:
                return table_name

    def _should_include_relationships(self, has_relationships: bool, where_clause: str) -> bool:
        """Ask whether related table data should be included."""
        if not has_relationships or not where_clause:
            return False

        return self.user_options.get_yes_no_question(
            "Do you want related tables data?"
        )

    def run_interactive(self) -> None:
        """Run the interactive extraction menu."""
        self.extract_interactively()
        while True:
            option = questionary.select(
                "Select an option",
                choices=[EXTRACT_ANOTHER, ABORT],
            ).ask()

            if option == ABORT:
                return

            if option == EXTRACT_ANOTHER:
                self.extract_interactively()

    def extract_from_command_line(self, db_name: str, table_name: str,
        where_clause: str, output_option: str, include_relationships: bool, output_file: Path) -> None:
        """Extract table data using command-line arguments."""
        db_config = self.user_options.get_database_config_via_name(
            db_name
        )

        if not self._validate_table(db_config, table_name):
            return

        self.sql_operations.extract_table_data(str(output_file), db_config, table_name,
            where_clause, output_option, include_relationships,[])

        print(f"Output file: {output_file}")

    def show_table_info(self, db_name: str, table_name: str) -> None:
        """Display metadata for a database table."""
        db_config = self.user_options.get_database_config_via_name(db_name)

        table_name = self._add_default_schema(table_name)

        if not self._validate_table(db_config, table_name):
            return

        table_info = (
            self.database_operations.get_table_meta_data_simple_string(db_config, table_name)
        )

        self.sql_operations.print_table_info(table_name,  table_info)

    def _validate_table(self, db_config, table_name: str) -> bool:
        """Validate that a database table exists."""
        return self.sql_operations.check_database_table_names(
            db_config,
            table_name,
        )

    @staticmethod
    def _add_default_schema(table_name: str) -> str:
        """Add dbo schema if no schema was provided."""
        if "." not in table_name:
            return f"dbo.{table_name}"

        return table_name


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Extract database table data or display table information.")

    subparsers = parser.add_subparsers(dest="command", required=False)

    extract_parser = subparsers.add_parser("extract", help="Extract data from a database table.")

    extract_parser.add_argument("database", help="Database name.")

    extract_parser.add_argument("table", help="Table name, including schema.")

    extract_parser.add_argument("where", help="WHERE clause without the WHERE keyword.")

    extract_parser.add_argument("output_option",  choices=["insert", "update", "insert and update"],
        help="Type of SQL script to generate.")

    extract_parser.add_argument("include_relationships",  type=parse_boolean,
        help="Include related table data: True or False.")

    extract_parser.add_argument( "-o", "--output", type=Path,
        default=DEFAULT_OUTPUT_FILE, help=f"Output file. Default: {DEFAULT_OUTPUT_FILE}")

    info_parser = subparsers.add_parser("info", help="Show table information.")

    info_parser.add_argument("database", help="Database name.")

    info_parser.add_argument("table", help="Table name.")

    return parser


def parse_boolean(value: str) -> bool:
    """Convert common string representations to a boolean."""
    normalized = value.lower()

    if normalized in {"true", "yes", "1"}:
        return True

    if normalized in {"false", "no", "0"}:
        return False

    raise argparse.ArgumentTypeError(f"Invalid boolean value: {value}. "
        "Use True/False, Yes/No, or 1/0."
    )


def main() -> None:
    extractor = DataExtractor()
    parser = create_parser()
    args = parser.parse_args()

    if args.command is None:
        extractor.run_interactive()
        return

    if args.command == "extract":
        extractor.extract_from_command_line(db_name=args.database, table_name=args.table, where_clause=args.where,
            output_option=args.output_option, include_relationships=args.include_relationships,
            output_file=args.output)
        return

    if args.command == "info":
        extractor.show_table_info(db_name=args.database, table_name=args.table)

if __name__ == "__main__":
    main()