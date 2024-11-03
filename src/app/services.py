import io
import os

from app.interfaces import LogInterface, S3Interface


class LogService(LogInterface):

    def __init__(
        self,
        absolute_path_to_logs_dir: str,
        log_files_extensions: list[str]
    ):
        self.absolute_path_to_logs_dir: str = absolute_path_to_logs_dir
        self.log_files_extensions: list[str] = log_files_extensions

    def get_all_log_files(self) -> list[str]:
        return [
            file for file in os.listdir(
                self.absolute_path_to_logs_dir
            ) if os.path.isfile(
                os.path.join(
                    self.absolute_path_to_logs_dir,
                    file
                )
            ) and file.endswith(tuple(self.log_files_extensions))
        ]

    def get_log_file_data(self, file_name: str) -> io.BytesIO:
        with open(
            os.path.join(
                self.absolute_path_to_logs_dir,
                file_name
            ),
            "rb"
        ) as file:
            return io.BytesIO(file.read())

    def clean_log_file(self, file_name: str) -> None:
        with open(
            os.path.join(
                self.absolute_path_to_logs_dir,
                file_name
            ),
            "w"
        ) as _:
            pass

    def get_log_file_size(self, file_name: str) -> int:
        return os.path.getsize(
            os.path.join(
                self.absolute_path_to_logs_dir,
                file_name
            )
        )
