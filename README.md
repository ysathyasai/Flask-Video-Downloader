# 🎬 Flask Video Downloader

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![MIT License](https://img.shields.io/badge/License-MIT%20-blue.svg)](https://choosealicense.com/licenses/mit/)


> [!NOTE]
> Can download YouTube videos easily on your Android device, any pc or laptop using a program (yes also works in Termux) and Flask.

### 🧠 Verdict

- ✅ It works great for Termux / Android use-case.
- 🚫 Not designed for multi-user or production servers.

> [!CAUTION]
> **⚠️ Disclaimer:** This tool is intended for educational purposes only.
> Downloading copyrighted content without permission may violate the terms of service of content providers.
> The author is not responsible for any misuse of this tool.


# 🚀 Introduction

This project provides a lightweight web interface to download YouTube videos directly to your Android device via **Termux**. <details>
  <summary>(Also works on PC or laptop with minor changes)</summary>
  The main change required is replacing the `termux-open-url` command with a cross-platform method to open the browser. On desktop systems, `termux-open-url` will cause an error. You can replace it with the following Python code:

  ```python
  import webbrowser
  webbrowser.open("http://127.0.0.1:5000/")
  ```

  This ensures compatibility across Windows, Linux, and macOS platforms.

</details>

- Built with Flask and yt-dlp, it lets you:

  - Streamline video downloads with a simple web UI 📥

  - Choose video quality up to your preference 🎞️

  - Optionally download subtitles 📄

  - Monitor real-time progress above the progress bar, and yes the progress bar doesn't work. The visual progress bar currently does not update due to an ongoing issue with tracking yt-dlp download events in Flask. If you can solve make a PR! ⏱️


## 🛠️ Implementation Details

### 1. Flask Server: Hosts the web interface and handles routes:

/ – Main form to input URL, quality, subtitles option.

/progress – Returns JSON with download progress.

/download – Serves the completed video file.

### 2. Downloader Thread:

Uses yt-dlp to fetch videos in a background thread.

Custom download_hook updates shared progress dict.

### 3. Safe Filenames:

Filenames normalized to ASCII and stripped of unsafe characters.

### 4. Termux Integration:

On launch, auto-opens the UI in Android’s default browser via termux-open-url.

# 🚀 Running on Your Device

**Follow these steps to get started:**

1. Install Termux on your Android device from the [F-Droid](https://f-droid.org/en/packages/com.termux/) or [GitHub Releases](https://github.com/termux/termux-app/releases).


2. Update packages:

```bash
pkg update && pkg upgrade
```

3. Allow the termux storage access:

```bash
termux-setup-storage
```

4. Install Python & Git:

```bash
pkg install python git
```

5. Clone the repo:

```bash
git clone https://github.com/ysathyasai/Flask-Video-Downloader.git
cd Flask-Video-Downloader
```

- Create virtual environment (optional but recommended):

```bash
python3 -m venv venv
source venv/bin/activate
```

6. Install dependencies:

```bash
pip install -r requirements.txt
```

7. Run the app:

```bash
python app.py
```

8. Use the UI:

> Program will open your browser at http://127.0.0.1:5000/ automatically 📱
>
> Paste a YouTube URL → Select quality → Download it.

> [!TIP]
>Lastly if you want a shortcut to run the program easily then use this command
>
>```bash
>echo '[[ "$PWD" == */Flask-Video-Downloader ]] && alias h="python app.py"' >> ~/.bashrc && source ~/.bashrc
>```

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- Enhanced UI
- Making the progress bar functional
- Adding option to select the subtitles lang.
- Making the terminal interface clean

They are few possible bugs such as,

| **Issue**                                  | **Fix**                                                                 |
|--------------------------------------------|--------------------------------------------------------------------------|
| Storage permission not granted             | Run: `termux-setup-storage`                                             |
|                                            | Allows access to `~/storage/shared/downloads`                             |
| No internet connection                     | Ensure you're connected to the internet                                 |
| Invalid or unsupported YouTube URL         | Check the URL validity                                                  |
|                                            | Add: `if not info: handle error`                                        |
| Filename becomes empty (emoji-only titles) | In `safe_filename()`:                                                   |
|                                            | `if not safe_title: safe_title = "video"`                                |
| Subtitles not available                    | Already handled with `'ignoreerrors': True`                             |
| File deleted before download is accessed   | Already handled with `os.path.exists()`                                 |
| Concurrent downloads overwrite each other  | Use session-based IDs if multi-user or parallel downloads are supported |

If possible use the try/except block's and prompt the user about the issue.

## 📝 License

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details

## 🌟 Show Some Love

Click the ⭐️ on the repo if this helps!

## 📞 Contact

Email: ysathyasai.dev@gmail.com

---
<p align="center">Enjoy and happy downloading! 🎉📲</p>

---
