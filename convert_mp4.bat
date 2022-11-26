rem Converts a single file to h264, and change container to mp4
ffmpeg -hwaccel auto -i "%1" -c:v h264_nvenc -cq:v 19 "%~n1.mp4"
