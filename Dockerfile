FROM debian:buster
LABEL maintainer "Pascal Meunier @milhouse1337"

# ENV TZ "America/Montreal"

ENV DEBIAN_FRONTEND noninteractive

# RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update && apt-get install -y \
    software-properties-common \
    python3-setuptools \
    python3-pip \
    python3-numpy \
    gdal-bin \
    libgdal-dev \
    libsm6 \
    libxext6 \
    libxrender-dev \
  && rm -rf /var/lib/apt/lists/*

RUN pip3 install --upgrade pip
RUN pip3 install numpy "GDAL==$(gdal-config --version)"
RUN pip3 install opencv-python
RUN pip3 install felicette

WORKDIR /root

CMD ["/usr/local/bin/felicette"]
