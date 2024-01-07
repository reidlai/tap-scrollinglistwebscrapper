"""Custom client handling, including scrollinglistwebscrapperStream base class."""

from __future__ import annotations

from typing import Iterable

from singer_sdk import typing as th  # JSON Schema typing helpers
from singer_sdk.streams import Stream

import time
from playwright.async_api import async_playwright

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
    
    def get_records(self) -> Iterable[dict]:
        pw = await async_playwright().start()
        browser = await pw.chromium.launch(headless=True, timeout=browserTimeoutSeconds * 1000)
        page = await browser.new_page()
        await page.goto(url)
        await scrollPageDown(page=page, scrollWaitSeconds=scrollWaitSeconds, endOfListSelector=endOfListSelector)
        itemList = await getItemList(page=page, itemSelector=itemSelector)
        await browser.close()
        await pw.end()
        for item in itemList:
            yield dict(item=item)
        
    async def scrollPageDown(page, scrollWaitSeconds, endOfPageSelector):
        selector = None
        while(selector == None):
            await page.keyboard.press("PageDown")
            time.sleep(scrollWaitSeconds)
            selector = await page.query_selector(endOfPageSelector)
    
    async def getItemList(page, itemSelector):
        itemSelectorList = await page.query_selector_all(itemSelector)
        itemList = []
        for itemSelector in itemSelectorList:
            itemList.append(await itemSelector.inner_html())
        return itemList
