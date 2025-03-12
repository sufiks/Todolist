FROM python:3.14.0a5-slim-bullseye
WORKDIR /opt/todolist

ENV PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_NO_CACHE_DIR=off \
    PYTHONPATH=/opt/todolist

RUN apt-get update && apt-get install -y \
    gcc \
    libffi-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install "poetry"
RUN poetry --version
RUN groupadd --system service && useradd --system -g service api

COPY poetry.lock pyproject.toml ./
RUN poetry config virtualenvs.create false \
    && poetry install --no-ansi --no-root

COPY todolist/ ./
COPY entrypoint.sh ./entrypoint.sh

RUN chmod +x entrypoint.sh  # Обеспечьте права на выполнение скрипта

USER api
ENTRYPOINT ["bash", "entrypoint.sh"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

EXPOSE 8000

