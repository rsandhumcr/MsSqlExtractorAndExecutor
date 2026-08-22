from __future__ import annotations

import sys
import argparse
from datetime import datetime
from pathlib import Path
from typing import Any

from sqlalchemy.engine import URL

from source_code.database_operations import DatabaseOperations
from source_code.file_operations import FileOperations
from source_code.parse_sql_parameters import ParseSqlParameters
from source_code.sql_operations import SqlOperations
from source_code.user_options import UserOptions


LIBRARY_PATH = Path("library")
OUTPUT_PATH = Path("output")
EXECUTION_OUTPUT_FILE = OUTPUT_PATH / "execution.txt"

ABORT_OPTION = "> Abort execution"
DATABASE_SELECTION_OPTION = "> Database selection"
PARENT_DIRECTORY_OPTION = "> .."

COLUMNS_OUTPUT = "Columns"
ROWS_OUTPUT = "Rows"
CSV_OUTPUT = "CSV"


# ---------------------------------------------------------------------------
# Dependencies
# ---------------------------------------------------------------------------

database_operations = DatabaseOperations()
file_operations = FileOperations()
sql_parameter_parser = ParseSqlParameters()
user_options = UserOptions()
sql_operations = SqlOperations()


# ---------------------------------------------------------------------------
# Timestamp helpers
# ---------------------------------------------------------------------------

def get_current_timestamp() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def get_file_timestamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


# ---------------------------------------------------------------------------
# Interactive execution
# ---------------------------------------------------------------------------

def execute_command_selection() -> None:
    db_config = user_options.get_database_config()

    if db_config is None:
        print_database_config_error()
        return

    current_path = LIBRARY_PATH

    while True:
        print(f"Database (name): {db_config['db_name']}")

        selected_file = user_options.get_files_in_directory(
            str(current_path)
        )

        if selected_file == ABORT_OPTION:
            return

        if selected_file == DATABASE_SELECTION_OPTION:
            db_config = user_options.get_database_config()

            if db_config is None:
                print_database_config_error()

            continue

        if selected_file == PARENT_DIRECTORY_OPTION:
            current_path = move_to_parent_directory(current_path)
            continue

        if file_operations.is_directory(
            str(current_path),
            selected_file,
        ):
            current_path /= selected_file

            print(
                f"==> Switching down to directory {current_path}"
            )

            continue

        execute_script_file(
            db_config=db_config,
            script_path=current_path / selected_file,
            selected_file=selected_file,
            specific_output_file=None,
        )


def move_to_parent_directory(current_path: Path) -> Path:
    """Move up one directory, without leaving the library directory."""

    if current_path == LIBRARY_PATH:
        return current_path

    parent_path = current_path.parent

    print(f"==> Switching up to directory {parent_path}")

    return parent_path


# ---------------------------------------------------------------------------
# Script execution
# ---------------------------------------------------------------------------

def execute_script_file(
    db_config: dict[str, str | URL],
    script_path: Path,
    selected_file: str,
    specific_output_file: Path | None,
) -> None:
    """Read, parse and execute a SQL script."""

    sql_script = file_operations.read_file(str(script_path))

    script_data = (
        sql_parameter_parser.replace_parameters_with_prompts(
            sql_script
        )
    )

    if script_data["return_results"]:
        execute_script_with_result(
            db_config=db_config,
            script_data=script_data,
            selected_file=selected_file,
            specific_output_file=specific_output_file,
        )
        return

    database_operations.execute_sql_script_no_data(
        db_config,
        script_data["sql_script"],
    )


def execute_script_with_result(
    db_config: dict[str, str | URL],
    script_data: dict[str, Any],
    selected_file: str,
    specific_output_file: Path | None,
) -> None:
    """Execute SQL and display/write the returned result sets."""

    result_sets = database_operations.execute_sql_script_raw_connection(
        db_config,
        script_data["sql_script"],
    )

    print_and_write(
        EXECUTION_OUTPUT_FILE,
        f"Db: {db_config['db_name']}",
    )

    if not result_sets:
        print_and_write(
            EXECUTION_OUTPUT_FILE,
            "No Data Returned",
        )
        return

    result_set_count = len(result_sets)

    print_result_summary(
        result_sets=result_sets,
        selected_file=selected_file,
        parameter_values=script_data["parameter_values"],
    )

    output_format = get_output_format(
        script_data,
        result_sets,
    )

    show_headers = not script_data["no_headers"]

    for result_number, result_set in enumerate(
        result_sets,
        start=1,
    ):
        if result_set_count > 1:
            print_and_write(
                EXECUTION_OUTPUT_FILE,
                f"Result set {result_number}",
            )

        result_output = format_result_set(
            output_format=output_format,
            result_number=result_number,
            selected_file=selected_file,
            result_set=result_set,
            show_headers=show_headers,
        )

        if result_output is None:
            continue

        if specific_output_file is not None:
            write_to_file(
                specific_output_file,
                result_output,
            )

        write_result_to_execution_log(result_output)


# ---------------------------------------------------------------------------
# Result handling
# ---------------------------------------------------------------------------

def print_result_summary(
    result_sets: list[dict[str, Any]],
    selected_file: str,
    parameter_values: str,
) -> None:
    """Print a summary of the returned result sets."""

    if len(result_sets) == 1:
        row_count = len(result_sets[0].data)

        output = (
            f"{selected_file}\n"
            f"You have {row_count} row(s)\n"
            f"{parameter_values}"
        )

        print_and_write(
            EXECUTION_OUTPUT_FILE,
            output,
        )

        return

    print_and_write(
        EXECUTION_OUTPUT_FILE,
        "You have:",
    )

    for result_number, result_set in enumerate(
        result_sets,
        start=1,
    ):
        row_count = len(result_set.data)
        column_count = len(result_set.columns)

        print_and_write(
            EXECUTION_OUTPUT_FILE,
            (
                f"   {row_count} row(s), "
                f"{column_count} column(s) "
                f"in result set {result_number}"
            ),
        )


def get_output_format(
    script_data: dict[str, Any],
    result_sets: list[dict[str, Any]],
) -> str:
    """Determine how SQL results should be displayed."""

    configured_format = script_data.get("result_in_columns")

    if configured_format is not None:
        return configured_format

    multiple_result_sets = len(result_sets) > 1
    multiple_rows = any(
        len(result_set.data) > 1
        for result_set in result_sets
    )

    if multiple_rows or multiple_result_sets:
        return user_options.select_row_or_columns_result()

    return COLUMNS_OUTPUT


def format_result_set(
    output_format: str,
    result_number: int,
    selected_file: str,
    result_set: dict[str, Any],
    show_headers: bool,
) -> str | None:
    """Format one result set."""

    match output_format:
        case "Columns":
            return sql_operations.show_table_result_columns(
                result_number,
                selected_file,
                result_set,
                show_headers,
            )

        case "Rows":
            return sql_operations.show_table_result_rows(
                result_number,
                result_set,
                show_headers,
            )

        case "CSV":
            return sql_operations.show_table_result_csv(
                result_set,
            )

        case _:
            # Safe fallback for unknown output formats.
            return sql_operations.show_table_result_csv(
                result_set,
            )


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

def write_result_to_execution_log(
    result_output: str,
) -> None:
    start_time = get_current_timestamp()

    output = (
        f"Start --- {start_time}\n\n"
        f"{result_output}\n\n"
        f"End --- {get_current_timestamp()}"
    )

    print_and_write(
        EXECUTION_OUTPUT_FILE,
        output,
    )


def write_to_file(
    file_path: Path | str,
    data: str,
) -> None:
    """Write data to a file using Windows line endings."""

    normalized_data = data.replace(
        "\r\n",
        "\n",
    ).replace(
        "\n",
        "\r\n",
    )

    file_operations.write_to_file(
        str(file_path),
        normalized_data,
    )


def print_and_write(
    file_path: Path | str,
    data: str,
) -> None:
    print(data)
    write_to_file(file_path, data)


# ---------------------------------------------------------------------------
# Command line execution
# ---------------------------------------------------------------------------

def execute_command_line(
    db_name: str,
    directory: str,
    script_name: str,
    output_file: str | None,
) -> None:
    db_config = user_options.get_database_config_via_name(
        db_name
    )

    if db_config is None:
        print_database_config_error()
        return

    specific_output_file = resolve_output_file(
        output_file
    )

    script_path = (
        LIBRARY_PATH
        / directory
        / script_name
    )

    execute_script_file(
        db_config=db_config,
        script_path=script_path,
        selected_file=script_name,
        specific_output_file=specific_output_file,
    )


def resolve_output_file(
    output_file: str | None,
) -> Path | None:
    """Resolve the optional output filename."""

    if not output_file:
        return None

    filename = output_file.replace(
        "TIMESTAMP",
        get_file_timestamp(),
    )

    return OUTPUT_PATH / filename


def create_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Execute SQL scripts from the library."
    )

    parser.add_argument(
        "database",
        help="Database configuration name.",
    )

    parser.add_argument(
        "directory",
        help="Directory within the library.",
    )

    parser.add_argument(
        "script",
        help="SQL script filename.",
    )

    parser.add_argument(
        "output_file",
        nargs="?",
        help=(
            "Optional output filename. "
            "Use TIMESTAMP to insert the current timestamp."
        ),
    )

    return parser


# ---------------------------------------------------------------------------
# Miscellaneous
# ---------------------------------------------------------------------------

def print_database_config_error() -> None:
    print(
        "There was an issue with the database configuration. "
        "Please check the configuration file and try again."
    )


def main() -> None:
    parser = create_argument_parser()

    if len(sys.argv) == 1:
        execute_command_selection()
        return

    args = parser.parse_args()

    execute_command_line(
        db_name=args.database,
        directory=args.directory,
        script_name=args.script,
        output_file=args.output_file,
    )


if __name__ == "__main__":
    main()