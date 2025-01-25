from flask import Flask, request, render_template, send_file
import os
import yt_dlp

app = Flask(__name__)

# Ensure the 'downloads' folder exists
DOWNLOAD_FOLDER = "downloads"
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_video():
    video_url = request.form['video_url']
    try:
        ydl_opts = {
            'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
            'format': 'bestvideo+bestaudio/best',
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=True)
            video_title = info_dict.get('title', None)
            video_file = ydl.prepare_filename(info_dict)
        
        # Serve the downloaded file to the user
        return send_file(
            video_file,
            as_attachment=True,
            download_name=os.path.basename(video_file),
        )
    except Exception as e:
        return render_template(
            'index.html',
            message=f"An error occurred: {e}. Please check the URL or try again later."
        )

if __name__ == "__main__":
    app.run(debug=True)
