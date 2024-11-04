# LogsAdmin
A service that monitors the size of log files in folder(LOGS_DIR in env variable) and, when exceeding the limits,
saves compressed files to s3 storage and clears log files. 
The storage period of compressed archives is configured via environment variable TIME_TO_LIVE_LOG_ARCHIVES_IN_SECONDS.
Log files by default are files with the ".log" extension that are located in the specified directory,
extensions that are taken as log files can be configured using a variable LOG_FILE_EXTENSIONS 
(in default LOG_FILE_EXTENSIONS=[".log"])
# how to run
you can include LogsAdmin in your docker-compose like this
```yaml
services:
  log_archiver:
    image: albertsabirzianov/logs_archiver:latest
    volumes:
      - ${LOGS_DIR}:/logs
    environment:
      - S3_HOST=${S3_HOST}
      - S3_PORT=${S3_PORT}
      - S3_ACCESS_KEY=${S3_ACCESS_KEY}
      - S3_SECRET_KEY=${S3_SECRET_KEY}
      - MAX_LOG_FILE_SIZE_IN_BYTES=${MAX_LOG_FILE_SIZE_IN_BYTES}
      - TIME_TO_LIVE_LOG_ARCHIVES_IN_SECONDS=${TIME_TO_LIVE_LOG_ARCHIVES_IN_SECONDS}
```
Values of environment variables
```text
LOGS_DIR=./logs # path to your directory with log files
# S3 values 
S3_HOST=minio  
S3_PORT=9000 
S3_ACCESS_KEY=S3_ACCESS_KEY 
S3_SECRET_KEY=S3_SECRET_KEY

MAX_LOG_FILE_SIZE_IN_BYTES=5 # max log size in bytes
TIME_TO_LIVE_LOG_ARCHIVES_IN_SECONDS=10 # time to archive live in seconds
```
If necessary, you can also specify additional variables
```text
LOG_FILE_EXTENSIONS=[".log"] # list of extensions that LogsAdmin monitor
```