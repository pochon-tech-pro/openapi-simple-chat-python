import openai
import configparser
from flask import (
    Flask,
    request,
    jsonify,
    render_template,
)  # pip install flask
from flask_socketio import SocketIO  # pip install flask-socketio

config = configparser.ConfigParser()
config.read("config.ini")
openai.api_key = config["openai"]["api_key"]

app = Flask(__name__, template_folder="templates")
socketio = SocketIO(app)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@socketio.on("chat")
def handle_chat(user_input):
    if not user_input:
        return jsonify({"error": "Missing 'message' field in form data"}), 400
    response = chat_with_gpt3(user_input)
    socketio.emit("response", response)


# text-davinci-002は、GPT-3の中でも最も高性能なモデルだが、応答速度が遅い
# gpt-3.5-turboは、text-davinci-002よりも応答速度が速いが、性能は劣る
def chat_with_gpt3(prompt, model="text-davinci-002", tokens=2048):
    response = openai.Completion.create(
        engine=model,
        prompt=prompt,
        max_tokens=tokens,
        n=1,
        stop=None,
        temperature=0.5,
    )
    print(response.choices[0].text)
    return response.choices[0].text


def main():
    app.debug = True  # デバッグモードを有効にする
    app.run(host="127.0.0.1", port=5001)


if __name__ == "__main__":
    main()
