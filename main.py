import shutil

ffmpeg_path = shutil.which('ffmpeg')
if ffmpeg_path:
    print(f"FFmpeg executable found at: {ffmpeg_path}")
else:
    print("FFmpeg is not installed or not in the system PATH.")