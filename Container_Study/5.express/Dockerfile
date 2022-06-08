FROM node:alpine

# ENV TZ=Asia/Seoul -> 타임존 환경셋

WORKDIR /app
ADD app.js /app
ADD package.json /app

RUN npm install express

CMD [ "node", "app.js" ]

# node 컨테이너 d0f0380dcff2