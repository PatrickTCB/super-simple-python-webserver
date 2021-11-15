#!/bin/sh
DOCKERHOST=docker.phn1.net
docker run -d --restart always --name my-webserver -p 8081:8080 $DOCKERHOST/sspws:latest