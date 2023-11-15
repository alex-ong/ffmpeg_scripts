"""
Simple autocropper based on putting hand in front of camera
Hardcoded to 50fps
"""
import json
import os
import shutil
import subprocess
import sys

import join_clips


def process_keyframes(src, temp_dir):
    """Given a src file, create new 1fps video that is just keyframes"""
    length = get_video_data(src)
    num_segments = 4
    segment_size = length / num_segments
    segments = [
        (int(i * segment_size), int((i + 1) * segment_size))
        for i in range(num_segments)
    ]
    tasks = []
    for index, (seg_start, seg_end) in enumerate(segments):
        task = extract_keyframes(src, temp_dir, seg_start, seg_end, index)
        tasks.append(task)

    print("waiting for our video segments to finish exporting...")
    for sub_process, _ in tasks:
        sub_process.wait()

    print("creating big file")
    join_clips.create_filelist(temp_dir + "/")
    join_clips.render(temp_dir + "/", "output_50fps.mp4")
    print("created big file")
    return temp_dir + "/output_50fps.mp4"


def extract_keyframes(src, temp_dir, start, end, index) -> (subprocess.Popen, str):
    """given a src file and start/end/index, extract part of the keyframes"""
    length = end - start
    output = os.path.join(temp_dir, f"output_50fps_{index}.mp4").replace("\\", "/")
    # fmt: off
    command = [
        "ffmpeg", "-y",
        "-skip_frame", "nokey",
        "-an",
        "-hwaccel", "auto",
        "-ss", str(start),
        "-t", str(length),
        "-i", src,
        "-vsync", "0",
        "-vf", "setpts=expr=N/50/TB,scale=1280:720",
        "-c:v", "hevc_nvenc",
        output
    ]
    # fmt: on
    print(command)

    process = subprocess.Popen(
        command, shell=True, creationflags=subprocess.DETACHED_PROCESS
    )

    return (process, output)


def get_video_data(filename):
    """returns duration of file"""
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "quiet",
            "-print_format",
            "json",
            "-show_format",
            "-show_streams",
            filename,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=True,
    )
    json_str = result.stdout
    data = json.loads(json_str)

    for stream in data["streams"]:
        if stream["codec_type"] == "video":
            return float(stream["duration"])

    return None


def process_video(directory: str):
    """
    Reads output.mp4 and spits out time.txt
    """
    src = os.path.join(directory, "output.mp4").replace("\\", "/")
    temp_dir = os.path.join(directory, "temp").replace("\\", "/")
    shutil.rmtree(temp_dir, ignore_errors=True)
    os.makedirs(temp_dir, exist_ok=True)
    keyframed_file = process_keyframes(src, temp_dir)

    print("overwriting fps from 50 back down to 1")
    ONE_FPS = f"ffmpeg -itsscale 50 -i {keyframed_file} -r 1 -an -c:v copy {temp_dir}/1fps.mp4"
    subprocess.run(ONE_FPS, shell=True, check=True)

    print("exporting timestamps to time.txt")
    SCENE_DIFF = (
        f"ffmpeg -i {temp_dir}/1fps.mp4"
        + " -filter_complex \"select='gt(scene,0.15)',metadata=print:file=time.txt\""
        + " -vsync vfr temp/img%03d.png"
    )
    # print(scene_diff)
    subprocess.run(SCENE_DIFF, shell=True, check=True)


def process_text():
    """open time.txt, export youtube.txt"""
    times = []

    last_time = 0
    with open("time.txt", "r", encoding="utf8") as file:
        for line in file:
            if line.startswith("frame"):
                elements = line.split()
                time = int(elements[2].split(":")[1])
                if time - last_time > 20:
                    times.append(last_time)
                last_time = time
        times.append(last_time)

    lines = [seconds_to_str(time) for time in times]
    with open("youtube.txt", "w", encoding="utf8") as file:
        file.writelines("\n".join(lines))


def seconds_to_str(seconds):
    """convert from pure seconds to HH:MM:SS"""
    return f"{seconds//3600:02}:{seconds%3600:02}:{seconds%60:02}"


if __name__ == "__main__":
    print(sys.argv)
    DIRECTORY = sys.argv[1]
    process_video(DIRECTORY)
    process_text()
