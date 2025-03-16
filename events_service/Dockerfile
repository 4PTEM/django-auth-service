FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --no-cache-dir poetry

WORKDIR /app

COPY poetry.lock pyproject.toml /app/

COPY . /app/

RUN poetry install --no-interaction --no-ansi

EXPOSE 80

CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:80", "--noreload"]
