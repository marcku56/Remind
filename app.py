from flask import Flask, render_template, jsonify, request
import time
import random
import string

app = Flask(__name__)

# ================= ЧАСЫ =================
MONTHS_RU = [
    "Января", "Февраля", "Марта", "Апреля",
    "Мая", "Июня", "Июля", "Августа",
    "Сентября", "Октября", "Ноября", "Декабря"
]

def get_time():
    now = time.localtime()
    date_str = f"{now.tm_mday} {MONTHS_RU[now.tm_mon-1]} {now.tm_year}"
    time_str = time.strftime("%H:%M:%S", now)
    return f"{date_str} {time_str}"

@app.route("/time")
def time_route():
    return jsonify({"time": get_time()})

# ================= ИГРА УГАДАЙ ЧИСЛО =================
secret_number = random.randint(0, 100)

@app.route("/guess", methods=["POST"])
def guess_number():
    global secret_number
    data = request.json
    user_guess = data.get("guess")
    if user_guess is None:
        return jsonify({"result": "Ошибка: нет числа"}), 400
    try:
        user_guess = int(user_guess)
    except ValueError:
        return jsonify({"result": "Ошибка: введи число"}), 400

    if user_guess < secret_number:
        return jsonify({"result": "Больше"})
    elif user_guess > secret_number:
        return jsonify({"result": "Меньше"})
    else:
        secret_number = random.randint(0, 100)  # новое число
        return jsonify({"result": "Ты угадал!"})

# ================= ГЕНЕРАТОР ПАРОЛЕЙ =================
@app.route("/password", methods=["POST"])
def generate_password():
    data = request.json
    ptype = data.get("type", "letters")
    length = 12
    chars = ""
    if ptype=="letters":
        chars = string.ascii_letters
    elif ptype=="digits":
        chars = string.digits
    elif ptype=="lettersdigits":
        chars = string.ascii_letters + string.digits
    elif ptype=="all":
        chars = string.ascii_letters + string.digits + string.punctuation
    else:
        return jsonify({"result": "Ошибка"}), 400

    password = ''.join(random.choice(chars) for _ in range(length))
    return jsonify({"result": password})

# ================= ГЛАВНАЯ СТРАНИЦА =================
@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
