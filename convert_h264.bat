ffmpeg -i "%1" -c:v h264_nvenc -cq:v 19 "%~n1_h264%~x1"
