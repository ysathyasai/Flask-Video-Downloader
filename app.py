import os
import threading
import unicodedata
import re
from flask import Flask, request, render_template, send_file, jsonify
import yt_dlp

app = Flask(__name__)
DOWNLOADS_DIR = os.path.expanduser("~/storage/shared/downloads")

progress = {
    'status': 'Waiting...',
    'percent': 0,
    'done': False,
    'error': ''
}
progress_lock = threading.Lock()
last_video_filename = None

def safe_filename(filename):
    value = unicodedata.normalize('NFKD', filename).encode('ascii', 'ignore').decode('ascii')
    value = str(re.sub(r'[^A-Za-z0-9_.-]', '_', value))
    return value[:100]  # Limit length for filesystem safety

def download_hook(d):
    with progress_lock:
        try:
            if d['status'] == 'downloading':
                percent_str = d.get('_percent_str', '0.0%').strip()
                try:
                    percent = float(percent_str.replace('%', ''))
                except ValueError:
                    percent = 0
                progress['percent'] = int(percent)
                progress['status'] = f'Downloading... {percent_str}'
                progress['done'] = False
            elif d['status'] == 'finished':
                progress['percent'] = 100
                progress['status'] = 'Processing file...'
                progress['done'] = False
        except Exception as e:
            progress['status'] = f"Error in hook: {e}"
            progress['done'] = True

def download_video(url, quality, download_subs):
    global last_video_filename
    try:
        ydl_opts = {
            'format': f'bestvideo[height<={quality}]+bestaudio/best[height<={quality}]',
            'outtmpl': os.path.join(DOWNLOADS_DIR, '%(title)s.%(ext)s'),
            'merge_output_format': 'mp4',
            'progress_hooks': [download_hook],
            'quiet': False,
            'no_warnings': False,
            'progress_with_newline': False,
            'ignoreerrors': True,  # Don't stop if subs are missing!
        }
        if download_subs:
            ydl_opts.update({
                'writesubtitles': True,
                'subtitleslangs': ['en'],
                'writeautomaticsub': True,
                'subtitlesformat': 'best',
            })

        os.makedirs(DOWNLOADS_DIR, exist_ok=True)
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info.get('title', 'video')
            safe_title = safe_filename(title)
            video_filename = os.path.join(DOWNLOADS_DIR, f"{safe_title}.mp4")
            # The file could have a different extension if yt-dlp fails to merge, so find the best match
            if os.path.exists(video_filename):
                last_video_filename = video_filename
            else:
                # fallback to the first mp4 in the dir with the safe_title
                files = [f for f in os.listdir(DOWNLOADS_DIR) if f.startswith(safe_title) and f.endswith('.mp4')]
                if files:
                    last_video_filename = os.path.join(DOWNLOADS_DIR, files[0])
                else:
                    last_video_filename = None

        with progress_lock:
            progress['status'] = 'Completed!'
            progress['percent'] = 100
            progress['done'] = True
            progress['error'] = ''
    except Exception as e:
        with progress_lock:
            progress['status'] = f"Error"
            progress['done'] = True
            progress['error'] = str(e)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form["url"]
        quality = request.form["quality"]
        download_subs = request.form.get("subs") is not None

        os.makedirs(DOWNLOADS_DIR, exist_ok=True)
        with progress_lock:
            progress['status'] = 'Starting...'
            progress['percent'] = 0
            progress['done'] = False
            progress['error'] = ''

        threading.Thread(target=download_video, args=(url, quality, download_subs), daemon=True).start()
        return render_template("progress.html")
    return render_template("index.html")

@app.route("/progress")
def progress_status():
    with progress_lock:
        return jsonify(progress)

@app.route("/download")
def download_file():
    global last_video_filename
    if last_video_filename and os.path.exists(last_video_filename):
        return send_file(last_video_filename, as_attachment=True)
    else:
        return "File not available or not found.", 404

if __name__ == "__main__":
    os.makedirs(DOWNLOADS_DIR, exist_ok=True)
    os.system("termux-open-url http://127.0.0.1:5000/")
    app.run(debug=True, host="0.0.0.0", port=5000)
