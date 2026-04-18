from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__)
# すべての外部アクセスを許可
CORS(app)

# --- 設定項目 ---
UPLOAD_FOLDER = './uploads'
PASSWORD = "mysecretpassword"  # ★スマホBで入力するパスワード
# ----------------

# 保存用フォルダの作成
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def check_auth(req):
    """パスワードをチェックする共通関数"""
    # ヘッダー(X-Password) または URLパラメータ(?pw=) から取得
    client_pw = req.headers.get('X-Password') or req.args.get('pw')
    return client_pw == PASSWORD

@app.route('/')
def home():
    return "Server is running. Please use your HTML interface to access."

# 1. アップロード機能
@app.route('/upload', methods=['POST'])
def upload():
    if not check_auth(request):
        return jsonify({"error": "Unauthorized"}), 401
    
    file = request.files.get('file')
    if file:
        # ファイル名を安全に取得して保存
        filename = file.filename
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        return jsonify({"status": "success", "filename": filename})
    return jsonify({"status": "no file"}), 400

# 2. ファイル一覧取得機能
@app.route('/files', methods=['GET'])
def list_files():
    if not check_auth(request):
        return jsonify({"error": "Unauthorized"}), 401
    
    files = os.listdir(UPLOAD_FOLDER)
    return jsonify(files)

# 3. ダウンロード機能
@app.route('/download/<filename>', methods=['GET'])
def download(filename):
    if not check_auth(request):
        return "Unauthorized", 401
    
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

if __name__ == '__main__':
    # クラウド環境やローカルネットワークで公開するために 0.0.0.0 で起動
    app.run(host='0.0.0.0', port=5000)
