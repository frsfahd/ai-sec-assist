from typing import TypedDict

class NewsArticle(TypedDict):
    title: str
    url: str
    date: str   # ISO 8601 format timestamp
    publisher: str

