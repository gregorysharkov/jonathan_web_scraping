# Scraper application

## Problem statement
The client wants to get a server application to be able to scrape information from `toresaid.com`. This website contains a collection of audio files and their transcription that is divided into 4 groups:
* episodes
* documentaries
* miscellaneous
* stereo

Each contains a list of episodes made with asp.net technology and accessible via `cshtml` technology.

For each document we want to collect all transcripts as well as metadata in json format.
```json
    {
        "title": "2020_10_14_-_Shadowgate_2",
        "summary": "Fake New Industrial Complex  Movie: https://www.millennialmillie.com/post/shadow-gate-2-0-full-movie",
        "document_type": "pdf",
        "source": "https://toresaid.com",
        "episode_date": "2020_10_14",
        "file_urls": [
            "https://toresaid.com/api/episode/printtranscript?i=973"
        ],
        "file_name": "2020_10_14 - 973.pdf"
    },
```

Once metadata has been extracted, we want to download a transcript url using the link available for each episode and store all documents separately.

The whole solution should be deployable on a server on can be ran locally.

## Setup
### Install docker in your environment
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
newgrp docker
```

### Install dependencies
```bash
pip install -r requirements.txt
```

### Enable run.sh
```bash
chmod +x run.sh
```

## Run scrapers
```bash
./run.sh
```

# Solution
Since we are facing a page which content is loaded one the page has been delivered, we will be using `scrapy` and `flash` python packages for this task.

The overall solution is a scrapy project with 4 spiders:
* `EpisodeScraper`
* `DocumentaryScraper`
* `MiscellaneousScraper`
* `StereoScraper`

They have the same functionality except for the custom settings, therefore the functionality is described in `EpisodeScraper` and all other scrapers inherit from it.

## Outputs
Each scraper produces 2 outputs:
1. `<scraper_name>.json` that contains metadata. Stored in `data\metadata` folder
2. `data\<scraper_name>\` folder that contains downloaded files

## Requests
The scraper uses `Splash middleware` to send http requests. Each request is sent, then it waits two seconds and only then starts scraping the response.

## ScrapedItems
Each spider populates an `EpisodeItem` defined in `items.py`. Each item contains the following fields:
* title. Contains title of the episode
* summary. Contains text summary of the episode
* url. Contains raw url extracted from the page
* source. Static. Contains 'toresaid.com'
* document_type. Static. Contains 'pdf'
* episode_path. Contains name of the file that corresponds to the episode. Equal to id of the episode
* episode_date. Contains date of the episode
* file_urls. Contains link to the file
* meta_name. Temporary contains name inherited from the scraping class. Used to identify path the file

## ItemPipelines
Each `EpisodeItem` is processed through an ItemPipeline. Defined in `pipelines.py` that consists of 3 steps:
1. `ToreItemExtractor`. Used to fill in fields that depend on the data extracted
2. `ToreFilesPipeline`. A `FilePipeline` that is responsible for downloading all files from `file_urls`.
3. 'ToreItemCleanUp'. Used to clean up unused fields
