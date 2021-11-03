FROM python:3.6.10-alpine

RUN apk add gcc musl-dev linux-headers

COPY . /exporter
#ADD x.tar.gz /y

EXPOSE 5000

RUN pip install --upgrade pip
RUN pip install flask numpy flask_classful anytree
RUN pip install elasticsearch

CMD python /exporter/main.py
