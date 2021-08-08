# 기본 이미지
# n 레이어
FROM ubuntu:20.04

# 1레이어
MAINTAINER linker <bob10lcw>

RUN apt-get update

# 2레이어
RUN apt-get install nginx -y

RUN echo "\ndaemon off;" >> /etc/nginx/nginx.conf

# 3레이어
CMD [ "nginx" ]

EXPOSE 80

# ADD -> 압축해제됨 복사 시
# COPY -> 파일 그대로 복사 (압축이면 압축상태로)
# VOLUME 안에 있는 무언가를 외부에서 대체 할 수 있음
# USER
# WROKDIR -> 실행되는 경로를 지정