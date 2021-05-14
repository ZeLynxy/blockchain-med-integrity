FROM ubuntu:20.04
RUN apt update
RUN apt install -y software-properties-common && \
    rm -rf /var/lib/apt/lists/*
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt install -y python3.8 python3-pip

WORKDIR /api

COPY requirements.txt .
RUN pip3 install --upgrade pip
RUN pip3 install  --no-cache-dir  -r requirements.txt

VOLUME /api 
VOLUME /smart-contracts 

ADD /api  /api
ADD /smart-contracts /smart-contracts 

RUN add-apt-repository ppa:ethereum/ethereum
RUN apt-get update
RUN apt-get install -y solc
RUN pip3 install py-solc-x
WORKDIR /smart-contracts
#RUN python3.8 deploy.py
WORKDIR /api