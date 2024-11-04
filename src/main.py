import logging

from pydantic import ValidationError

from app.services import S3Service, Compress7zService, LogService
from app.settings import S3Settings, LogsSettings
from app.workers import LogAdminWorker


def main():
    logging.basicConfig(
        level=logging.INFO
    )

    try:
        s3_settings = S3Settings()
        logs_settings = LogsSettings()
    except ValidationError as e:
        logging.error(f"Envs not provided! {e}")
        return

    s3_service = S3Service(
        access_key=s3_settings.s3_access_key,
        secret_key=s3_settings.s3_secret_key,
        endpoint_url=s3_settings.endpoint_url
    )
    logs_service = LogService(
        absolute_path_to_logs_dir=logs_settings.logs_folder,
        log_files_extensions=logs_settings.log_file_extensions
    )
    compress_service = Compress7zService(
        absolute_path_to_logs_dir=logs_settings.logs_folder
    )

    worker = LogAdminWorker(
        logs_service=logs_service,
        s3_service=s3_service,
        compress_service=compress_service,
        time_to_log_file_live_in_seconds=logs_settings.time_to_live_log_archives_in_seconds,
        max_log_file_size=logs_settings.max_log_file_size_in_bytes,
        time_format="%d:%m:%Y_%H:%M:%S"
    )
    worker.run()


if __name__ == "__main__":
    main()
