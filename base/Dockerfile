# This image image can also be pulled from gitlab.lrz.de:5005/tum-cps/commonroad-docker-submission/base:1.0.0

FROM python:3.9-slim

COPY ./dummy_solutions /commonroad/dummy_solutions
COPY dependencies.txt /commonroad/base/dependencies.txt
COPY requirements.txt /commonroad/base/requirements.txt

RUN apt-get -y update && \
    xargs -rxa /commonroad/base/dependencies.txt -- apt-get -y install -- && \
    python3.9 -m pip install --no-cache-dir -r /commonroad/base/requirements.txt

# ------------ BEGIN SUMO installation --------------
# Turn off interactive install
ENV DEBIAN_FRONTEND=noninteractive

# Enable colored output
ENV TERM xterm-256color

RUN apt-get -y update && \
    apt-get -y install \
    cmake \
    g++ \
    libxerces-c-dev \
    libfox-1.6-dev \ 
    libgdal-dev \
    libproj-dev \
    libgl2ps-dev \
    swig \
    default-jdk \
    maven \
    libeigen3-dev 

# Checkout SUMO with fixed version v1_12_0
RUN git clone --branch v1_12_0 --depth 1 --single-branch --recursive https://github.com/eclipse/sumo && \
    rm -rf ./sumo/.git ./sumo/tests

# Build SUMO
RUN mkdir /sumo/build/cmake-build
WORKDIR /sumo/build/cmake-build
RUN cmake ../..
RUN make -j 8
WORKDIR /

ENV SUMO_HOME=/sumo
ENV PATH=$PATH:/sumo/bin

# ------------ END SUMO installation --------------
