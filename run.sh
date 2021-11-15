#!/bin/sh
DOCKERHOST=localhost:8500
docker run -d --restart always --name my-webserver -p 8081:8080 $DOCKERHOST/sspws:latest