from flask import Flask, request, jsonify, send_from_directory, render_template_string
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = './uploads'
PASSWORD = "mysecretpassword" # ★パスワード
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# --- ここにHTMLを丸ごと貼り付ける ---
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>All-in-One Share</title>
    <style>
        body { font-family: sans-serif; padding: 20px; max-width: 500px; margin: auto; background: #f0f2f5; }
        .card { background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        input, button { width: 100%; padding: 10px; margin: 5px 0; box-sizing: border-box; }
        button { background: #007bff; color: white; border: none; cursor: pointer; }
        .file-item { display: flex; justify-content: space-between; padding: 10px; border-bottom: 1px solid #eee; }
    </style>
</head>
<body>
    <div class="card">
        <h2>ファイル共有サイト</h2>
        <input type="password" id="pw" placeholder="パスワードを入力">
        <hr>
        <input type="file" id="fileInput">
        <button onclick="uploadFile()">アップロード</button>
        <hr>
        <button onclick="loadFiles()" style="background:#28a745;">一覧更新</button>
        <div id="list"></div>
    </div>

    <script>
        async function uploadFile() {
            const fileInput = document.getElementById('fileInput');
            const pw = document.getElementById('pw').value;
            const formData = new FormData();
            formData.append('file', fileInput.files[0]);

            const res = await fetch('/upload', {
                method: 'POST',
                headers: { 'X-Password': pw },
                body: formData
            });
            if (res.ok) { alert('成功'); loadFiles(); } else { alert('失敗'); }
        }

        async function loadFiles() {
            const pw = document.getElementById('pw').value;
            const res = await fetch('/files', { headers: { 'X-Password': pw } });
            if (res.ok) {
                const files = await res.json();
                const list = document.getElementById('list');
                list.innerHTML = files.map(f => `
                    <div class="file-item">
                        <span>${f}</span>
                        <a href="/download/${f}?pw=${pw}" target="_blank">保存</a>
                    </div>
                `).join('');
            }
        }
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    # アクセスされたら上のHTMLを返す
    return render_template_string(HTML_TEMPLATE)

@app.route('/upload', methods=['POST'])
def upload():
    pw = request.headers.get('X-Password')
    if pw != PASSWORD: return "NG", 401
    file = request.files.get('file')
    if file:
        file.save(os.path.join(UPLOAD_FOLDER, file.filename))
        return "OK"
    return "No file", 400

@app.route('/files')
def list_files():
    pw = request.headers.get('X-Password')
    if pw != PASSWORD: return "NG", 401
    return jsonify(os.listdir(UPLOAD_FOLDER))

@app.route('/download/<name>')
def download(name):
    pw = request.args.get('pw')
    if pw != PASSWORD: return "NG", 401
    return send_from_directory(UPLOAD_FOLDER, name)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
