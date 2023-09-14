# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from datetime import datetime

import scrapy
import re
from w3lib.html import remove_tags
from itemloaders.processors import TakeFirst, MapCompose


def strip_space(value):
    return value.strip()


def replace_non_characters(value):
    value = re.sub(r"\W", "_", value)
    return re.sub(r"_{2,}", "_", value)


def transform_title_date(value):
    date_string = re.findall(r"^\d{1,2}_\d{1,2}_\d{4}", value)[0]
    new_date_string = datetime.strptime(date_string, r"%m_%d_%Y").strftime(r"%Y_%m_%d")

    return f"{new_date_string}_-_{value[len(date_string):]}"


def extract_date(value):
    return value.split(r"_-_")[0]


class EpisodeItem(scrapy.Item):
    title = scrapy.Field(
        input_processor=MapCompose(
            remove_tags,
            strip_space,
            replace_non_characters,
            transform_title_date,
        ),
        output_processor=TakeFirst(),
    )
    summary = scrapy.Field(
        input_processor=MapCompose(
            remove_tags,
            strip_space,
        ),
        output_processor=TakeFirst(),
    )
    date = scrapy.Field(
        depends_on="title",
        input_processor=MapCompose(
            extract_date,
        ),
        output_processor=TakeFirst(),
    )
    url = scrapy.Field(
        output_processor=TakeFirst(),
    )

    file = scrapy.Field()
    document_type = scrapy.Field(
        output_processor=TakeFirst(),
    )
    episode_date = scrapy.Field(
        output_processor=TakeFirst(),
    )
