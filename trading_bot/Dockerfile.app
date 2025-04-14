FROM python:3.11.10-slim-bookworm

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

ENV QUESTDB_HOST questdb 

CMD ["python", "app.py"]

