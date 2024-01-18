from singer_sdk.testing import get_tap_test_class

from tap_scrollinglistwebscrapper.tap import TapScrollingListWebScrapper

SAMPLE_CONFIG = {
    "url": "https://www.tntsupermarket.com/eng/weekly-special-er.html",
    "browserTimeoutSeconds": 0,
    "scrollWaitSeconds": 1,
    "endOfListSelector": "p[class^='category-noData-']",
    "itemSelector": "div[class^='item-root']"
}

# Run standard built-in tap tests from the SDK:
TestTapScrollingListWebScrapper = get_tap_test_class(
    tap_class=TapScrollingListWebScrapper,
    config=SAMPLE_CONFIG,
)

