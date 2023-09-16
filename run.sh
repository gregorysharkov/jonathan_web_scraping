#!/bin/bash

# Start Splash
# Check if the Splash container is already running
if [ "$(docker ps -aq -f status=running -f name=splash)" ]; then
  echo "Splash container is already running."
else
  # Start the Splash container
  docker run -d -p 8050:8050 scrapinghub/splash
fi

# Crawl episodes
scrapy crawl episodes
scrapy crawl documentaries
scrapy crawl stereo
scrapy crawl miscellaneous