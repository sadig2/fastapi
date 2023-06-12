FROM python:3 AS app

COPY requirements.txt /app/
RUN pip3 install -r /app/requirements.txt

COPY src/ /app/

ENTRYPOINT uvicorn app.__main__:app --reload --host 0.0.0.0 --port 8000


FROM app AS test

COPY test-requirements.txt /test/
RUN pip install -r /test/test-requirements.txt

COPY test/ /test/

WORKDIR /test

ENTRYPOINT pytest -v
