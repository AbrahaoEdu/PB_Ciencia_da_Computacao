FROM ubuntu:22.04
RUN apt-get update && apt-get install -y \
    build-essential gcc g++ libomp-dev python3 python3-pip \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /tp3
COPY . .
RUN pip3 install matplotlib psutil reportlab
CMD ["/bin/bash"]
