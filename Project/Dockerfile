FROM python:alpine
RUN mkdir /server
WORKDIR /server

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY main.py .
