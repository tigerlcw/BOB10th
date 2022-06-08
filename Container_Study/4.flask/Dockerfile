FROM python:3.8-alpine

RUN pip install flask

WORKDIR /app
COPY  . /app

CMD ["python","app.py"]
EXPOSE 5000


# RUN pip install -r requirements.txt -> pip list 뽑아온거 다른 곳에서 다시 설치할때 명령어 ㅇㅇ