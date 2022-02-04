# Jobscraper

### This is a scraper that first scrapes Careerguide.com and then finds the corresponding jobs on linkedin

1. clone this repo
2. install scrapy via pip install scrapy
3. cd into Jobscraper
4. You can run 1. scrapy crawl career -o career.json --> This will populate career.json. It is mandatory to name it thus.
5. You can then run scrapy crawl linkedin -0 {anyname.json} --> this will store the required output with company deatils and job details in the json file
