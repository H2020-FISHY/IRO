FROM python:3.7-slim

COPY . /iro

RUN apt update
RUN DEBIAN_FRONTEND=noninteractive apt install -y iproute2
RUN pip install flask numpy flask_classful anytree elasticsearch certifi
WORKDIR /iro
RUN mkdir /iro/outputfiles

CMD [ "./entrypoint.sh" ]
