FROM ubuntu:20.04
USER root

RUN apt update && \
    apt install -y python3.9 && \
     apt install -y python3-pip && \
      apt install -y sudo wget vim git curl gawk make gcc

COPY requirements.txt .
RUN pip3 install -r requirements.txt

RUN apt -y install locales && \
    localedef -f UTF-8 -i ja_JP ja_JP.UTF-8
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9
ENV TERM xterm

WORKDIR /var