import os
import re
import requests
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pytube import YouTube
from time import time

def foldertitle(url):
    try:
        res = requests.get(url)
    except:
        messagebox.showerror('Error', 'No internet connection')
        return False
    plain_text = res.text

    if 'list=' in url:
        eq = url.rfind('=') + 1
        cPL = url[eq:]
    else:
        messagebox.showerror('Error', 'Incorrect playlist URL')
        return False
    return cPL

def link_snatcher(url):
    our_links = []
    try:
        res = requests.get(url)
    except:
        messagebox.showerror('Error', 'No internet connection')
        return False

    plain_text = res.text

    if 'list=' in url:
        eq = url.rfind('=') + 1
        cPL = url[eq:]
    else:
        messagebox.showerror('Error', 'Incorrect playlist URL')
        return False

    tmp_mat = re.compile(r'watch\?v=\S+?list=' + cPL)
    mat = re.findall(tmp_mat, plain_text)
    
    for m in mat:
        new_m = m.replace('&amp;', '&')
        work_m = 'https://youtube.com/' + new_m
        if work_m not in our_links:
            our_links.append(work_m)
    return our_links

def update_progress(stream, chunk, file_handle, bytes_remaining, file_size, start_time, progress_bar, label_status, video_title):
    bytes_downloaded = file_size - bytes_remaining
    progress = (bytes_downloaded / file_size) * 100
    elapsed_time = time() - start_time
    download_speed = bytes_downloaded / elapsed_time / 1024  # KB/s
    remaining_time = (bytes_remaining / download_speed / 1024) if download_speed != 0 else 0  # seconds
    progress_bar['value'] = progress
    label_status.config(text=f'Downloading: {video_title} - {round(progress, 2)}% '
                             f'- Speed: {round(download_speed, 2)} KB/s, Remaining: {int(remaining_time)} s')
    root.update_idletasks()

def download_video(yt, resolution, save_path, progress_bar, label_status):
    try:
        video_title = yt.title
        main_title = video_title + '.mp4'
        main_title = main_title.replace('|', '')
        save_file_path = os.path.join(save_path, main_title)

        vid = yt.streams.filter(progressive=True, file_extension='mp4', res=resolution).first()
        file_size = vid.filesize
        start_time = time()

        with open(save_file_path, 'wb') as file_handle:
            for chunk in vid.stream_to_buffer():
                file_handle.write(chunk)
                update_progress(vid, chunk, file_handle, vid.filesize - file_handle.tell(), file_size, start_time, progress_bar, label_status, video_title)

        progress_bar['value'] = 100
        label_status.config(text=f'Completed: {video_title}')
    except Exception as e:
        label_status.config(text=f'Error: {str(e)}')

def start_download():
    url = entry_url.get()
    resolution = combobox_resolution.get()
    save_path = filedialog.askdirectory()

    if not url or not resolution or not save_path:
        messagebox.showerror('Error', 'Please fill in all fields and select a folder')
        return

    our_links = link_snatcher(url)
    if not our_links:
        return

    for link in our_links:
        try:
            yt = YouTube(link)
        except Exception as e:
            label_status.config(text=f'Error fetching video info: {str(e)}')
            return

        main_title = yt.title + '.mp4'
        main_title = main_title.replace('|', '')
        save_file_path = os.path.join(save_path, main_title)

        if not os.path.exists(save_file_path):
            download_video(yt, resolution, save_file_path, progress_bar, label_status)
        else:
            label_status.config(text=f'Skipping: {main_title} (already exists)')

    label_status.config(text='All downloads completed')

# Set up the GUI
root = tk.Tk()
root.title("YouTube Playlist Downloader")

frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

label_url = ttk.Label(frame, text="Playlist URL:")
label_url.grid(row=0, column=0, pady=5)

entry_url = ttk.Entry(frame, width=40)
entry_url.grid(row=0, column=1, pady=5)

label_resolution = ttk.Label(frame, text="Resolution:")
label_resolution.grid(row=1, column=0, pady=5)

combobox_resolution = ttk.Combobox(frame, values=["360p", "720p"])
combobox_resolution.grid(row=1, column=1, pady=5)
combobox_resolution.current(0)

button_download = ttk.Button(frame, text="Download", command=start_download)
button_download.grid(row=2, column=1, pady=10)

progress_bar = ttk.Progressbar(frame, orient="horizontal", length=300, mode="determinate")
progress_bar.grid(row=3, column=0, columnspan=2, pady=10)

label_status = ttk.Label(frame, text="")
label_status.grid(row=4, column=0, columnspan=2)

root.mainloop()
