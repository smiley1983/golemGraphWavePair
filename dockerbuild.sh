#!/usr/bin/env sh
docker build . -f graphdata.Dockerfile -t graphdata
#gvmkit-build graphdata --push
#docker run -it graphdata
