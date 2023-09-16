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
        "summary": "Fake New Insdustrial Complex  Movie: https://www.millennialmillie.com/post/shadow-gate-2-0-full-movie",
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

## how to run
The scra

## Solution
Since we are facing a page which content is loaded one the page has been delivered, we will be using `scrapy` and `flash` python packages for this task.

