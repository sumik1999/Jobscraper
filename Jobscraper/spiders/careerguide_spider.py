import scrapy
from ..items import JobscraperItem


class CareerguideSpider(scrapy.Spider):
    name = "career"

    def start_requests(self):
        urls = [
            'https://www.careerguide.com/career-options'
        ]
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
        for url in urls:
            yield scrapy.Request(url=url, headers=headers, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-1]
        filename = f'{page}.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}')

        header = response.css("div.c-body h2.c-font-bold a::text").getall()
        ul_objects = response.css("div.c-body div.col-md-4 ul")
        items = JobscraperItem()

        for object, heading in zip(ul_objects, header):
            items["category"] = heading
            items["subcategory"] = object.css("li a::text").getall()

            yield items
