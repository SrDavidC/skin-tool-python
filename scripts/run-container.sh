#!/bin/bash

# name for container
NAME=skin_tool_py
# public tcp port for the rest api
PORT=8069

# run the container
docker rm $NAME && docker stop $NAME
docker run -it -d --name $NAME -p $PORT:5000 jcedeno/skin-tool-python:latest
