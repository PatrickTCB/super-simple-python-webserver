FROM python:3-buster

RUN mkdir /webserver
RUN mkdir /db
RUN apt-get clean && apt-get update && apt-get install -y locales
RUN locale-gen en_US.UTF-8
RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen
ENV LC_ALL="en_US.UTF-8"
ENV export LC_CTYPE="en_US.UTF-8"
ENV FQDN="example.com"
RUN dpkg-reconfigure --frontend=noninteractive locales

COPY ./app/ /webserver

WORKDIR /webserver

EXPOSE 8080

CMD [ "python3", "-u", "/webserver/server.py"]