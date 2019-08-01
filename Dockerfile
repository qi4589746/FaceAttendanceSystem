FROM mongo:3.4.22-xenial

RUN apt-get -y update

RUN apt-get install -y \
    build-essential \
    cmake \
    gfortran \
    git \
    wget \
    curl \
    graphicsmagick \
    libgraphicsmagick1-dev \
    libatlas-dev \
    libavcodec-dev \
    libavformat-dev \
    libgtk2.0-dev \
    libjpeg-dev \
    liblapack-dev \
    libswscale-dev \
    pkg-config \
    python3-dev \
    python3-pip \
    python3-numpy \
    software-properties-common \
    zip \
    && apt-get clean && rm -rf /tmp/* /var/tmp/* \
    && apt-get autoclean && apt-get autoremove --purge

RUN pip3 install setuptools

RUN cd ~ && \
    mkdir -p dlib && \
    git clone -b 'v19.9' --single-branch https://github.com/davisking/dlib.git dlib/ && \
    cd  dlib/ && \
    python3 setup.py install --yes USE_AVX_INSTRUCTIONS

# The rest of this file just runs an example script.

# If you wanted to use this Dockerfile to run your own app instead, maybe you would do this:
COPY . /root/faceBackend
RUN cd /root/faceBackend && \
    pip3 install -r requirements.txt

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

EXPOSE 5000 27017

WORKDIR /root/faceBackend

RUN touch start.sh
RUN echo '#!/bin/sh' >> start.sh
RUN echo 'docker-entrypoint.sh mongod &' >> start.sh
RUN echo 'flask run' >> start.sh
RUN chmod 777 start.sh

CMD ["/root/faceBackend/start.sh"]