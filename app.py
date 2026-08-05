from flask import Flask, render_template_string, request
import requests
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
        .success { color: #4cd137; margin-top: 15px; }
        a { color: #3ea6ff; text-decoration: none; font-weight: bold; font-size: 18px; word-break: break-all; }
    </style>
</head>
<body>
    <div class="container">
        <h2>NyxTube Downloader</h2>
        <form method="POST">
            <input type="text" name="url" placeholder="Paste YouTube Video URL here..." required>
            <br>
            <button type="submit">Get Download Link</button>
        </form>
        {% if dl_link %}
            <div class="success">
                <p>Your download link is ready:</p>
                <a href="{{ dl_link }}" target="_blank">📥 Click Here to Download Video</a>
            </div>
        {% endif %}
        {% if error %}
            <p style="color: #ff4d4d; margin-top: 10px;">{{ error }}</p>
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
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
            data = {
                "url": url
            }
            response = requests.post("https://api.cobalt.tools/api/json", json=data, headers=headers)
            res_json = response.json()
            
            if "url" in res_json:
                download_url = res_json["url"]
                return render_template_string(HTML_TEMPLATE, dl_link=download_url)
            elif "picker" in res_json:
                download_url = res_json["picker"][0]["url"]
                return render_template_string(HTML_TEMPLATE, dl_link=download_url)
            else:
                return render_template_string(HTML_TEMPLATE, error="Could not fetch download link. Try another URL.")
        except Exception as e:
            return render_template_string(HTML_TEMPLATE, error=str(e))
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    
