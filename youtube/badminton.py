from simple_youtube_api.Channel import Channel
from simple_youtube_api.LocalVideo import LocalVideo
from datetime import datetime
import webbrowser

BADMINTON_PLAYLIST = "PLRf65GY9yj9jFmP9tcJLzElc45tpq4if1"

def create_credentials():
    channel = Channel()
    channel.login("client_secret.json", "login_cache.storage")
    return
    
def upload(file_path):
    # login into the channel
    channel = Channel()
    channel.login("client_secret.json", "login_cache.storage")
    
    # setting up the video that is going to be uploaded
    video = LocalVideo(file_path=file_path)

    # setting snippet
    date_string = datetime.now().strftime('%Y-%m-%d')
    video.set_title(f"Badminton {date_string}")
    video.set_description("An excellent badminton video")    
    video.set_default_language("en-US")
    video.set_made_for_kids(False)


    # setting status
    video.set_embeddable(True)    
    video.set_privacy_status("unlisted")
    video.set_public_stats_viewable(True)
    # this doesnt work coz library broken.
    # video.set_playlist(BADMINTON_PLAYLIST)

    # uploading video and printing the results
    video = channel.upload_video(video)
    print(video.id)

    # liking video
    video.like()
    
    channel.add_video_to_playlist(BADMINTON_PLAYLIST, video.id)
    
    # open the edit page
    url = f"https://studio.youtube.com/video/{video.id}/edit"
    webbrowser.open(url, new=0, autoraise=True)    
        