from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import openai
import configparser

config = configparser.ConfigParser()
config.read("config.ini")
openai.api_key = config["openai"]["api_key"]

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")


def get_response_stream(prompt):
    responses = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
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

    return message.strip()


@app.route("/")
def index():
    return render_template("index.html")


@socketio.on("message")
def handleMessage(msg):
    get_response_stream(msg)


if __name__ == "__main__":
    # app.run(host="127.0.0.1", port=5001)
    # 現在の設定ではアプリケーションはローカルホスト（127.0.0.1）でのみアクセス可能
    # 外部からアクセスできるようにするには、`app.py`の`app.run()`関数の`host`引数を変更
    # 全アクセスを受け付けてしまうので、実稼働環境ではリバースプロキシ（例：Nginx）を構成して、安全な方法で外部からアクセスできるようにすること
    app.run(host="0.0.0.0", port=5001)
