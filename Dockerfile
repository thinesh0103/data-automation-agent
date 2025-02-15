FROM python:3.10

RUN apt update && apt install -y curl && \
    curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt install -y nodejs

RUN node -v && npm -v

RUN npm install -g prettier@3.4.2

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir fastapi uvicorn

RUN pip install --no-cache-dir fastapi uvicorn openai requests pillow pandas json5 duckdb markdown-it-py pydantic aiofiles beautifulsoup4 markdown2 faker

ADD https://raw.githubusercontent.com/sanand0/tools-in-data-science-public/tds-2025-01/project-1/datagen.py /app/datagen.py

RUN python /app/datagen.py 23f2002954@ds.study.iitm.ac.in

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
