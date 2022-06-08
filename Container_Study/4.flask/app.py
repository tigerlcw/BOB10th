import os
from flask import Flask, render_template

app = Flask(__name__)

color = os.environ.get('APP_COLOR') # 환경변수로 부터 빨강색 불러오기 하지만 지금은 없어서, 밑 줄에 고정 해놓음
color = "red"

@app.route('/')
def main():
    return render_template('hello.html', color=color)

if __name__  == "__main__":
    app.run(debug=True, host= '0.0.0.0' , port=5000)

