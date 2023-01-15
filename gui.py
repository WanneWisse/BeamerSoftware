from api_manager import ApiManager
import tkinter.font as tkFont
from tkinter import *
from dotenv import load_dotenv
import os

load_dotenv()
api_manager = ApiManager(os.getenv("GENIUS_API_KEY"))


def search():
    global index_text
    global pages_with_text
    artist_to_search = artist.get()
    song_to_search = song_name.get()
    pages_with_text = api_manager.get_pages_with_lyrics(song_to_search, artist_to_search)
    index_text = 0
    current_text = pages_with_text[0]
    music_show_text.config(text=current_text)
    music_show_frame.pack()
    music_show_frame.focus_set()
    search_music_frame.forget()


def stop(event):
    music_show_frame.forget()
    search_music_frame.pack()
    search_music_frame.focus_set()


def leftKey(event):
    global index_text
    if index_text > 0:
        index_text -= 1
        current_text = pages_with_text[index_text]
        music_show_text.config(text=current_text)


def rightKey(event):
    global index_text
    if index_text < len(pages_with_text) - 1:
        index_text += 1
        current_text = pages_with_text[index_text]
        music_show_text.config(text=current_text)


pages_with_text = []
index_text = 0
current_text = ""

window = Tk()
window.attributes("-fullscreen", True)
font = tkFont.Font(size=50)

search_music_frame = Frame(window)

song_name_label = Label(search_music_frame, text="Song Name", font=font)
song_name = Entry(search_music_frame, font=font)

artist_label = Label(search_music_frame, text="Artist", font=font)
artist = Entry(search_music_frame, font=font)

search = Button(search_music_frame, text="search", command=search, font=font)

song_name_label.pack()
song_name.pack()

artist_label.pack()
artist.pack()
search.pack()
search_music_frame.pack()

music_show_frame = Frame(window)

music_show_text = Label(music_show_frame, text=current_text, font=font)
music_show_text.pack()
music_show_frame.bind('<Left>', leftKey)
music_show_frame.bind('<Right>', rightKey)
music_show_frame.bind('<Escape>', stop)

window.mainloop()
