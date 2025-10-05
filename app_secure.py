# app_secure.py
from flask import Flask, request, jsonify
import json
import os
from dotenv import load_dotenv
import yaml

load_dotenv() 

app = Flask(__name__)

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
SECRET_TOKEN = os.getenv("SECRET_TOKEN")

users = {
    "1": {"name": "Alice", "role": "user"},
    "2": {"name": "Bob", "role": "admin"}
}

@app.route('/')
def index():
    return "SECURE Shop API"

@app.route('/profile')
def profile():
    uid = request.args.get('id')
    if not uid or uid not in users:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"id": uid, "name": users[uid]["name"]})

@app.route('/import_pickle', methods=['POST'])
def import_pickle():
    return jsonify({"error": "Pickle import is not allowed"}), 400

@app.route('/import_yaml', methods=['POST'])
def import_yaml():
    try:
        doc = request.data.decode('utf-8')
        data = yaml.safe_load(doc)
        if not isinstance(data, dict):
            return jsonify({"error": "Invalid YAML payload"}), 400
        return jsonify({"ok": True, "data": data})
    except Exception:
        return jsonify({"error": "Invalid YAML"}), 400

@app.route('/debug_echo', methods=['POST'])
def debug_echo():
    payload = request.get_json(silent=True)
    return jsonify({"received": bool(payload)})

@app.errorhandler(Exception)
def handle_error(e):
    app.logger.exception("Unhandled exception")
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=False)
