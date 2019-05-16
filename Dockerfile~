FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
Run apt-get update \
    && apt-get install -y mecab \
    && apt-get install -y libmecab-dev \
    && apt-get install -y mecab-ipadic-utf8 \
    && apt-get install -y git \
    && apt-get install -y make \
    && apt-get install -y curl \
    && apt-get install -y xz-utils \
    && apt-get install -y file \
    && apt-get install -y sudo \
    && apt-get install -y wget

RUN git clone --depth 1 https://github.com/neologd/mecab-ipadic-neologd.git \
    && cd mecab-ipadic-neologd \
    && bin/install-mecab-ipadic-neologd -n -y 

RUN apt-get install -y software-properties-common vim

RUN pip3 install -r requirements.txt
COPY . /code/
