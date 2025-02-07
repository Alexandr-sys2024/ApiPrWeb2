from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

def get_random_quote():
    try:
        response = requests.get("https://zenquotes.io/api/random", timeout=5)
        response.raise_for_status()
        data = response.json()
        return data[0]["q"], data[0]["a"]
    except requests.exceptions.Timeout:
        return "Ошибка: превышено время ожидания запроса", "Сервер недоступен"
    except requests.exceptions.RequestException:
        return "Ошибка при получении цитаты", "Неизвестный автор"

@app.route("/")
def index():
    quote, author = get_random_quote()
    return render_template("index.html", quote=quote, author=author)

@app.route("/quote")
def quote():
    quote, author = get_random_quote()
    return jsonify({"quote": quote, "author": author})

if __name__ == "__main__":
    app.run(debug=True)