from flask import Flask, render_template_string, request, send_file, redirect, url_for
import yt_dlp
import os

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NyxTube - Video Downloader</title>
    <style>
        body { font-family: Arial, sans-serif; background: #0f0f0f; color: #fff; text-align: center; padding: 50px; }
        .container { max-width: 500px; margin: auto; background: #212121; padding: 30px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }
        input[type="text"] { width: 90%; padding: 12px; margin: 15px 0; border: none; border-radius: 6px; font-size: 16px; }
        button { background: #ff0000; color: white; border: none; padding: 12px 20px; font-size: 16px; border-radius: 6px; cursor: pointer; font-weight: bold; }
        button:hover { background: #cc0000; }
        .error { color: #ff4d4d; margin-top: 10px; }
    </style>
</head>
<body>
    <div class="container">
        <h2>NyxTube Downloader</h2>
        <form method="POST">
            <input type="text" name="url" placeholder="Paste YouTube Video URL here..." required>
            <br>
            <button type="submit">Download Video</button>
        </form>
        {% if error %}
            <p class="error">{{ error }}</p>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('url')
        try:
            ydl_opts = {
                'format': 'best',
                'outtmpl': 'downloads/%(title)s.%(ext)s',
                'extractor_args': {'youtube': {'player_client': ['android', 'web']}}
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
            return send_file(filename, as_attachment=True)
        except Exception as e:
            return render_template_string(HTML_TEMPLATE, error=str(e))
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    os.makedirs('downloads', exist_ok=True)
    app.run(host='0.0.0.0', port=5000)
    
