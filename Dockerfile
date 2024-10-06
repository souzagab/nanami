FROM python:3.12-slim

WORKDIR /nanami

RUN pip install --no-cache-dir poetry

COPY pyproject.toml poetry.lock gunicorn.conf.py /nanami/

RUN poetry config virtualenvs.create false \
  && poetry install --no-root --no-interaction --no-ansi


COPY . /nanami/

CMD ["gunicorn", "app.main:app", "-c", "gunicorn.conf.py"]
