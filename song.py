from dataclasses import dataclass, field
from typing import List


@dataclass
class Song:
    """Represent a collection of verses, author and title"""
    author: str = "unknown"
    title: str = "unknown"
    verses: List[str] = field(default_factory=lambda: [""])

    @property
    def num_verses(self):
        return len(self.verses)

    @property
    def display(self):
        return self.author + " - " + self.title
