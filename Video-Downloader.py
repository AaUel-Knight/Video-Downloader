import os
from pytube import YouTube

def video_downloader(url, resolution, save_path):
    try:
        yt = YouTube(url)
        main_title = yt.title
        main_title = main_title + '.mp4'
        main_title = main_title.replace('|', '')
        # You can check available resolutions using: )
        vid = yt.streams.filter(progressive=True, file_extension='mp4', res=resolution).first()
        print(yt.streams.all())
        save_folder = os.path.join(save_path, 'videos')
        os.makedirs(save_folder, exist_ok=True)
        save_path = os.path.join(save_folder, main_title)
        print(f'Downloading. . . {main_title} and its file size -> {round(vid.filesize / (1024 * 1024), 2)} MB.')
        vid.download(save_folder)
        print('Video Downloaded')
    except Exception as e:
        print(f'Error downloading video: {e}')

# BASE_DIR and other initial setup code remains unchanged
print('WELCOME TO VIDEO DOWNLOADER')
url = str(input("\nSpecify the video URL\n"))
print('\nCHOOSE ANY ONE - TYPE 360P OR 720P\n')
user_res = str(input()).lower()
save_path = str(input("\nEnter the directory where you want to save the video (press Enter for current directory):\n"))

if not save_path:
    save_path = os.getcwd()

print('...You chose ' + user_res + ' resolution\n.')
print('\nConnecting . . .\n')
video_downloader(url, user_res, save_path)
print('Downloading finished')
print(f'\nYour video is saved at --> {os.path.join(save_path, "videos")}')

