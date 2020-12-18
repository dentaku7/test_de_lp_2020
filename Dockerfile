FROM python:3.8

COPY requirements.txt requirements.txt

RUN pip install --no-cache -r requirements.txt

COPY app app