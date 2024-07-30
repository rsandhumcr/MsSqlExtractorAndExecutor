import os
import traceback


class FileOperations:
    def write_to_file(self, path_file: str, string_data: str) -> None:
        try:
            text_file = open(path_file, "a")
            text_file.write(string_data)
            text_file.close()
        except Exception as exc:
            self.handle_general_exceptions('write_to_file', exc)

    def read_file(self, path_file: str) -> str:
        try:
            text_file = open(path_file, "r")
            file_data = text_file.read()
            text_file.close()
            return file_data

        except Exception as exc:
            self.handle_general_exceptions('read_file', exc)

    def get_files_in_directory(self, file_path: str) -> list[str]:
        try:
            return os.listdir(file_path)
        except Exception as exc:
            self.handle_general_exceptions('get_files_in_directory', exc)

    def is_directory(self, file_path, directory_name: str) -> bool:
        try:
            return os.path.isdir(f'{file_path}\\{directory_name}')
        except Exception as exc:
            self.handle_general_exceptions('is_directory', exc)

    def get_parent_directory(self, file_path: str) -> tuple[str] | str:
        try:
            head, tail = os.path.split(file_path)
            return head
        except Exception as exc:
            self.handle_general_exceptions('get_parent_directory', exc)

    @staticmethod
    def handle_general_exceptions(method_name: str, exception: Exception) -> None:
        print(f'FileOperations Method : {method_name}')
        print('ex : ', exception)
        tb = traceback.TracebackException.from_exception(exception)
        print(''.join(tb.stack.format()))
