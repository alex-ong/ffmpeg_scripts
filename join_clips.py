"""
Grabs all files in the folder, and creates "files.txt"
Only includes .mp4, and sorts by alphabetical
"""
import os
import subprocess
import sys


def create_filelist(root=""):
    files = os.listdir(root)
    files = [file.lower() for file in files]
    files = [file for file in files if file.endswith(".mp4")]
    files.sort()
    files = [f"file '{root}{file}'\n" for file in files]

    print(files)

    with open(f"{root}files.txt", "w") as file_list:
        file_list.writelines(files)


def render(root="", output_name="output.mp4"):
    command = (
        f"ffmpeg -f concat -safe 0 -i {root}files.txt -c:v copy {root}{output_name}"
    )
    subprocess.call(command.split())  # can't use .run because MacOS is PoS


if __name__ == "__main__":
    # python join_clips.py T:/VideoEdit/Goodminton-20221116/clips/
    root = ""
    if len(sys.argv) >= 2:
        root = sys.argv[1]
        root = root.replace("\\", "/")
        if not root.endswith("/"):
            root = root + "/"

    create_filelist(root)
    render(root)
