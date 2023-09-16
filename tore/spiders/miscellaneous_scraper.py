from .episode_scraper import EpisodeScraper
from ..items import EpisodeItem

MISCELLANEOUS_NAME = "miscellaneous"


class MiscellaneousScraper(EpisodeScraper):
    name = f"{MISCELLANEOUS_NAME}"
    start_urls = [
        "https://toresaid.com/miscList.cshtml",
    ]
    custom_settings = {
        "FEEDS": {
            f"tore/data/metadata/{MISCELLANEOUS_NAME}.json": {
                "format": "json",
                "item_classes": [
                    EpisodeItem,
                ],
                "overwrite": True,
            },
        },
        "FILES_STORE": f"tore/data/{MISCELLANEOUS_NAME}",
    }
