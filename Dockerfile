FROM python:3.12
LABEL authors="crusazer"

WORKDIR /Task-managment

RUN pip install --upgrade pip
COPY requirements.txt /Task-managment
RUN pip install -r requirements.txt

COPY . /Task-managment
