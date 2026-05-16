# 1. Базовый образ — лёгкий Python
FROM python:3.14-slim

# 2. Установить рабочую директорию внутри контейнера
WORKDIR /app

# 3. Скопировать файл парсера в контейнер
COPY test_httpx2.py .

# 4. Установить зависимости (httpx)
RUN pip install httpx sqlalchemy psycopg2-binary python-dotenv

# 5. Команда, которая выполнится при запуске контейнера
CMD ["python", "test_httpx2.py"]