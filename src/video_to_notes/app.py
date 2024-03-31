import os
import tempfile
from quart import Quart, request

app = Quart(__name__)
app.config["MAX_CONTENT_LENGTH"] = 500 * 1024 * 1024


@app.route("/upload", methods=["POST"])
async def upload_video():
    """Upload a video file to the server."""
    files = await request.files
    if "video" not in files:
        return "No video file found", 400

    video_file = files["video"]

    if video_file.filename == "":
        return "No selected video file", 400

    if not video_file.filename.lower().endswith(".mp4"):
        return "Invalid file format. Only MP4 files are allowed.", 400

    upload_directory = tempfile.mkdtemp()
    video_path = os.path.join(upload_directory, video_file.filename)
    await video_file.save(video_path)

    return f"Video uploaded successfully. Saved to: {video_path}", 200


if __name__ == "__main__":
    app.run()
