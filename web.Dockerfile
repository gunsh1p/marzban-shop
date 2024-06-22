FROM python:3.10-slim-bullseye
WORKDIR /app
COPY requirements.txt requirements.txt
RUN ["pip", "install", "-r", "requirements.txt"]
COPY app /app
COPY migrations /app/migrations
COPY db /app/db
COPY utils /app/utils
COPY constants /app/constants
COPY pyproject.toml /app/pyproject.toml
ENTRYPOINT ["bash", "-c", "aerich upgrade; uvicorn main:get_app --host 0.0.0.0 --port 8080"]