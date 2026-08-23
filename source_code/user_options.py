from __future__ import annotations

import logging
from functools import wraps
from typing import Callable, ParamSpec, TypeAlias, TypeVar

import questionary
from sqlalchemy.engine import URL

from source_code.database_config import DatabaseConfig
from source_code.database_operations import DatabaseOperations
from source_code.file_operations import FileOperations


DatabaseConfigType: TypeAlias = dict[str, str | URL]

P = ParamSpec("P")
T = TypeVar("T")

logger = logging.getLogger(__name__)


def handle_errors(default: T) -> Callable[
    [Callable[P, T]],
    Callable[P, T],
]:
    """Convert unexpected exceptions into a logged default result."""

    def decorator(func: Callable[P, T]) -> Callable[P, T]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            try:
                return func(*args, **kwargs)
            except Exception:
                logger.exception(
                    "UserOptions method '%s' failed",
                    func.__name__,
                )
                return default

        return wrapper

    return decorator


class UserOptions:
    """Handle interactive user input and selection."""

    ABORT = "> Abort execution"
    DATABASE_SELECTION = "> Database selection"
    PARENT_DIRECTORY = "> .."
    SEARCH_AGAIN = "Search again"

    YES = "Yes"
    NO = "No"

    SCRIPT_OUTPUT_OPTIONS = (
        "abort",
        "insert",
        "insertAdd",
        "insertPk",
        "update",
        "update and insert",
        "csharp",
        "csharpV2",
    )

    RESULT_FORMATS = (
        "Rows",
        "Columns",
        "CSV",
    )

    def __init__(
        self,
        database_operations: DatabaseOperations | None = None,
        file_operations: FileOperations | None = None,
        database_config: DatabaseConfig | None = None,
    ) -> None:
        self.database_operations = (
            database_operations
            if database_operations is not None
            else DatabaseOperations()
        )

        self.file_operations = (
            file_operations
            if file_operations is not None
            else FileOperations()
        )

        self.database_config = (
            database_config
            if database_config is not None
            else DatabaseConfig()
        )

    # ------------------------------------------------------------------
    # Prompt helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _select(
        message: str,
        choices: list[str] | tuple[str, ...],
    ) -> str | None:
        """Display a selection prompt and return the selected value."""
        return questionary.select(
            message,
            choices=choices,
        ).ask()

    @staticmethod
    def _checkbox(
        message: str,
        choices: list[str] | tuple[str, ...],
    ) -> list[str] | None:
        """Display a checkbox prompt and return selected values."""
        return questionary.checkbox(
            message,
            choices=choices,
        ).ask()

    @staticmethod
    def _confirm(message: str) -> bool | None:
        """Display a confirmation prompt."""
        return questionary.confirm(message).ask()

    # ------------------------------------------------------------------
    # Database selection
    # ------------------------------------------------------------------

    @handle_errors(default=None)
    def get_database_options(self) -> str | None:
        """Prompt the user to select a database."""
        return self.get_database_name()

    @handle_errors(default=None)
    def get_database_name(self) -> str | None:
        """Select a single database."""
        database_names = self.database_operations.get_database()

        return self._select(
            "Select a database",
            database_names,
        )

    @handle_errors(default=[])
    def get_database_names(self) -> list[str]:
        """Select multiple databases."""
        database_names = self.database_operations.get_database()

        return self._checkbox(
            "Select databases",
            database_names,
        ) or []

    @handle_errors(default=None)
    def get_database_config(self) -> DatabaseConfigType | None:
        """Prompt the user to select a database configuration."""
        config_names = (
            self.database_config.get_connection_config_names()
        )

        selected_config = self._select(
            "Select a database configuration",
            config_names,
        )

        if selected_config is None:
            return None

        return self.database_config.get_connection(
            selected_config
        )

    @handle_errors(default=None)
    def get_database_config_via_name(
        self,
        db_name: str,
    ) -> DatabaseConfigType | None:
        """Get a database configuration by name."""
        return self.database_config.get_connection(db_name)

    # ------------------------------------------------------------------
    # File selection
    # ------------------------------------------------------------------

    @handle_errors(default=None)
    def get_files_in_directory(
        self,
        file_path: str,
    ) -> str | None:
        """Display files and directory navigation options."""
        files = self.file_operations.get_files_in_directory(
            file_path
        )

        choices = (
            *files,
            self.DATABASE_SELECTION,
            self.PARENT_DIRECTORY,
            self.ABORT,
        )

        return self._select(
            "Select a file to execute",
            choices,
        )

    # ------------------------------------------------------------------
    # Table selection
    # ------------------------------------------------------------------

    @handle_errors(default=None)
    def search_table_name(
        self,
        database_config: DatabaseConfigType,
        search_term: str,
    ) -> str | None:
        """Search for a table and allow the user to select one."""
        table_names = self.database_operations.search_table_name(
            database_config,
            search_term,
        )

        return self._select(
            "Select a table",
            (
                *table_names,
                self.SEARCH_AGAIN,
            ),
        )

    # ------------------------------------------------------------------
    # Yes / No
    # ------------------------------------------------------------------

    @handle_errors(default=False)
    def get_yes_no_question(self, question: str) -> bool:
        """Ask the user a Yes/No question."""
        return self._confirm(question) is True

    # ------------------------------------------------------------------
    # Script options
    # ------------------------------------------------------------------

    @handle_errors(default=None)
    def get_script_output_options(self) -> str | None:
        """Select the type of script/output to generate."""
        return self._select(
            "Select an option",
            self.SCRIPT_OUTPUT_OPTIONS,
        )

    # ------------------------------------------------------------------
    # Result formatting
    # ------------------------------------------------------------------

    @handle_errors(default=None)
    def select_row_or_columns_result(self) -> str | None:
        """Select the format for displaying SQL results."""
        return self._select(
            "Select a result format",
            self.RESULT_FORMATS,
        )