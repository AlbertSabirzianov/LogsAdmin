import datetime
import io
from abc import ABC, abstractmethod, abstractproperty


class S3Interface(ABC):
    """Abstract base class for S3 operations."""

    @abstractmethod
    def upload(self, bucket_name: str, file_name: str, file: io.BytesIO) -> None:
        """Uploads a file to the specified S3 bucket.

        Args:
            bucket_name (str): The name of the S3 bucket.
            file_name (str): The name of the file to be uploaded.
            file (io.BytesIO): The file content as a BytesIO object.
        """
        raise NotImplementedError

    @abstractmethod
    def get_all_files(self, bucket_name: str) -> list[str]:
        """Retrieves a list of all files in the specified S3 bucket.

        Args:
            bucket_name (str): The name of the S3 bucket.

        Returns:
            list[str]: A list of file names in the bucket.
        """
        raise NotImplementedError

    @abstractmethod
    def delete_file(self, bucket_name: str, file_name: str) -> None:
        """Deletes a specified file from the S3 bucket.

        Args:
            bucket_name (str): The name of the S3 bucket.
            file_name (str): The name of the file to be deleted.
        """
        raise NotImplementedError

    @abstractmethod
    def last_modified(self, bucket_name: str, file_name: str) -> datetime.datetime:
        """Gets the last modified date of a specified file in the S3 bucket.

        Args:
            bucket_name (str): The name of the S3 bucket.
            file_name (str): The name of the file.

        Returns:
            datetime.datetime: The last modified date of the file.
        """
        raise NotImplementedError


class LogInterface(ABC):
    """Abstract base class for log file operations."""

    @abstractmethod
    def get_all_log_files(self) -> list[str]:
        """Retrieves a list of all log files.

        Returns:
            list[str]: A list of log file names.
        """
        raise NotImplementedError

    @abstractmethod
    def get_log_file_size(self, file_name: str) -> int:
        """Gets the size of a specified log file.

        Args:
            file_name (str): The name of the log file.

        Returns:
            int: The size of the log file in bytes.
        """
        raise NotImplementedError

    @abstractmethod
    def clean_log_file(self, file_name: str) -> None:
        """Cleans the specified log file.

        Args:
            file_name (str): The name of the log file to be cleaned.
        """
        raise NotImplementedError


class CompressInterface(ABC):
    """Abstract base class for file compression operations."""

    @abstractmethod
    def compress_file(self, log_file_name: str) -> io.BytesIO:
        """Compresses a specified log file.

        Args:
            log_file_name (str): The name of the log file to compress.

        Returns:
            io.BytesIO: The compressed file as a BytesIO object.
        """
        raise NotImplementedError

    @abstractproperty
    def archive_format(self) -> str:
        """Gets the format of the archive.

        Returns:
            str: The archive format (e.g., 'zip', 'tar').
        """
        raise NotImplementedError


class WorkerInterface(ABC):
    """Abstract base class for worker operations."""

    @abstractmethod
    def run(self):
        """Executes the worker's main functionality."""
        raise NotImplementedError