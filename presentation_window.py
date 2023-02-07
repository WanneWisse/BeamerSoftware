import tkinter.font as tk_font
import tkinter as tk
from tkinter import ttk


class PresentationWindow(tk.Toplevel):
    def __init__(self, parent, fullscreen=False):
        super(PresentationWindow, self).__init__(parent)
        self.PRESENTATION_FONT = tk.font.Font(size=50)

        # Take parameter on which monitor to go fullscreen on
        self.attributes('-fullscreen', fullscreen)
        self.configure(bg='white')
        self.geometry('1400x900')
        self.title('Presentation Window')

        self._verse_text_label: ttk.Label = tk.Label(self, font=self.PRESENTATION_FONT, background='white')
        self._verse_text_label.pack()

        ttk.Button(
            self,
            text="Close",
            command=self.destroy
        ).pack()

    @property
    def verse_text(self):
        return self._verse_text_label["text"]

    @verse_text.setter
    def verse_text(self, text):
        self._verse_text_label.config(text=text)
