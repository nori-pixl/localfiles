from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app) # これがないとPyScriptから接続できません

UPLOAD_FOLDER = './uploads'
PASSWORD = "mysecretpassword"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload():
    if request.headers.get('X-Password') != PASSWORD: return "NG", 401
    file = request.files.get('file')
    if file:
        file.save(os.path.join(UPLOAD_FOLDER, file.filename))
        return "OK"
    return "No file", 400

@app.route('/files')
def list_files():
    if request.headers.get('X-Password') != PASSWORD: return "NG", 401
    return jsonify(os.listdir(UPLOAD_FOLDER))

@app.route('/download/<name>')
def download(name):
    if request.args.get('pw') != PASSWORD: return "NG", 401
    return send_from_directory(UPLOAD_FOLDER, name)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
