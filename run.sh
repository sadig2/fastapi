#!/bin/bash -ex

docker volume create myvolume

docker stop $(docker ps -qa)

docker build -t app --target app .

docker run --rm -it -p 8000:8000 -v $(pwd)/src:/src -v /$(pwd)/data:/data app
