"""Custom client handling, including scrollinglistwebscrapperStream base class."""

from __future__ import annotations

from typing import Iterable

from singer_sdk import typing as th  # JSON Schema typing helpers
from singer_sdk.streams import Stream

import time
from playwright.async_api import async_playwright
import asyncio

class ScrollingListWebScrapperStream(Stream):

    @property
    def url(self) -> str:
        return self.config["url"]
    
    @property
    def browserTimeoutSeconds(self) -> int:
        return self.config["browserTimeoutSeconds"]
    
    @property
    def scrollWaitSeconds(self) -> int:
        return self.config["scrollingWaitSeconds"]
    
    @property
    def endOfListSelector(self) -> str:
        return self.config["endOfListSelector"]
    
    @property
    def itemSelector(self) -> str:
        return self.config["itemSelector"]
        
    def get_records(self, context: dict | None) -> Iterable[dict]:
        pw = asyncio.run(async_playwright().start())
        browser = asyncio.run(pw.chromium.launch(headless=True, timeout=self.browserTimeoutSeconds * 1000))
        page = asyncio.run(browser.new_page())
        asyncio.run(page.goto(self.url))
  
        asyncio.run(self.scrollPageDown(page=page))
        itemList = asyncio.run(getItemList(page=page))
        asyncio.run(browser.close())
        asyncio.run(pw.end())
        for item in itemList:
            yield dict(item=item)
        
                
    async def scrollPageDown(self, page):
        selector = None
        while(selector == None):
            await page.keyboard.press("PageDown")
            time.sleep(self.scrollWaitSeconds)
            selector = await page.query_selector(self.endOfPageSelector)
    
    async def getItemList(self, page):
        itemSelectorList = await page.query_selector_all(self.itemSelector)
        itemList = []
        for itemSelector in itemSelectorList:
            itemList.append(await itemSelector.inner_html())
        return itemList
    
    schema = th.PropertiesList(
        th.Property("item", th.StringType),
    ).to_dict()
