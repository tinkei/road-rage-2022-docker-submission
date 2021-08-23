# This image image can also be pulled from gitlab.lrz.de:5005/tum-cps/commonroad-docker-submission/base:1.0.0

FROM python:3.7-slim

COPY ./dummy_solutions /commonroad/dummy_solutions
COPY dependencies.txt /commonroad/base/dependencies.txt
COPY requirements.txt /commonroad/base/requirements.txt

RUN apt-get -y update && \
    xargs -rxa /commonroad/base/dependencies.txt -- apt-get -y install -- && \
    python3.7 -m pip install --no-cache-dir -r /commonroad/base/requirements.txt && \
    git clone https://gitlab.lrz.de/tum-cps/commonroad-drivability-checker.git --single-branch --branch master --depth 1 && \
    cd commonroad-drivability-checker && \
    bash build.sh -e /usr/local -v 3.7 --cgal --serializer -w -i -j 8

# ------------ BEGIN SUMO installation --------------
# Turn off interactive install
ENV DEBIAN_FRONTEND=noninteractive

# Enable colored output
ENV TERM xterm-256color

RUN apt-get update && \
    apt-get -qq install \
    wget \
    curl\
    g++ \
    cmake \
    make \
    libxerces-c-dev \
    libeigen3-dev \
    libfox-1.6-0 libfox-1.6-dev \
    libsqlite3-dev \
    libgdal-dev \
    libproj-dev \
    libgl2ps-dev

# Checkout SUMO with fixed version v1_9_2
RUN git clone --branch v1_9_2 --depth 1 --single-branch --recursive https://github.com/eclipse/sumo && rm -rf ./sumo/.git ./sumo/tests

# Build SUMO
RUN mkdir /sumo/build/cmake-build
WORKDIR /sumo/build/cmake-build
RUN cmake ../..
RUN make -j 8
WORKDIR /

ENV SUMO_HOME=/sumo
ENV PATH=$PATH:/sumo/bin

# ------------ END SUMO installation --------------
