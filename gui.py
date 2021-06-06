from tkinter import *
from config import *
from downloader import *
from tkinter import messagebox, filedialog
from tkinter.ttk import Progressbar


# Window -------------------------------------------------
root = Tk()
root.title('Youtube MP3 Downloader')
root.geometry(f'{WIN_WIDTH}x{WIN_HEIGHT}+500+150') 
root.config(bg=BG_COLOR)
root.resizable(width=False,height=True)
default_path = get_default_path()
is_playlist = BooleanVar()
use_video_title = BooleanVar()

# Methods------------------------------------------------
def clear_all():
    url_entry.delete('0', END)
    file_name_entry.delete('0', END)
    dl_path_entry.delete('0', END)


def load_default_path():
    dl_path_entry.delete('0', END)    
    dl_path_entry.insert('0', get_default_path())


def get_info():
    messagebox.showinfo("About", ABOUT_MSG)


def get_help():
    messagebox.showinfo("Instructions", HELP_MSG)


# Change the "File Name" label to "Playlist Name" if the playlist option is checked
def edit_name_label(event):
    if not event.get():
        file_name_label.config(text= 'File Name: ') 
        use_video_title_check.config(text='Use Video Title')
        root.update()
        return
    file_name_label.config(text= 'Playlist Name: ') 
    use_video_title_check.config(text='Use Playlist Title')
    root.update()

# Disable file name input if user wants to use video title as file name
def edit_name_entry(event):
    if not event.get():
        file_name_entry.config(state=NORMAL)
        return
    file_name_entry.delete('0', END)    
    file_name_entry.config(state=DISABLED)      

# Start download process
def start_download():
    if validate(url_entry.get(), file_name_entry.get(), dl_path_entry.get(), is_playlist.get(), use_video_title.get()):
        progress.grid(row=4, column=2, sticky='ew') 
        root.update_idletasks()
        download_audio(url_entry.get(), file_name_entry.get(), dl_path_entry.get(), is_playlist.get(), use_video_title.get(), root, progress)
        progress.grid_forget()

# Set the download path
def set_path(path):
    dl_path_entry.delete('0', END)    
    dl_path_entry.insert('0', path)    

# File dialog to select path
def select_path():
    path = filedialog.askdirectory(parent=root, initialdir= get_default_path(), title='Please select a directory')
    if path:
        set_path(path)


# Components ---------------------------------------------
thumbnail_preview = Label(root, bg=BG_COLOR, image = "")

url_label = Label(root, text="YouTube Link: ", bg=BG_COLOR, font=DEFAULT_FONT, fg=FONT_COLOR)
url_label.grid(row=1, column=0, sticky='w',padx=5)

url_entry = Entry(root, width=60,  bg=ENTRY_COLOR, fg=FONT_COLOR, font=DEFAULT_FONT, relief=FLAT, insertbackground=FONT_COLOR)
url_entry.grid(row=1, column=1, sticky='w',pady=10, columnspan=5)

#---
play_list_check = Checkbutton(root, text = "Download Playlist", font=SMALL_FONT, relief=FLAT, 
bg=BG_COLOR, fg=FONT_COLOR, selectcolor=TOP_COLOR, activebackground=BG_COLOR,activeforeground=FONT_COLOR, 
variable=is_playlist, command=lambda: edit_name_label(is_playlist), onvalue=True, offvalue=False)
play_list_check.grid(row=1, column=4, padx=5, columnspan=3, sticky='w')

#---
show_thumbnail_button = Button(root, text="Show Thumbnail", relief=FLAT, bg = BTN_COLOR, fg = FONT_COLOR, 
command= lambda: get_thumbnail(url_entry.get(), thumbnail_preview), 
activebackground=BTN_PRESSED_COLOR, activeforeground=FONT_COLOR, font=SMALL_FONT, height=1)
show_thumbnail_button.grid(row=1, column=7)


#----
file_name_label = Label(root, text="File Name: ", bg=BG_COLOR, font=DEFAULT_FONT, fg=FONT_COLOR )
file_name_label.grid(row=2, column=0, sticky='w', padx=5)

file_name_entry = Entry(root, width=60, bg=ENTRY_COLOR, fg=FONT_COLOR, font=DEFAULT_FONT, 
relief=FLAT, disabledbackground=BG_COLOR, insertbackground=FONT_COLOR)
file_name_entry.grid(row=2, column=1, sticky='w',pady=10, columnspan=5)

use_video_title_check = Checkbutton(root, text = "Use Video Title", font=SMALL_FONT, relief=FLAT, 
bg=BG_COLOR, fg=FONT_COLOR, selectcolor=TOP_COLOR, activebackground=BG_COLOR,activeforeground=FONT_COLOR, 
variable=use_video_title, command=lambda: edit_name_entry(use_video_title), onvalue=True, offvalue=False)
use_video_title_check.grid(row=2, column=4, padx=5, columnspan=3,sticky='w')

#----
dl_path_label = Label(root, text="Download Path: ", bg=BG_COLOR, font=DEFAULT_FONT, fg=FONT_COLOR )
dl_path_label.grid(row=3, column=0, sticky='w', padx=5)

dl_path_entry = Entry(root, width=60, bg=ENTRY_COLOR, fg=FONT_COLOR,  font=DEFAULT_FONT, 
relief=FLAT, insertbackground=FONT_COLOR)
dl_path_entry.grid(row=3, column=1, sticky='w',pady=10, columnspan=3)
dl_path_entry.insert("0", default_path)
#---

select_path_button = Button(root, text="Open", relief=FLAT, bg = BTN_COLOR, fg = FONT_COLOR, 
command= select_path, activebackground=BTN_PRESSED_COLOR, activeforeground=FONT_COLOR, font=SMALL_FONT, height=1)
select_path_button.grid(row=3, column=4, padx=3)

# ---
load_path_button = Button(root, text="Load", relief=FLAT, bg = BTN_COLOR, fg = FONT_COLOR, 
command= load_default_path, activebackground=BTN_PRESSED_COLOR, activeforeground=FONT_COLOR, font=SMALL_FONT, height=1)
load_path_button.grid(row=3, column=5)

#---
save_path_button = Button(root, text="Save", relief=FLAT, bg = BTN_COLOR, fg = FONT_COLOR, 
command=lambda: set_default_path(dl_path_entry.get()), 
activebackground=BTN_PRESSED_COLOR, activeforeground=FONT_COLOR, font=SMALL_FONT, height=1)
save_path_button.grid(row=3, column=6)

#---
download_button = Button(root, text="Download", relief=FLAT, bg = BLUE, fg = FONT_COLOR, 
command=lambda: start_download(), activebackground=DARK_BLUE, activeforeground=FONT_COLOR, font=SMALL_FONT)
download_button.grid(row=4, column=1, sticky='w', pady=10)

#---
clear_button = Button(root, text="Clear All", relief=FLAT, bg = RED, fg = FONT_COLOR, 
command=clear_all, activebackground=DARK_RED, activeforeground=FONT_COLOR, font=SMALL_FONT)
clear_button.grid(row=4, column=4, padx=5, columnspan=2, sticky='w')

#---
help_button = Button(root, text="Help", relief=FLAT, bg = BTN_COLOR, fg = FONT_COLOR, 
command=get_help, activebackground=BTN_PRESSED_COLOR, activeforeground=FONT_COLOR, font=SMALL_FONT)
help_button.grid(row=4, column=0, sticky='w', padx=10)

info_button = Button(root, text=" i ", relief=FLAT, bg = BTN_COLOR, fg = FONT_COLOR, 
command=get_info, activebackground=BTN_PRESSED_COLOR, activeforeground=FONT_COLOR, font=SMALL_FONT)
info_button.grid(row=4, column=0)

progress = Progressbar(root, orient = HORIZONTAL,
              length = 200, mode = 'determinate')


if __name__ == "__main__":
    root.mainloop()

