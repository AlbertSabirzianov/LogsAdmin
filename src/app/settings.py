from pydantic_settings import BaseSettings


class S3Settings(BaseSettings):
    s3_host: str
    s3_port: int
    s3_access_key: str
    s3_secret_key: str

    @property
    def endpoint_url(self) -> str:
        return f"http://{self.s3_host}:{self.s3_port}"


class LogsSettings(BaseSettings):
    logs_folder: str = "/logs"
    log_file_extensions: list[str] = [".log"]
    max_log_file_size_in_bytes: int
    time_to_live_log_archives_in_seconds: int


class WorkerSettings(BaseSettings):
    delay_time_in_seconds: int = 1
    is_testing: bool = False


