FROM python:3.10-alpine

WORKDIR /app

COPY ./requirements.txt .

RUN pip install -r requirements.txt

ENV MONGO_PORT=27017
ENV MONGO_HOST=mongo

COPY server.py .


CMD python3 server.py


