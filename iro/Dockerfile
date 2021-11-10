FROM python:3.7-slim

COPY . /iro

RUN pip install flask numpy flask_classful anytree elasticsearch certifi
WORKDIR /iro

CMD [ "python3", "main.py" ]
