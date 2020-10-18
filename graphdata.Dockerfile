FROM golemfactory/base:1.5

MAINTAINER Jude Hungerford <smiley7c0@gmail.com>

RUN apt-get -y update && apt-get -y upgrade

RUN apt-get -y install python3-matplotlib

ADD graphWavePair.py /golem/work/graphWavePair.py
ADD dummyScript.py /golem/work/dummyScript.py

RUN chmod u+x /golem/work/graphWavePair.py
RUN chmod u+x /golem/work/dummyScript.py

WORKDIR /golem/work

VOLUME /golem/work
