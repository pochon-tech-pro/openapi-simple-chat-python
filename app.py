from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import openai
import configparser

# FlaskとFlask-SocketIOがeventletサーバを使用することを求めているため、eventletをインポート
# Flask-SocketIOは、ソケット通信を処理するためにWebSocketサーバ（この場合eventlet）が必要
# Flask-SocketIOがデフォルトでeventletを使用しようとするのは、eventletが非同期I/Oをサポートし、より良いパフォーマンスを提供するから
# pip install eventlet
# import eventlet

# # eventletが非同期I/Oをフルに活用できるように、Pythonの標準ライブラリをパッチする
# eventlet.monkey_patch()

config = configparser.ConfigParser()
config.read("config.ini")
openai.api_key = config["openai"]["api_key"]

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")


def chat_completion_api_call(user_model_input: str, prompt: str):
    responses = openai.ChatCompletion.create(
        model=user_model_input,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        max_tokens=256,
        stream=True,
    )

    message = ""
    for response in responses:
        chunk = response["choices"][0]["delta"].get("content")

        if chunk == None:
            pass
        else:
            print(chunk, end="", flush=True)  # 逐次出力
            message += chunk
            socketio.emit("char", chunk)


def completion_api_call(user_model_input: str, prompt: str):
    responses = openai.Completion.create(
        model=user_model_input,
        prompt=prompt,
        temperature=0,
        max_tokens=256,
        stream=True,
    )

    message = ""
    for response in responses:
        chunk = response["choices"][0]["text"]

        if chunk == None:
            pass
        else:
            print(chunk, end="", flush=True)  # 逐次出力
            message += chunk
            socketio.emit("char", chunk)


@app.route("/")
def index():
    return render_template("index.html")


@socketio.on("message")
def handleMessage(data):
    user_model_input = data["user_model_input"]
    user_input = data["user_input"]
    # gpt-3.5-turboかgpt4であれば
    if user_model_input == "gpt-3.5-turbo" or user_model_input == "gpt-4":
        chat_completion_api_call(user_model_input, user_input)
    elif user_model_input == "text-davinci-003" or user_model_input == "text-curie-001":
        completion_api_call(user_model_input, user_input)
    else:
        print("error")


if __name__ == "__main__":
    # app.run(host="127.0.0.1", port=5001)
    # 現在の設定ではアプリケーションはローカルホスト（127.0.0.1）でのみアクセス可能
    # 外部からアクセスできるようにするには、`app.py`の`app.run()`関数の`host`引数を変更
    # 全アクセスを受け付けてしまうので、実稼働環境ではリバースプロキシ（例：Nginx）を構成して、安全な方法で外部からアクセスできるようにすること
    app.run(host="0.0.0.0", port=5001)
