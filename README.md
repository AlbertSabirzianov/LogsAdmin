# LogsAdmin

**LogsAdmin** — это сервис, который отслеживает размер лог-файлов в указанной папке (путь задается переменной окружения `LOGS_DIR`). Когда размер лог-файлов превышает заданные пределы, сервис сохраняет сжатые файлы в хранилище S3 и очищает лог-файлы. Период хранения сжатых архивов настраивается через переменную окружения `TIME_TO_LIVE_LOG_ARCHIVES_IN_SECONDS`.

По умолчанию лог-файлы имеют расширение `.log` и находятся в указанной директории. Расширения, которые считаются лог-файлами, можно настроить с помощью переменной `LOG_FILE_EXTENSIONS` (по умолчанию `LOG_FILE_EXTENSIONS=[".log"]`).

## Как запустить

Вы можете включить LogsAdmin в ваш `docker-compose` следующим образом:

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
## Значения переменных окружения
```text
LOGS_DIR=./logs # путь к вашей директории с лог-файлами

# Значения для S3
S3_HOST=minio  
S3_PORT=9000 
S3_ACCESS_KEY=S3_ACCESS_KEY 
S3_SECRET_KEY=S3_SECRET_KEY

MAX_LOG_FILE_SIZE_IN_BYTES=5 # максимальный размер лог-файла в байтах
TIME_TO_LIVE_LOG_ARCHIVES_IN_SECONDS=10 # время хранения архивов в секундах
LOG_FILE_EXTENSIONS=[".log"] # список расширений, которые мониторит LogsAdmin
```

## Примечания

- Убедитесь, что все переменные окружения правильно настроены перед запуском сервиса.
- Для получения дополнительной информации о настройке S3, пожалуйста, обратитесь к документации вашего S3 провайдера.

---