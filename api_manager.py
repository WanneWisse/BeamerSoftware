import requests
from lyricsgenius import Genius
from bs4 import BeautifulSoup
import bs4


class ApiManager:
    def __init__(self, api_key):
        self.api_key = api_key
        self.genius = self.init_api()

    def init_api(self):
        genius = Genius(self.api_key)
        genius.verbose = False
        return genius

    def get_pages_with_lyrics(self, title, artist):
        song_lyrics_url = self.get_song_lyrics_url(title, artist)
        lyrics_from_webpage = self.webscrape_song_lyrics_url(song_lyrics_url)
        lyrics_without_headers = self.delete_lyrics_headers(lyrics_from_webpage)
        pages_of_lyrics = self.create_pages(lyrics_without_headers)
        return pages_of_lyrics

    def get_song_lyrics_url(self, title, artist):
        song_info = self.genius.search_song(title=title, artist=artist, song_id=None, get_full_info=True)
        return song_info.to_dict()["url"]

    @staticmethod
    def webscrape_song_lyrics_url(url):
        r = requests.get(url, allow_redirects=True)
        # open("page.html", "wb").write(r.content)
        # text = None
        # with open("page.html", "r", encoding='utf-8') as f:
        #     text= f.read()
        soup = BeautifulSoup(r.content, 'html.parser')

        lyrics = []
        for i in soup.find_all("div", class_="Lyrics__Container-sc-1ynbvzw-6 YYrds"):

            for tag in i.contents:
                if type(tag) == bs4.element.Tag:
                    if tag.name == "br":
                        lyrics.append("\n")
                    elif tag.name == "a":
                        for j in tag.find_all("span", class_="ReferentFragmentdesktop__Highlight-sc-110r0d9-1 jAzSMw"):
                            lyrics.append("\n")
                            for inner_tag in j.contents:
                                if type(inner_tag) == bs4.element.Tag:
                                    if inner_tag.name == "br":
                                        lyrics.append("\n")
                                else:
                                    lyrics.append(inner_tag.string)
                else:
                    lyrics.append(tag.string)
        return lyrics

    @staticmethod
    def delete_lyrics_headers(lyrics):
        new_lyrics = []
        for index in range(len(lyrics)):
            if lyrics[index][0] != "[":
                new_lyrics.append(lyrics[index])
        return new_lyrics

    @staticmethod
    def create_pages(lyrics):
        pages_with_text = []

        amount_n = 0
        current_text_page = ""
        for characters in lyrics:
            if characters == "\n":
                if current_text_page != "":
                    amount_n += 1
                    current_text_page += characters
            else:
                amount_n = 0
                current_text_page += characters
            if amount_n == 2:
                pages_with_text.append(current_text_page)
                current_text_page = ""
                amount_n = 0
        pages_with_text.append(current_text_page)
        return pages_with_text
