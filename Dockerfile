FROM python:3.10-slim-bullseye
WORKDIR /app
COPY requirements.txt requirements.txt
RUN ["pip", "install", "-r", "requirements.txt"]
COPY bot /app
ENTRYPOINT ["sh", "-c", "pybabel compile -d locales -D bot && wait-for-it -s $DB_ADDRESS:3306 -- echo 'Database is up' && python main.py"]