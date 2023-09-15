# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

import scrapy
from pathlib import Path

from itemadapter import ItemAdapter
from scrapy.pipelines.files import FilesPipeline

# remove URL
# remove meta_name
# replace file_name with filename with the actual file name


class ToreItemExtractor(object):
    """first step: fill in fields that are derivative to the already collected fields"""

    def process_item(self, item, spider):
        """populate other required fields"""
        adapter = ItemAdapter(item)
        adapter["episode_date"] = self._get_episode_date(adapter)
        adapter["file_urls"] = [self._get_episode_url(adapter)]
        adapter["file_name"] = self._get_episode_path(adapter)
        return item

    def _get_episode_date(self, episode) -> str:
        """gets episode date from the title"""

        return episode["title"].split("_-_")[0]

    def _get_episode_url(self, episode) -> str:
        """returns episode url for a given episode"""

        return episode["source"] + episode["url"]

    def _get_episode_path(self, episode) -> str:
        """returns path to the episode"""

        meta_name = episode["meta_name"]
        episode_date = episode["episode_date"]
        episode_id = episode["url"].split("=")[-1]

        return str(Path(f"{episode_date} - {episode_id}.pdf"))


class ToreFilesPipeline(FilesPipeline):
    """second step: download file and save it with the appropriate name"""

    def file_path(self, request, response=None, info=None, *, item=None):
        adapter = ItemAdapter(item)
        return Path(adapter["file_name"])

    def get_media_requests(self, item, info):
        adapter = ItemAdapter(item)
        for file_url in adapter["file_urls"]:
            yield scrapy.Request(file_url)


# class ToreItemCleanUp(object):
#     """remove technical item fields"""
