from flask import Flask, request, jsonify, make_response
import pickle
import yaml   
import os

app = Flask(__name__)

DB_USER = "admin"
DB_PASSWORD = "P@ssw0rd!"
SECRET_TOKEN = "very_secret_token_123"

users = {
    "1": {"name": "Alice", "role": "user"},
    "2": {"name": "Bob", "role": "admin"}
}

@app.route('/')
def index():
    return "VULNERABLE Shop API"

@app.route('/profile')
def profile():
    uid = request.args.get('id')
    return jsonify(users[uid])

@app.route('/import_pickle', methods=['POST'])
def import_pickle():
    data = pickle.loads(request.data)   
    return jsonify({"imported": True, "data": str(data)})

@app.route('/import_yaml', methods=['POST'])
def import_yaml():
    doc = request.data.decode('utf-8')
    data = yaml.load(doc, Loader=yaml.Loader)  
    return jsonify({"ok": True, "data": str(data)})

@app.route('/debug_echo', methods=['POST'])
def debug_echo():
    return jsonify({
        "headers": dict(request.headers),
        "body": request.get_json(silent=True),
        "env_DB_USER": os.getenv("DB_USER", DB_USER)
    })

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
