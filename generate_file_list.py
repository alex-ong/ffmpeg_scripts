"""
Grabs all files in the folder, and creates "files.txt"
Only includes .mp4, and sorts by alphabetical
"""
import os

files = os.listdir(".")
files = [file.lower() for file in files]
files = [file for file in files if file.endswith(".mp4")]
files.sort()
files = [f"file '{file}'\n" for file in files]

print(files)

with open("files.txt", "w") as file_list:
    file_list.writelines(files)

print("all done")
