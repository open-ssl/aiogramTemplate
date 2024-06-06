FROM python:3.11-alpine

WORKDIR /usr/aiogramTemplate

ENV PATH="/root/.local/bin:${PATH}"
ENV POETRY_VERSION=1.8.2

COPY pyproject.toml .
COPY poetry.lock .

RUN curl -sSL https://install.python-poetry.org | python3 - --version ${POETRY_VERSION}\
    && poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

COPY src .

RUN chmod +x src/bot

ENV PYTHONPATH="${PYTHONPATH}:/usr/aiogramTemplate/src"

CMD ["poetry", "run", "python", "src/bot/main.py"]
