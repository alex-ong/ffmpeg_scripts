"""
Grabs all files in the folder, and creates "files.txt"
Only includes .mp4, and sorts by alphabetical
"""
import os

def create_filelist()
    files = os.listdir(".")
    files = [file.lower() for file in files]
    files = [file for file in files if file.endswith(".mp4")]
    files.sort()
    files = [f"file '{file}'\n" for file in files]

    print(files)

    with open("files.txt", "w") as file_list:
        file_list.writelines(files)

def render():
    command = "ffmpeg -f concat -safe 0 -i files.txt -c:v copy output.mp4"
    subprocess.run(command)
    
if __name__ == "__main__":
    create_filelist()
    render()    