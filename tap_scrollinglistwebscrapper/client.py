"""Custom client handling, including scrollinglistwebscrapperStream base class."""

from __future__ import annotations

from typing import Iterable

from singer_sdk import typing as th  # JSON Schema typing helpers
from singer_sdk.streams import Stream

import time
from playwright.async_api import async_playwright
import asyncio

class ScrollingListWebScrapperStream(Stream):
        
    def get_records(self, context: dict | None) -> Iterable[dict]:
        itemList = asyncio.run(self.get_records_async(context))
        for item in itemList:
            yield item
         
    async def get_records_async(self, context: dict | None) -> list[str]:
        pw = await async_playwright().start()
        
        browser = await pw.chromium.launch(headless=True, timeout=self.config.get("browserTimeoutSeconds") * 1000)

        page = await browser.new_page()
        await page.goto(self.config.get("url"))
  
        await self.scrollPageDown(page=page)
        
        itemList = await self.getItemList(page=page)
        
        await browser.close()
        
        pw.stop()
        
        # itemList =  [dict(id=1, htmlString="1"), dict(id=2, htmlString="2")]
        return itemList
        
                
    async def scrollPageDown(self, page):
        selector = None
        while(selector == None):
            await page.keyboard.press("PageDown")
            time.sleep(self.config.get("scrollWaitSeconds"))
            selector = await page.query_selector(self.config.get("endOfListSelector"))
    
    async def getItemList(self, page):
        itemSelectorList = await page.query_selector_all(self.config.get("itemSelector"))
        itemList = []
        id = 0
        for itemSelector in itemSelectorList:
            id += 1
            itemList.append(dict(id=id, htmlString= await itemSelector.inner_html()))
        return itemList
    
    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("htmlString", th.StringType),
    ).to_dict()
