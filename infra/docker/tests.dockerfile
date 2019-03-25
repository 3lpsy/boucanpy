FROM python:3.7

RUN mkdir /requirements

COPY ./requirements.txt /requirements/requirements.txt

RUN pip install -r /requirements/requirements.txt

VOLUME /bountydns
