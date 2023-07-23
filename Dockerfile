FROM python:3

WORKDIR /messenger

COPY poetry.lock pyproject.toml /messenger/

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-root

COPY . /messenger/

RUN chmod +x run.sh

ENTRYPOINT [ "./run.sh" ]