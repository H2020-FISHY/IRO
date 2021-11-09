FROM python:3.7-slim

COPY . /iro


RUN pip install flask numpy flask_classful anytree
RUN pip install elasticsearch

EXPOSE 5000
CMD python /iro/main.py
