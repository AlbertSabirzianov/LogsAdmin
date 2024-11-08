import datetime
import io
import logging
import time

from botocore.exceptions import ClientError

from app.interfaces import WorkerInterface, S3Interface, LogInterface, CompressInterface


class LogAdminWorker(WorkerInterface):

    def __init__(
        self,
        logs_service: LogInterface,
        s3_service: S3Interface,
        compress_service: CompressInterface,
        time_to_log_file_live_in_seconds: int,
        max_log_file_size: int,
        time_format: str,
        delay_time_in_seconds: int
    ):
        self.logs_service: LogInterface = logs_service
        self.s3_service: S3Interface = s3_service
        self.compress_service: CompressInterface = compress_service
        self.time_to_log_file_live_in_seconds: int = time_to_log_file_live_in_seconds
        self.max_log_file_size: int = max_log_file_size
        self.time_format: str = time_format
        self.delay_time_in_seconds: int = delay_time_in_seconds

    def get_s3_file_name_from_log_name(self, log_name: str) -> str:
        return f"{log_name}_{datetime.datetime.now().strftime(self.time_format)}{self.compress_service.archive_format}"

    def is_s3_file_too_old(self, last_modified: datetime.datetime) -> bool:
        delta = datetime.timedelta(seconds=self.time_to_log_file_live_in_seconds)
        if last_modified < datetime.datetime.now() - delta:
            return True
        return False

    def clean_logs(self) -> None:
        for name in self.logs_service.get_all_log_files():
            size = self.logs_service.get_log_file_size(name)
            logging.info(f"{name} - size {size}")
            if size > self.max_log_file_size:
                archive: io.BytesIO = self.compress_service.compress_file(
                    name
                )
                try:
                    self.s3_service.upload(
                        bucket_name=name,
                        file_name=self.get_s3_file_name_from_log_name(name),
                        file=archive
                    )
                except ClientError as e:
                    logging.error(f"Can't upload file {name} - {e}")
                    continue
                self.logs_service.clean_log_file(name)

    def clean_s3_archives(self):
        for bucket_name in self.logs_service.get_all_log_files():
            s3_files = self.s3_service.get_all_files(bucket_name)
            for file in s3_files:
                last_m: datetime.datetime = self.s3_service.last_modified(bucket_name, file)
                if self.is_s3_file_too_old(last_m):
                    self.s3_service.delete_file(
                        bucket_name,
                        file
                    )

    def run(self) -> None:
        while True:
            try:
                logging.info("Start logs admin")
                self.clean_logs()
                self.clean_s3_archives()
            except Exception as err:
                logging.error(f"Cant clean log files {err}")
                break
            else:
                logging.info("End Admin")
                time.sleep(self.delay_time_in_seconds)




