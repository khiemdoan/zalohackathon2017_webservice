FROM ubuntu:latest

LABEL maintainer="Khiem Doan <doankhiem.crazy@gmail.com>"

ENV DEBIAN_FRONTEND noninteractive
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

# install web service
COPY requirements.txt /src/requirements.txt
RUN buildDeps='python3-pip gcc libc6-dev python3-dev' \
    && apt-get update \
    && apt-get install -y --no-install-recommends python3 \
    && apt-get install -y --no-install-recommends $buildDeps \
    && rm -rf /var/lib/apt/lists/* \
    && pip3 install --upgrade pip \
    && pip3 install setuptools \
    && pip3 install gunicorn gevent \
    && pip3 install -r /src/requirements.txt \
    && apt-get purge -y --auto-remove $buildDeps

# use for debug
ENV FLASK_APP /src/service.py
ENV FLASK_DEBUG 1

EXPOSE 5000
WORKDIR /src
ENTRYPOINT gunicorn service:app --bind=0.0.0.0:5000 --workers=4 --worker-class=gevent