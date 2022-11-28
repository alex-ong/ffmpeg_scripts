"""
Renders a folder of lossless-cut files (.llc) with associated videos
"""
import os
import json5
import ast
import subprocess


def process_file(file_name):
    """processes a single llc file; making several clips"""
    os.makedirs("clips", exist_ok=True)
    with open(file_name) as file:
        data = json5.load(file)
        video_file = data["mediaFileName"]
        for index, item in enumerate(data["cutSegments"]):
            process_clip(video_file, item, index)


def process_clip(file_name, clip_info, index):
    """Render a single clip"""
    print(file_name, clip_info, index)
    file_name_no_ext = os.path.splitext(file_name)[0]
    start_str = f'-ss {clip_info["start"]}' if "start" in clip_info else ""
    end_str = f'-to {clip_info["end"]}' if "end" in clip_info else ""
    command = f'ffmpeg -hwaccel auto {start_str} {end_str} -i "{file_name}" -c:v h264_nvenc -cq:v 19 "clips/{file_name_no_ext}-{index}.mp4"'
    subprocess.run(command)


def main():
    """process everything in the current directory"""
    for file in os.listdir("."):
        if file.endswith("-proj.llc"):
            process_file(file)


if __name__ == "__main__":
    main()
