import scrapy
import json
from ..items import LinkedinscraperItem, JobscraperItem, CompanyscraperItem
import re


class LinkedInSpider(scrapy.Spider):
    """ This is the linkedin spider to crawl linkedin for jobs corresponding to each state and then finding company descriptions corresponding to each job"""
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

                    yield scrapy.Request(url=f'https://www.linkedin.com/jobs/search?keywords={subcategory}&location={state+", India"}&geoId=&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0', headers=headers, callback=self.parse, meta={"state": state, "subcategory": subcategory, "category": item["category"], "headers": headers})
                print()

    def parse(self, response):

        Parent_category = JobscraperItem()

        Parent_category["category"] = response.meta["category"]
        Parent_category["subcategory"] = response.meta["subcategory"]

        if not response.css("h1.core-section-container__main-title::text").extract():
            for card in response.css("ul.jobs-search__results-list li"):
                job_items = LinkedinscraperItem()
                next_url_company = ""

                if card.css("h3.base-search-card__title"):
                    job_items["job_designation"] = str(
                        card.css("h3.base-search-card__title::text").get()).strip(" \n")
                else:
                    job_items["job_designation"] = str(
                        card.css("a job-card-list__title::text").get()).strip(" \n")

                if card.css(
                        "h4.base-search-card__subtitle a"):
                    job_items["company"] = str(card.css(
                        "h4.base-search-card__subtitle a.hidden-nested-link::text").get()).strip(" \n")
                    next_url_company = card.css(
                        "h4.base-search-card__subtitle a.hidden-nested-link").attrib["href"]

                elif card.css(
                        "h4.base-search-card__subtitle div"):
                    job_items["company"] = str(card.css(
                        "h4.base-search-card__subtitle div::text").get()).strip(" \n")
                    next_url_company = ""

                elif card.css(
                        "a.job-card-container__company-name"):
                    job_items["company"] = str(card.css(
                        "a.job-card-container__company-name::text").get()).strip(" \n")
                    next_url_company = card.css(
                        "a.job-card-container__company-name").attrib["href"]

                elif card.css(
                        "a.job-card-container__link"):
                    job_items["company"] = str(card.css(
                        "a.job-card-container__link::text").get()).strip(" \n")
                    next_url_company = card.css(
                        "a.job-card-container__link").attrib["href"]

                if card.css(
                        "span.job-search-card__location"):
                    job_items["location"] = str(card.css(
                        "span.job-search-card__location::text").get()).strip(" \n")
                elif card.css("li.job-card-container__metadata-item"):
                    job_items["location"] = str(card.css(
                        "li.job-card-container__metadata-item::text").get()).strip(" \n")

                Parent_category["job_detail"] = dict(job_items)
                Parent_category["company_detail"] = ""

                if next_url_company != "":
                    yield scrapy.Request(
                        url=next_url_company, headers=response.meta["headers"], callback=self.parse_company, meta={"parent": Parent_category})

        else:
            job_items = LinkedinscraperItem()
            job_items["job_designation"] = "None 0 results"
            job_items["company"] = "Not Found any 0 results"
            job_items["location"] = response.meta["state"]

            Parent_category["job_detail"] = dict(job_items)
            yield Parent_category

    def parse_company(self, response):

        company = CompanyscraperItem()
        company["description"] = str(response.css(
            "p.about-us__description::text").getall()).strip("\n ")

        company["location"] = (" ".join([string.strip("\n ") for string in response.css(
            "ul li.locations__location p.locations__address-line::text").getall()])).strip("\n ")

        dd_text_list = [x.strip(" \n")
                        for x in response.css("dd::text").extract()]
        for dd in dd_text_list:
            if re.search("employees$", dd):
                company["number_employees"] = dd

        response.meta["parent"]["company_detail"] = dict(company)
        yield response.meta["parent"]
