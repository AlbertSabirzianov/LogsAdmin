import datetime
import io
import logging
import os

import boto3
import py7zr
from botocore.exceptions import ClientError

from app.interfaces import LogInterface, S3Interface, CompressInterface


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


class Compress7zService(CompressInterface):

    @property
    def archive_format(self) -> str:
        return ".7z"

    def __init__(
        self,
        absolute_path_to_logs_dir: str
    ):
        self.absolute_path_to_logs_dir: str = absolute_path_to_logs_dir

    def get_file_path(self, log_file_name: str) -> str:
        return os.path.join(
            self.absolute_path_to_logs_dir,
            log_file_name
        )

    def compress_file(self, log_file_name: str) -> io.BytesIO:
        byte_io = io.BytesIO()
        with py7zr.SevenZipFile(byte_io, 'w') as archive:
            archive.write(
                self.get_file_path(log_file_name)
            )
        byte_io.seek(0)
        return byte_io


class S3Service(S3Interface):

    def __init__(self, access_key: str, secret_key: str, endpoint_url: str):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            endpoint_url=endpoint_url
        )

    def create_bucket_if_not_exists(self, bucket_name: str) -> None:
        try:
            self.s3_client.head_bucket(Bucket=bucket_name)
            logging.info(f"Bucket {bucket_name} already exists")
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                self.s3_client.create_bucket(Bucket=bucket_name)
                logging.info(f"Bucket {bucket_name} created")

    def upload(self, bucket_name: str, file_name: str, file: io.BytesIO) -> None:
        self.create_bucket_if_not_exists(bucket_name)
        self.s3_client.upload_fileobj(file, bucket_name, file_name)
        logging.info(f"File {file_name} uploaded to bucket {bucket_name}.")

    def get_all_files(self, bucket_name: str) -> list[str]:
        self.create_bucket_if_not_exists(bucket_name)
        response = self.s3_client.list_objects_v2(Bucket=bucket_name)
        if 'Contents' in response:
            return [obj['Key'] for obj in response['Contents']]
        else:
            return []

    def delete_file(self, bucket_name: str, file_name: str) -> None:
        self.create_bucket_if_not_exists(bucket_name)
        self.s3_client.delete_object(Bucket=bucket_name, Key=file_name)
        logging.info(f"File {file_name} deleted from bucket {bucket_name}.")

    def last_modified(self, bucket_name: str, file_name: str) -> datetime.datetime:
        self.create_bucket_if_not_exists(bucket_name)
        response = self.s3_client.head_object(Bucket=bucket_name, Key=file_name)
        return response['LastModified'].replace(tzinfo=None)

