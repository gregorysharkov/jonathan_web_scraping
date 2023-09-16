from .episode_scraper import EpisodeScraper
from ..items import EpisodeItem

STEREO_NAME = "stereo"


class StereoScraper(EpisodeScraper):
    name = f"{STEREO_NAME}"
    start_urls = [
        "https://toresaid.com/StereoList.cshtml",
    ]
    custom_settings = {
        "FEEDS": {
            f"tore/data/metadata/{STEREO_NAME}.json": {
                "format": "json",
                "item_classes": [
                    EpisodeItem,
                ],
                "overwrite": True,
            },
        },
        "FILES_STORE": f"tore/data/{STEREO_NAME}",
    }
