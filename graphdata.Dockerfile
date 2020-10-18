FROM golemfactory/base:1.5

MAINTAINER Jude Hungerford <smiley7c0@gmail.com>

RUN apt-get -y update && apt-get -y upgrade

RUN apt-get -y install python3-matplotlib

WORKDIR /golem/work

VOLUME /golem/work
