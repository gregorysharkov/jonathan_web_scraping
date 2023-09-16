from .episode_scraper import EpisodeScraper
from ..items import EpisodeItem

DOCUMENTARIES_NAME = "documentaries"


class DocumentaryScraper(EpisodeScraper):
    name = f"{DOCUMENTARIES_NAME}"
    start_urls = [
        "https://toresaid.com/DocumList.cshtml",
    ]
    custom_settings = {
        "FEEDS": {
            f"tore/data/metadata/{DOCUMENTARIES_NAME}.json": {
                "format": "json",
                "item_classes": [
                    EpisodeItem,
                ],
                "overwrite": True,
            },
        },
        "FILES_STORE": f"tore/data/{DOCUMENTARIES_NAME}",
    }
