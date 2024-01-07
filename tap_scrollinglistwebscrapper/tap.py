from __future__ import annotations
from singer_sdk import Tap
from singer_sdk import typing as th
from tap_scrollinglistwebscrapper import streams

class TapScrollingListWebScrapper(Tap):
    name = "tap-scrollinglistwebscrapper"
    config_jsonschema = th.PropertiesList(
        th.Property("url", th.StringType, description="The url for the web page"),
        th.Property("browserTimeoutSeconds", th.IntegerType, description="The timeout in seconds for the browser to load the page"),
        th.Property("scrollWaitSeconds", th.IntegerType, description="The scrolling wait in seconds"),
        th.Property("endOfListSelector", th.StringType, description="The selector for the end of list"),
        th.Property("itemSelector", th.StringType, description="The selector for the items in the list"),
    ).to_dict()

    def discover_streams(self) -> list[streams.ScrollingListWebScrapperStream]:
        return [streams.GenericHTMLStringStream(self)]

if __name__ == "__main__":
    TapScrollingListWebScrapper.cli()
