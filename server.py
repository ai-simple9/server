from flask import Flask, jsonify, request
import json
import hashlib
from datetime import date

app = Flask(__name__)

# ====================== БАЗА ПОЛЬЗОВАТЕЛЕЙ ======================
users = {
    "admin": {
        "password": hashlib.sha256("az1x@d0s".encode()).hexdigest(),
        "max_attacks": 100000,
        "attacks_today": 0,
        "last_date": str(date.today())
    },
    "free": {
        "password": hashlib.sha256("8974".encode()).hexdigest(),
        "max_attacks": 25,
        "attacks_today": 0,
        "last_date": str(date.today())
    }
}

@app.route('/api/users', methods=['GET'])
def get_users():
    # Обновляем дату при запросе
    today = str(date.today())
    for u in users:
        if users[u]["last_date"] != today:
            users[u]["attacks_today"] = 0
            users[u]["last_date"] = today
    return jsonify(users)

@app.route('/api/users', methods=['POST'])
def update_users():
    global users
    try:
        new_users = request.get_json()
        if new_users:
            users = new_users
            return jsonify({"status": "ok", "message": "База обновлена"})
        return jsonify({"status": "error"}), 400
    except:
        return jsonify({"status": "error"}), 500

if __name__ == '__main__':
    print("Сервер запущен → http://127.0.0.1:5000/api/users")
    app.run(host='0.0.0.0', port=5000, debug=False)
