from __future__ import annotations

import logging
from typing import TypeAlias

import questionary
from sqlalchemy.engine import URL

from source_code.database_config import DatabaseConfig
from source_code.database_operations import DatabaseOperations
from source_code.file_operations import FileOperations


DatabaseConfigType: TypeAlias = dict[str, str | URL]

logger = logging.getLogger(__name__)


class UserOptions:
    """Handles interactive user input and selection."""

    ABORT = "> Abort execution"
    DATABASE_SELECTION = "> Database selection"
    PARENT_DIRECTORY = "> .."
    SEARCH_AGAIN = "Search again"

    YES = "Yes"
    NO = "No"

    def __init__(
        self,
        database_operations: DatabaseOperations | None = None,
        file_operations: FileOperations | None = None,
        database_config: DatabaseConfig | None = None,
    ) -> None:
        self.database_operations = (
            database_operations
            or DatabaseOperations()
        )

        self.file_operations = (
            file_operations
            or FileOperations()
        )

        self.database_config = (
            database_config
            or DatabaseConfig()
        )

    # ------------------------------------------------------------------
    # General selection helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _select(
        message: str,
        choices: list[str],
    ) -> str | None:
        """Display a selection prompt and return the selected value."""

        return questionary.select(
            message,
            choices=choices,
        ).ask()

    @staticmethod
    def _checkbox(
        message: str,
        choices: list[str],
    ) -> list[str] | None:
        """Display a checkbox prompt and return selected values."""

        return questionary.checkbox(
            message,
            choices=choices,
        ).ask()

    # ------------------------------------------------------------------
    # Database selection
    # ------------------------------------------------------------------

    def get_database_options(self) -> str | None:
        """Prompt the user to select a database."""

        return self.get_database_name()

    def get_database_name(self) -> str | None:
        """Select a database from the available databases."""

        try:
            database_names = self.database_operations.get_database()

            return self._select(
                "Select a database",
                database_names,
            )

        except Exception as exc:
            self.handle_general_exception(
                "get_database_name",
                exc,
            )
            return None

    def get_database_names(self) -> list[str]:
        """Allow the user to select multiple databases."""

        try:
            database_names = self.database_operations.get_database()

            selected = self._checkbox(
                "Select databases",
                database_names,
            )

            return selected or []

        except Exception as exc:
            self.handle_general_exception(
                "get_database_names",
                exc,
            )
            return []

    def get_database_config(
        self,
    ) -> DatabaseConfigType | None:
        """Prompt the user to select a database configuration."""

        try:
            config_names = (
                self.database_config
                .get_connection_config_names()
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

        except Exception as exc:
            self.handle_general_exception(
                "get_database_config",
                exc,
            )
            return None

    def get_database_config_via_name(
        self,
        db_name: str,
    ) -> DatabaseConfigType | None:
        """Get a database configuration by its name."""

        try:
            return self.database_config.get_connection(
                db_name
            )

        except Exception as exc:
            self.handle_general_exception(
                "get_database_config_via_name",
                exc,
            )
            return None

    # ------------------------------------------------------------------
    # File selection
    # ------------------------------------------------------------------

    def get_files_in_directory(
        self,
        file_path: str,
    ) -> str | None:
        """Display files and navigation options for a directory."""

        try:
            files = self.file_operations.get_files_in_directory(
                file_path
            )

            choices = [
                *files,
                self.DATABASE_SELECTION,
                self.PARENT_DIRECTORY,
                self.ABORT,
            ]

            return self._select(
                "Select a file to execute",
                choices,
            )

        except Exception as exc:
            self.handle_general_exception(
                "get_files_in_directory",
                exc,
            )
            return None

    # ------------------------------------------------------------------
    # Table selection
    # ------------------------------------------------------------------

    def search_table_name(
        self,
        database_config: DatabaseConfigType,
        search_term: str,
    ) -> str | None:
        """Search for a table and allow the user to select one."""

        try:
            table_names = (
                self.database_operations.search_table_name(
                    database_config,
                    search_term,
                )
            )

            choices = [
                *table_names,
                self.SEARCH_AGAIN,
            ]

            return self._select(
                "Select a table",
                choices,
            )

        except Exception as exc:
            self.handle_general_exception(
                "search_table_name",
                exc,
            )
            return None

    # ------------------------------------------------------------------
    # Yes / No
    # ------------------------------------------------------------------

    def get_yes_no_question(
        self,
        question: str,
    ) -> bool:
        """Ask the user a Yes/No question."""

        try:
            answer = self._select(
                question,
                [self.YES, self.NO],
            )

            return answer == self.YES

        except Exception as exc:
            self.handle_general_exception(
                "get_yes_no_question",
                exc,
            )
            return False

    # ------------------------------------------------------------------
    # Script options
    # ------------------------------------------------------------------

    def get_script_output_options(self) -> str | None:
        """Select the type of script/output to generate."""

        options = [
            "abort",
            "insert",
            "insertAdd",
            "insertPk",
            "update",
            "update and insert",
            "csharp",
            "csharpV2",
        ]

        try:
            return self._select(
                "Select an option",
                options,
            )

        except Exception as exc:
            self.handle_general_exception(
                "get_script_output_options",
                exc,
            )
            return None

    # ------------------------------------------------------------------
    # Result formatting
    # ------------------------------------------------------------------

    def select_row_or_columns_result(self) -> str | None:
        """Select the format for displaying SQL results."""

        try:
            return self._select(
                "Select a result format",
                [
                    "Rows",
                    "Columns",
                    "CSV",
                ],
            )

        except Exception as exc:
            self.handle_general_exception(
                "select_row_or_columns_result",
                exc,
            )
            return None

    # ------------------------------------------------------------------
    # Error handling
    # ------------------------------------------------------------------

    @staticmethod
    def handle_general_exception(
        method_name: str,
        exception: Exception,
    ) -> None:
        """Log an unexpected exception."""

        logger.exception(
            "UserOptions method '%s' failed",
            method_name,
            exc_info=exception,
        )