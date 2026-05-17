FROM python:3.14-slim

WORKDIR /app

COPY test_httpx2.py .

RUN pip install httpx sqlalchemy psycopg2-binary python-dotenv

CMD ["python", "test_httpx2.py"]