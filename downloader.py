import pafy
import youtube_dl as ydl
import os, os.path
from os import path
from util import * 
from tkinter import messagebox
import requests
from PIL import ImageTk, Image

illegal_chars = ('*','<', '>', ':', '"', '/', '\\', '|', '?', '*')

def validate(url, file_name, dl_path, is_playlist, use_video_title):
    if not url:
        messagebox.showwarning("Warning", "Please enter a link to a YouTube video or playlist.")   
        return
    elif not is_playlist and 'playlist' in url:
        messagebox.showwarning("Warning", "The link you entered is a playlist link. If you would like to download a playlist, please check the 'Playlist' box on the right before downloading.")
        return
    elif is_playlist and 'playlist' not in url:
        messagebox.showwarning("Warning", "The link you entered is not a playlist. Please uncheck the 'Download Playlist' box if you would like to download audio from a single video.")
        return        
    else:
        try:
            r =requests.get(url)
            if r.status_code != 200:
                messagebox.showwarning("Error", "Cannot reach the YouTube link.")    
                return           
        except:
            messagebox.showerror("Error", "Error reaching the YouTube link.")
            return

    # todo in case use_video_title is True, check if the video title can be a valid file name
    if not use_video_title and not file_name:
        messagebox.showwarning("Warning", "Please enter a name for your file or check the 'Use Video Title' box.")
        return        

    if not dl_path:
        messagebox.showwarning("Warning", "Please enter a download path.")
        return
    else:
        if not path.isdir(dl_path):
            messagebox.showwarning("Error", "Download path is invalid.")
            return

    return True


def download_audio(url, file_name, dl_path, is_playlist, use_video_title, root=None, progress_bar=None):
    # Receives callback data (must include all 5 parameters) and updates prgress bar
    def update_progress(total, recvd, ratio, rate, eta):
        progress_bar['value'] = int(ratio*100)
        root.update_idletasks()


    def download_playlist():
        with ydl.YoutubeDL() as playlist:

            playlist = playlist.extract_info(url, download=False)
            playlist_title = playlist.get('title')
            videos = playlist['entries']
            if len(videos) > 3:
                confirmation = messagebox.askquestion("Playlist Download", 
                f'You are about to download a playlist containing {len(videos)} songs. Are you sure you want to download it?', icon='warning')
                if confirmation != 'yes':
                    return
            if use_video_title:
                for char in playlist_title:
                    if char in illegal_chars:
                        playlist_title = playlist_title.replace(char, "")
                file_name = playlist_title
            try:
                os.mkdir(dl_path+f"\\{file_name}")
            except FileExistsError:
                pass    

            for video in videos:
                video_url = f"https://www.youtube.com/watch?v={video['id']}"
                download_audio(video_url, video['title'], dl_path+f"\\{file_name}", False, use_video_title, root, progress_bar)

    if is_playlist:
        download_playlist()
    else:
        try:
            video = pafy.new(url)
            bestaudio = video.getbestaudio()
        except OSError:
            messagebox.showerror("Error", f"Cannot access the YouTube video. It may be a private video.")
            return
        except:
            messagebox.showerror("Error", f"Cannot access the YouTube video. It may be a deleted or private video.")         
            return
           
        if use_video_title:
            file_name = video.title    
            for char in file_name:
                if char in illegal_chars:
                        file_name = file_name.replace(char, "")
                
        bestaudio.download(filepath=f'{dl_path}/{file_name}.mp3', quiet=True, callback=update_progress)
    
# Scrape thumbnail
def get_thumbnail(url, thumbnail_preview):
    try:
        clear_thumbnail(thumbnail_preview)
        # Load video thumbnail
        video = pafy.new(url, basic=False)
        thumbnail_url = video.thumb
        # Save thumbnail in temp
        temp = open(full_path(f"temp\\temp.jpg"),'wb')
        temp.write(requests.get(thumbnail_url).content)
        temp.close()
        # Load temp thumbnail into tkinter
        thumbnail = ImageTk.PhotoImage(Image.open(full_path(f"temp\\temp.jpg")))
        thumbnail_preview.config(image=thumbnail)
        thumbnail_preview.photo = thumbnail
        thumbnail_preview.grid(row=0, column=2, sticky='n')
    except ValueError:
        messagebox.showerror("Error", "Error fetching thumbnail. Make sure the link you entered is valid and not a playlist link.")

# Clera the temp folder and hide thumbnail preview
def clear_thumbnail(thumbnail_preview):
    try:
        path = full_path('temp')
        for file in os.listdir(path):
            os.remove(os.path.join(path, file))
        thumbnail_preview.grid_forget()
    except:
        pass


