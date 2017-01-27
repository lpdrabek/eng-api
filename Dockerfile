FROM python:3

ADD requirements.txt /app/requirements.txt
COPY . /app

WORKDIR /app/

RUN pip install -r /app/requirements.txt
RUN useradd --shell /usr/sbin/nologin engineer -M -r

