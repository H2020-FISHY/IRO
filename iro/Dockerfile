FROM python:3.7-slim

COPY . /iro

RUN apt update
RUN DEBIAN_FRONTEND=noninteractive apt install -y iproute2
WORKDIR /iro
RUN pip install -r requirements.txt
RUN mkdir /iro/notification_store/reports/
RUN mkdir /iro/outputfiles

CMD [ "./entrypoint.sh" ]
