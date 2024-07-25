# Используем официальный образ Python
FROM python:3.10-slim


WORKDIR /backend

ENV PYTHONDONTWRITEBYTECODE = 1\
	PYTHONNONBUFFERED = 1

COPY requirements.txt /backend

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

RUN pip install -r requirements.txt

COPY . /backend

EXPOSE 8000

