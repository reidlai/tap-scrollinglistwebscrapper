from __future__ import annotations
from tap_scrollinglistwebscrapper.client import ScrollingListWebScrapperStream

class HTMLStringItemsStream(ScrollingListWebScrapperStream):
    path = "/htmlStringItems"
    name = "htmlStringItems"
    