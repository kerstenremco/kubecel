FROM python:3.12

RUN curl -sSL https://install.python-poetry.org | python3 -
RUN mkdir /app
COPY ../ /app
WORKDIR /app
RUN /root/.local/bin/poetry install
EXPOSE 8000
CMD /root/.local/bin/poetry run fastapi run server.py