#!/bin/bash

# name for container
NAME=skin_tool
# public tcp port for the rest api
PORT=8069

# run the container
docker run -it -d --name $NAME -p $PORT:5000 jcedeno/skin-tool-opencv:latest
