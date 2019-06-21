FROM ubuntu:xenial

RUN apt-get update \
 && apt-get install gnupg -y

RUN echo "deb http://repo.sawtooth.me/ubuntu/nightly xenial universe" >> /etc/apt/sources.list \
 && (apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 44FC67F19B2466EA \
 || apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 44FC67F19B2466EA) \
 && apt-get update

RUN apt-get install -y -q \
    git \
    python3 \
    python3-stdeb

RUN apt-get install -y -q \
    python3-grpcio \
    python3-grpcio-tools \
    python3-protobuf

RUN apt-get install -y -q \
    python3-cbor \
    python3-colorlog \
    python3-secp256k1 \
    python3-toml \
    python3-yaml \
    python3-zmq

RUN mkdir -p /var/log/sawtooth

ENV PATH=$PATH:/project/sawtooth-sdk-python/bin

WORKDIR /project/sawtooth-sdk-python

CMD echo "\033[0;32m--- Building med-tp-python ---\n\033[0m" \
 && bin/protogen \
 && cd med_python \
 && python3 setup.py clean --all \
 && python3 setup.py build