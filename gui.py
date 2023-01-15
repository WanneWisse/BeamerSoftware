import tkinter.font as tkFont
from tkinter import *
from tkinter import ttk
from dotenv import load_dotenv
import os

from typing import Optional, List, Text

from presentation_window import PresentationWindow
from api_manager import ApiManager
from song import Song


load_dotenv()
api_manager = ApiManager(os.getenv("GENIUS_API_KEY"))


class App(Tk):
    def __init__(self):
        super(App, self).__init__()
        self.DEFAULT_FONT = tkFont.Font(size=12)

        ttk.Button(
            self,
            text="Toggle Presentation Window",
            command=self.toggle_presentation_window,
        ).pack()

        self.title('Main Window')
        self.presentation_window: Optional[PresentationWindow] = PresentationWindow(self)

        # List of songs
        # Each song is a list of text
        self.songs: List[Song] = [
            Song()  # added an empty default song
        ]
        self._current_index = (0, 0)

        self.search_frame = SearchFrame(self)
        self.search_frame.pack()

        self.bind('<Right>', self.go_verse_right)
        self.bind('<Left>', self.go_verse_left)

    @property
    def current_index(self):
        return self._current_index

    @current_index.setter
    def current_index(self, index):
        song_index, verse_index = index
        song_index = max(0, min(len(self.songs) - 1, song_index))
        verse_index = max(0, min(self.songs[song_index].num_verses - 1, verse_index))

        self._current_index = (song_index, verse_index)

        if self.presentation_window_exists():
            self.presentation_window.verse_text = self.current_verse_text

    @property
    def current_verse_text(self):
        song_index, verse_index = self.current_index
        return self.songs[song_index].verses[verse_index]

    def toggle_presentation_window(self):
        if not self.presentation_window_exists():
            self.open_presentation_window()
        else:
            self.close_presentation_window()

    def open_presentation_window(self):
        if not self.presentation_window_exists():
            self.presentation_window = PresentationWindow(self)

    def close_presentation_window(self):
        if self.presentation_window_exists():
            self.presentation_window.destroy()
            self.presentation_window = None

    def presentation_window_exists(self):
        if self.presentation_window is not None:
            return self.presentation_window.winfo_exists()
        return False

    def search(self):
        artist_to_search = self.search_frame.artist_entry.get()
        song_to_search = self.search_frame.song_name_entry.get()
        lyrics = api_manager.get_pages_with_lyrics(song_to_search, artist_to_search)

        self.songs.append(
            Song(
                artist_to_search,
                song_to_search,
                lyrics,
            )
        )

    def go_verse_right(self, event):
        song_index, verse_index = self.current_index
        current_song_len = self.songs[song_index].num_verses

        new_verse_index = verse_index + 1
        if new_verse_index < current_song_len:  # still in current song
            self.current_index = (song_index, new_verse_index)
        elif song_index + 1 >= len(self.songs):  # end of last song
            # No need to change update current index
            pass
        else:  # go to next song
            self.current_index = (song_index + 1, 0)

    def go_verse_left(self, event):
        song_index, verse_index = self.current_index
        # current_song_len = self.songs[song_index].num_verses

        new_verse_index = verse_index - 1
        if new_verse_index >= 0:  # still in current song
            self.current_index = (song_index, new_verse_index)
        elif song_index - 1 < 0:  # beyond start of first song
            # No need to change update current index
            pass
        else:  # go to previous song
            new_song_index = song_index - 1
            self.current_index = (new_song_index, self.songs[new_song_index].num_verses - 1)


class SearchFrame(Frame):
    def __init__(self, parent: App):
        super(SearchFrame, self).__init__(parent)

        self.song_name_label = ttk.Label(
            self,
            text="Song Name",
            font=parent.DEFAULT_FONT,
        )
        self.song_name_entry = Entry(self, font=parent.DEFAULT_FONT)
        self.song_name_label.pack()
        self.song_name_entry.pack()

        self.artist_label = Label(
            self,
            text="Artist",
            font=parent.DEFAULT_FONT
        )
        self.artist_entry = Entry(self, font=parent.DEFAULT_FONT)
        self.artist_label.pack()
        self.artist_entry.pack()

        self.search_button = Button(self, text="search", command=parent.search, font=parent.DEFAULT_FONT)
        self.search_button.pack()


window = App()
window.mainloop()
