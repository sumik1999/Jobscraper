import scrapy
import json
from ..items import LinkedinscraperItem, JobscraperItem, CompanyscraperItem


class LinkedInSpider(scrapy.Spider):
    name = "linkedin"

    def start_requests(self):
        urls = [
            'https://www.linkedin.com/jobs/search?keywords={subcategory}&location={state}&geoId=&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0'
        ]
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}

        with open("states.json", "r") as statefile:
            state_dict = json.load(statefile)

        with open("career.json", "r") as careerfile:
            career_list = json.load(careerfile)

        for state in state_dict["states"]:
            for item in career_list:
                for subcategory in item["subcategory"]:
                    print("SSS subcategory", subcategory)

                    yield scrapy.Request(url=f'https://www.linkedin.com/jobs/search?keywords={subcategory}&location={state+", India"}&geoId=&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0', headers=headers, callback=self.parse, meta={"state": state, "subcategory": subcategory, "category": item["category"], "headers": headers})
                print()
            break

    def parse(self, response):

        Parent_category = JobscraperItem()
        job_items = LinkedinscraperItem()

        Parent_category["category"] = response.meta["category"]
        Parent_category["subcategory"] = response.meta["subcategory"]
        list_jobs = []

        if not response.css("h1.core-section-container__main-title::text").extract():
            for card in response.css("ul.jobs-search__results-list li"):

                job_items["title"] = str(card.css(
                    "h3.base-search-card__title::text").get()).strip(" \n")
                if card.css(
                        "h4.base-search-card__subtitle a.hidden-nest-link"):
                    job_items["company"] = str(card.css(
                        "h4.base-search-card__subtitle a.hidden-nest-link::text").get()).strip(" \n")

                elif card.css(
                        "h4.base-search-card__subtitle div"):
                    job_items["company"] = str(card.css(
                        "h4.base-search-card__subtitle div::text").get()).strip(" \n")

                job_items["location"] = str(card.css(
                    "span.job-search-card__location::text").get()).strip(" \n")

                list_jobs.append(dict(job_items))

                if card.css(
                        "h4.base-search-card__subtitle a.hidden-nested-link"):
                    next_url_company = card.css(
                        "h4.base-search-card__subtitle a.hidden-nested-link").attrib["href"]
                    Parent_category["company_detail"] = yield scrapy.Request(url=next_url_company, headers=response.meta["headers"], callback=self.parse_company)

            Parent_category["job_detail"] = list_jobs

            yield Parent_category

        else:
            job_items["title"] = response.meta["subcategory"]
            job_items["company"] = "Not Found any"
            job_items["location"] = response.meta["state"]

            Parent_category["job_detail"] = dict(job_items)
            yield Parent_category

    def parse_company(self, response):

        company = CompanyscraperItem()
        company["description"] = response.css(
            "p.about-us__description::text").extract()
        company["location"] = response.css(
            "ul li.locations__location p.locations__address-line::text").getall()
        company["number_employees"] = response.css(
            "div dd::text").extract()

        yield company
