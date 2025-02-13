FROM python:3.9

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir fastapi uvicorn openai requests pillow pandas sqlite3 json5 duckdb markdown-it-py pydantic aiofiles

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
