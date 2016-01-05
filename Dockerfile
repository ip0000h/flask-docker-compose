FROM python:2.7.10-slim

MAINTAINER Ivan Gorbachev <ip0000h@gmail.com>

RUN apt-get update && apt-get install -qq -y build-essential libpq-dev libffi-dev && \
apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
-o APT::AutoRemove::SuggestsImportant=false $buildDeps && \
easy_install pip

COPY ./app/requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
