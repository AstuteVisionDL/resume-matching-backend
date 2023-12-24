FROM python:3.10-bullseye
WORKDIR /app
RUN pip install poetry
ADD poetry.lock .
ADD pyproject.toml .
RUN poetry install
COPY /src ./src