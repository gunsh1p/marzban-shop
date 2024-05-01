FROM python:3.10-slim-bullseye
WORKDIR /app
COPY requirements.txt requirements.txt
RUN ["pip", "install", "-r", "requirements.txt"]
COPY bot /app
COPY migrations /app/migrations
COPY db /app/db
COPY utils /app/utils
COPY pyproject.toml /app/pyproject.toml
ENTRYPOINT ["bash", "-c", "aerich upgrade; python main.py"]