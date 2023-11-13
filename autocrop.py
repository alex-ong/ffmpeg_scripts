import os
import subprocess
import sys

def process_video2():
    os.makedirs("temp", exist_ok=True)
    FIFTY_FPS = 'ffmpeg -skip_frame nokey -an -hwaccel auto -i output.mp4 -vsync 0 -vf "setpts=expr=N/50/TB,scale=1280:720" -c:v hevc_nvenc output_50fps.mp4'
    subprocess.run(FIFTY_FPS, shell=True)
    ONE_FPS = "ffmpeg -itsscale 50 -i output_50fps.mp4 -r 1 -an -c:v copy output_3fps.mp4"
    subprocess.run(ONE_FPS, shell=True)
    SCENE_DIFF = "ffmpeg -i output_3fps.mp4 -filter_complex \"select='gt(scene,0.3)',metadata=print:file=time.txt\" -vsync vfr temp/img%03d.png"
    #print(scene_diff)
    subprocess.run(SCENE_DIFF, shell=True)
    
def process_video():
    os.makedirs("temp", exist_ok=True)
    # 24 minutes for 2.25 hour video
    ONE_FPS = "ffmpeg -c:v hevc_cuvid -resize 1280x720 -i output.mp4 -c:v h264_nvenc -vf fps=fps=1 -an output_1fps.mp4"
    subprocess.run(ONE_FPS, shell=True)
    # 20 seconds to process...
    SCENE_DIFF = "ffmpeg -i output_1fps.mp4 -filter_complex \"select='gt(scene,0.3)',metadata=print:file=time.txt\" -vsync vfr temp/img%03d.png"
    #print(scene_diff)
    subprocess.run(SCENE_DIFF, shell=True)

def process_text():
    times = []
    
    last_time = 0
    with open("time.txt", "r") as file:
        for line in file:
            if line.startswith("frame"):
                elements = line.split()
                time = int(elements[2].split(":")[1])
                if time - last_time > 20:
                    times.append(last_time)
                last_time = time
        times.append(last_time)
    
    return [seconds_to_str(time) for time in times]

def seconds_to_str(s):
    return "{:02}:{:02}:{:02}".format(s//3600, s%3600//60, s%60)

if __name__ == "__main__":
    print(sys.argv)
    directory = sys.argv[1]
    os.chdir(directory)
    process_video2()
    output = process_text()
    with open("youtube.txt", "w", encoding="utf8") as file:
        file.writelines("\n".join(output))