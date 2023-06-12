FROM python:3 AS app

COPY requirements.txt /app/
RUN pip3 install -r /app/requirements.txt
ENV PYTHONPATH="/Users/snaibbay/Desktop/fast_api/fast-library"

COPY src/ /src/
ENTRYPOINT uvicorn src.__main__:app --reload --host 0.0.0.0 --port 8000


FROM app AS test
COPY test-requirements.txt /test/

RUN pip install -r /test/test-requirements.txt

COPY test/ /test/

WORKDIR /test

ENTRYPOINT pytest -v
