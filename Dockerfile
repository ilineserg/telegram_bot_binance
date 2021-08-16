# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /

ENV TA_API_TOKEN=token
ENV TLG_TOKEN=token

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "app.py"]
