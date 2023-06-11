#!/bin/bash -ex

docker volume create myvolume

docker build -t app --target app .

docker run -p 8000:8000 -v myvolume:/data app
