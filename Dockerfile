FROM python:3.6
RUN apt update && apt install python3-pip git -y && pip3 install pipenv
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD . /code/
RUN pipenv install
RUN pipenv install django

