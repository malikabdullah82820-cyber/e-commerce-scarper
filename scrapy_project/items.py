"""
Job item definitions for Scrapy
"""
import scrapy


class JobItem(scrapy.Item):
    """Item class for job listings"""
    job_title = scrapy.Field()
    company = scrapy.Field()
    location = scrapy.Field()
    department = scrapy.Field()
    employment_type = scrapy.Field()
    posted_date = scrapy.Field()
    job_url = scrapy.Field()
    job_description = scrapy.Field()
    required_skills = scrapy.Field()
    experience_level = scrapy.Field()
    salary = scrapy.Field()
    internal_id = scrapy.Field()
    scraped_date = scrapy.Field()
    source = scrapy.Field()
