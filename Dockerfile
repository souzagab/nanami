FROM python:3.12-slim

WORKDIR /nanami

RUN pip install --no-cache-dir poetry

COPY pyproject.toml poetry.lock /nanami/

RUN poetry config virtualenvs.create false \
  && poetry install --no-root --no-interaction --no-ansi

EXPOSE 3000

COPY ./app /nanami/app

CMD ["sh", "-c", "gunicorn app.main:app \
  --workers ${WORKERS:-1} \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind ${BIND:-0.0.0.0:3000} \
  --timeout ${TIMEOUT:-120} \
  --keep-alive ${KEEP_ALIVE:-5} \
  --log-level ${LOG_LEVEL:-debug}"]
