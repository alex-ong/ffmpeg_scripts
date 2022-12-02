from youtube.badminton import upload, create_credentials
import sys

# Usage: first time, run with no args; this will create the credentials file
# After that, pass in the file you want to upload
if __name__ == "__main__":
    file_path = None
    if len(sys.argv) >= 2:
        file_path = sys.argv[1]
        upload(file_path)
    else:
        create_credentials()
        