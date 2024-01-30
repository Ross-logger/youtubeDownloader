from pytube import YouTube
import os
import re

DEFAULT_DOWNLOAD_PATH = "~/Desktop/downloadedYoutubeVideos"


def is_youtube_link(link):
    pattern = r"(?:https?:\/\/)?(?:www\.)?youtu(?:\.be|be\.com)\/(?:watch\?v=|embed\/|v\/)?([\w\-]+)"
    match = re.match(pattern, link)
    return match is not None


def get_valid_youtube_link():
    link = input("Please, input the link to the video for downloading: ")

    try:
        YouTube(link)
        return link

    except Exception as e:
        print("An error occurred while processing the YouTube link:", str(e))
        return get_valid_youtube_link()


link = get_valid_youtube_link()

youtube = YouTube(link)

print("Title:", youtube.title)

print("Author: ", youtube.author)

# getting the resolution from user needed if 0 is input then the highest resolution video is downloaded

resolution = input(
    'Please, input (a number, 360, 720, 1080 etc.) the needed resolution or input "0" to download the best resolution: ')

while True:
    try:
        resolution = int(resolution)
        break
    except ValueError:
        resolution = input("Please, input the NUMBER (360, 720, 1080 etc.): ")

if resolution == 0:
    stream = youtube.streams.get_highest_resolution()
else:
    stream = youtube.streams.get_by_resolution(resolution)


# getting the path to download the youtube video - if it does not exist just create it

def downloadStream(stream, path):
    if stream is not None:
        print("Downloading...")
        stream.download(path)
        print("Download complete!")
    else:
        print("No stream available for the specified resolution.")


path = input("Please, input the full path where the video need to be saved: ")

default_path = os.path.expanduser(DEFAULT_DOWNLOAD_PATH)

if os.path.exists(path) and os.path.isdir(path):
    if os.path.exists(os.path.join(path, youtube.title + ".mp4")):
        print("The video file already exists in the specified directory.")
    else:
        downloadStream(stream, path)
else:
    if os.path.exists(os.path.join(default_path, youtube.title + ".mp4")):
        print("The video file already exists in the specified directory.")
    elif not os.path.exists(default_path):
        os.makedirs(default_path)
        print("The path you entered does not exist - but I got you back and created one in your Desktop!")
        downloadStream(stream, default_path)
    else:
        print(f"The path you entered does not exist - the video will be downloaded in {default_path}")
        downloadStream(stream, default_path)