FROM debian:latest
LABEL maintainer "Pascal Meunier @milhouse1337"

# ENV TZ "America/Montreal"

ENV DEBIAN_FRONTEND noninteractive

# RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update && apt-get install -y \
    software-properties-common \
    python3-setuptools \
    python3-pip \
    python-numpy \
    gdal-bin \
    libgdal-dev \
    libsm6 \
    libxext6 \
    libxrender-dev

RUN pip3 install --upgrade pip
RUN pip install numpy GDAL==$(gdal-config --version)
RUN pip install opencv-python
RUN pip install felicette

WORKDIR /root

CMD ["/usr/local/bin/felicette"]
