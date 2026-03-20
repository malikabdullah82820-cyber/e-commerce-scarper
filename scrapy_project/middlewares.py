"""
Scrapy middlewares for job scraper
"""
from scrapy import signals
from scrapy.exceptions import IgnoreRequest
import random


class JobScraperDownloaderMiddleware:
    """Custom downloader middleware"""
    
    def __init__(self):
        pass
    
    @classmethod
    def from_crawler(cls, crawler):
        o = cls()
        crawler.signals.connect(o.spider_opened, signal=signals.spider_opened)
        return o
    
    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
    
    def process_request(self, request, spider):
        # Add random user agent
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
        ]
        request.headers['User-Agent'] = random.choice(user_agents)
        return None
    
    def process_response(self, request, response, spider):
        # Only process 200 responses
        if response.status == 429:  # Too many requests
            spider.logger.warning(f'Rate limited. Retry: {request.url}')
            return request
        
        return response
    
    def process_exception(self, request, exception, spider):
        spider.logger.error(f'Error processing {request.url}: {exception}')
