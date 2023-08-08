import os
import json5
import subprocess
import sys


def process_file(file_name, root):
    clips_dir = os.path.join(root, "clips")
    os.makedirs(clips_dir, exist_ok=True)
    with open(root + file_name) as file:
        data = json5.load(file)
        video_file = data["mediaFileName"]
        for index, item in enumerate(data["cutSegments"]):
            process_clip(video_file, item, index, root)


def process_clip(file_name, clip_info, index, root):
    clips_dir = os.path.join(root, "clips")
    print(file_name, clip_info, index, clips_dir)
    file_name_no_ext = os.path.splitext(file_name)[0]
    start_str = f'-ss {clip_info["start"]}' if "start" in clip_info else ""
    end_str = f'-to {clip_info["end"]}' if "end" in clip_info else ""
    command = f'ffmpeg -hwaccel auto {start_str} {end_str} -i "{root}{file_name}" -c:v h264_nvenc -cq:v 19 "{clips_dir}/{file_name_no_ext}-{index}.mp4"'
    subprocess.run(command)


def main(root="", file=None):
    if file is None:
        if root != "":
            root += "/"
        for file in os.listdir(root):
            if file.endswith("-proj.llc"):
                process_file(file, root)
    else:
        process_file(file, root)


if __name__ == "__main__":
    # A folder with llc's inside (notice the trailing slash)
    # python render_proj.py T:/VideoEdit/Goodminton-20221116/raw/

    # A single llc
    # python render_proj.py T:/VideoEdit/Goodminton-20221116/raw/GX010026-proj.llc
    if len(sys.argv) >= 2:
        root, file = os.path.split(sys.argv[1])
        if len(root) == 0:
            root = ""
        if len(file) == 0:
            file = None
        main(root, file)
    # Scans current directory
    else:
        main()
