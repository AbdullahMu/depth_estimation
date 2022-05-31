FROM ubuntu:18.04 as builder
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential \
    python3 \
    python3-pip \
    python3-venv \
    python3.8-dev \
    && rm -rf /var/apt/archives \
    && rm -rf /var/lib/apt/lists
RUN python3 -m pip install --upgrade pip \
    && python3 -m pip install build
COPY . /data
RUN cd data && python3 -m build .