FROM python:alpine
RUN mkdir /server
WORKDIR /server

RUN apk add --no-cache g++
COPY requirements.txt .
RUN pip install -r requirements.txt


COPY main.py .
