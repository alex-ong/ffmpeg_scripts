rem Converts a single file to h264 (keeps file extension the same)
ffmpeg -hwaccel auto -i "%1" -c:v h264_nvenc -cq:v 19 "%~n1_h264%~x1"
