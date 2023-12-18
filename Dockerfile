FROM python:3.10-alpine
WORKDIR /app
RUN pip install poetry
ADD poetry.lock .
ADD pyproject.toml .
RUN poetry install
COPY /src ./src