import openai
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

openai.api_key = config["openai"]["api_key"]


# text-davinci-002は、GPT-3の中でも最も高性能なモデルだが、応答速度が遅い
# gpt-3.5-turboは、text-davinci-002よりも応答速度が速いが、性能は劣る
def chat_with_gpt3(prompt, model="text-davinci-002", tokens=150):
    response = openai.Completion.create(
        engine=model,
        prompt=prompt,
        max_tokens=tokens,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response.choices[0].text


if __name__ == "__main__":
    while True:
        # 例: あなたはどんなことが得意ですか？箇条書きで10個教えてください。lang:ja
        user_input = input("あなた：")
        if user_input.lower() == "exit":
            break
        prompt = f"以下の質問への答えを教えてください: {user_input}"
        response = chat_with_gpt3(prompt)
        print("GPT-3チャットボット:", response)
