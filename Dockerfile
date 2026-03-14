FROM python:3.12-alpine

WORKDIR /app

RUN apk add docker-cli docker-cli-compose

COPY tools/requirements.txt /app/

RUN pip3 install -r requirements.txt

COPY server.py /app/
COPY modules /app/modules

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]