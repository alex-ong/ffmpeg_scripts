ffmpeg -i "%~1" -ar 44100 -vn -b:a 320k "%~n1-enc.mp3"
