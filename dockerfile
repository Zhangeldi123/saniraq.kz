FROM python:3.12.2 AS requirements-stage

WORKDIR /tmp
RUN pip install poetry==1.5.0
COPY ./pyproject.toml ./poetry.lock /tmp/
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.12.2

WORKDIR /code
COPY --from=requirements-stage /tmp/requirements.txt .
RUN pip install --no-cache-dir --upgrade -r ./requirements.txt
RUN pip install --no-cache-dir uvicorn
RUN pip install --no-cache-dir python-multipart

COPY . .

EXPOSE 8000

ENTRYPOINT ["sh", "./scripts/launch.sh"]  