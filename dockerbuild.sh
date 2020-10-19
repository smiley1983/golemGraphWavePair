#!/usr/bin/env sh
docker build . -f graphdata.Dockerfile -t graphwavepair
#gvmkit-build graphwavepair
#gvmkit-build graphwavepair --push
#docker run -it graphwavepair # Can be useful to check that the image works
