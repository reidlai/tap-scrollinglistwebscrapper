from __future__ import annotations
from tap_scrollinglistwebscrapper.client import ScrollingListWebScrapperStream

class GenericHTMLStringStream(ScrollingListWebScrapperStream):
    name = "list_content"