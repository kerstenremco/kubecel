FROM python:3.12

RUN curl -sSL https://install.python-poetry.org | python3 -
RUN mkdir /app
COPY ../ /app
WORKDIR /app
RUN /root/.local/bin/poetry install
WORKDIR /app

CMD /root/.local/bin/poetry run celery -A worker.tasks worker --concurrency=1 --loglevel=info