"""
Simple autocropper based on putting hand in front of camera
Hardcoded to 50fps
"""
import os
import subprocess
import sys


def process_video():
    """
    Reads output.mp4 and spits out time.txt
    """
    os.makedirs("temp", exist_ok=True)

    FIFTY_FPS = 'ffmpeg -skip_frame nokey -an -hwaccel auto -i output.mp4 -vsync 0 -vf "setpts=expr=N/50/TB,scale=1280:720" -c:v hevc_nvenc output_50fps.mp4'
    subprocess.run(FIFTY_FPS, shell=True, check=True)

    ONE_FPS = (
        "ffmpeg -itsscale 50 -i output_50fps.mp4 -r 1 -an -c:v copy output_3fps.mp4"
    )
    subprocess.run(ONE_FPS, shell=True, check=True)

    SCENE_DIFF = "ffmpeg -i output_3fps.mp4 -filter_complex \"select='gt(scene,0.15)',metadata=print:file=time.txt\" -vsync vfr temp/img%03d.png"
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

    return [seconds_to_str(time) for time in times]


def seconds_to_str(seconds):
    """convert from pure seconds to HH:MM:SS"""
    return f"{seconds//3600:02}:{seconds%3600:02}:{seconds%60:02}"


if __name__ == "__main__":
    print(sys.argv)
    DIRECTORY = sys.argv[1]
    os.chdir(DIRECTORY)

    process_video()
    output = process_text()
    with open("youtube.txt", "w", encoding="utf8") as file:
        file.writelines("\n".join(output))
