import datetime
import io
from abc import ABC, abstractmethod


class S3Interface(ABC):

    @abstractmethod
    def upload(self, bucket_name: str, file_name: str, file: io.BytesIO) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_all_files(self, bucket_name: str) -> list[str]:
        raise NotImplementedError

    @abstractmethod
    def delete_file(self, bucket_name: str, file_name: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def last_modified(self, bucket_name: str, file_name: str) -> datetime.datetime:
        raise NotImplementedError


class LogInterface(ABC):

    @abstractmethod
    def get_all_log_files(self) -> list[str]:
        raise NotImplementedError

    @abstractmethod
    def get_log_file_size(self, file_name: str) -> int:
        raise NotImplementedError

    @abstractmethod
    def get_log_file_data(self, file_name: str) -> io.BytesIO:
        raise NotImplementedError

    @abstractmethod
    def clean_log_file(self, file_name: str) -> None:
        raise NotImplementedError


class WorkerInterface(ABC):

    @abstractmethod
    def run(self):
        raise NotImplementedError
