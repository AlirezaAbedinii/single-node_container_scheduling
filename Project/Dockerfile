FROM python:alpine
RUN mkdir /server
WORKDIR /server

RUN apk add build-base
COPY requirements.txt .
RUN pip install -r requirements.txt


COPY main.py .
