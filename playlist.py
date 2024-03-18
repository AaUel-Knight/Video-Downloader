import tkinter as tk
from tkinter import filedialog
import os
import subprocess
from pytube import YouTube
import random
import requests
import re
import string

BASE_DIR = os.getcwd()

def foldertitle(url):
    try:
        res = requests.get(url)
    except:
        print('no internet')
        return False
    plain_text = res.text

    if 'list=' in url:
        eq = url.rfind('=') + 1
        cPL = url[eq:]
    else:
        print('Incorrect attempt.')
        return False
    return cPL

def link_snatcher(url):
    our_links = []
    try:
        res = requests.get(url)
    except:
        print('no internet')
        return False

    plain_text = res.text

    if 'list=' in url:
        eq = url.rfind('=') + 1
        cPL = url[eq:]
    else:
        print('Incorrect Playlist.')
        return False

    tmp_mat = re.compile(r'watch\?v=\S+?list=' + cPL)
    mat = re.findall(tmp_mat, plain_text)

    for m in mat:
        new_m = m.replace('&amp;', '&')
        work_m = 'https://youtube.com/' + new_m
        if work_m not in our_links:
            our_links.append(work_m)
    return our_links

def download_file():
    url = url_entry.get()
    our_links = link_snatcher(url)
    SAVEPATH = save_path_entry.get()
    user_res = user_res_entry.get()

    os.chdir(BASE_DIR)
    try:
        os.mkdir(SAVEPATH[:7])
    except:
        print('folder already exists')

    os.chdir(SAVEPATH[:7])
    x = []
    for root, dirs, files in os.walk(".", topdown=False):
        for name in files:
            pathh = os.path.join(root, name)
            if os.path.getsize(pathh) < 1:
                os.remove(pathh)
            else:
                x.append(str(name))

    for link in our_links:
        try:
            yt = YouTube(link)
            main_title = yt.title
            main_title = main_title + '.mp4'
            main_title = main_title.replace('|', '')
        except:
            print('connection problem..unable to fetch video info')
            break
        if main_title not in x:
            if user_res == '360p' or user_res == '720p':
                vid = yt.streams.filter(progressive=True, file_extension='mp4', res=user_res).first()
                print('Downloading. . . ' + vid.default_filename + ' and its file size -> ' + str(round(vid.filesize / (1024 * 1024), 2)) + ' MB.')
                progress_text.set(f'Downloading. . . {vid.default_filename} and its file size -> {str(round(vid.filesize / (1024 * 1024), 2))} MB.')
                vid.download(SAVEPATH)
                progress_text.set('Playlist Downloaded')
            else:
                print('something is wrong.. please rerun the script')
        else:
            print(f'\n skipping "{main_title}" video \n')

#    window.destroy()

window = tk.Tk()
window.title("Playlist Downloader")
url_label = tk.Label(window, text="Enter Playlist URL:", width=100)
url_label.pack()
url_entry = tk.Entry(window, width=75)
url_entry.pack()
save_path_label = tk.Label(window, text="Enter Save Path:")
save_path_label.pack()
save_path_entry = tk.Entry(window, width=75)
save_path_entry.pack()
resolution_label = tk.Label(window, text="Choose Resolution (360p or 720p):")
resolution_label.pack()
user_res_entry = tk.Entry(window, width=75)
user_res_entry.pack()
download_button = tk.Button(window, text="Download Playlist", command=download_file)
download_button.pack()
progress_text = tk.StringVar()
space = tk.Label(window, text="     ", height=3)
space.pack()
text_label = tk.Label(window, textvariable=progress_text)
text_label.pack()
window.mainloop()
