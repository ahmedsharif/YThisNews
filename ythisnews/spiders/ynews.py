import json

from scrapy import Request, FormRequest
from scrapy.spiders import CrawlSpider, Spider, Rule
from scrapy.linkextractors import LinkExtractor
from w3lib.url import add_or_replace_parameter
from copy import deepcopy
import re

from ythisnews.items import YthisnewsItem

count = 1

class YNewsMixin:
    allowed_domain = ['http://ythisnews.com/aur/']


class YNewsParserSpider(YNewsMixin, Spider):
    allowed_domain = YNewsMixin.allowed_domain

    name = 'ynews-parse'

    def product_news(self, response):
        product = YthisnewsItem()
        # product['title'] = ""
        product['news'] = {}
        # product['date'] = ""

        return self.extract_requests(self.detail_requests(response), product)

    def product_desc(self, response):
       # 
       data = response.css(".entry-content p::text").extract()
       return data
       #return [re.sub(r"[^a-zA-Z0-9]+", ' ', k) for k in a.split("\n")]


    #    final_result = []
    #    for d in data: 
    #        final_result = d.split(".")
       return data

    def product_title(self, response):
        return response.css('.entry-title a::text').extract()
    
    def product_detail_title(self, response):
            return response.css('h1.entry-title::text').extract_first()
    
    def product_Date(self, response):
        date = response.css(".entry-content::text").extract_first()
        return re.sub('[^A-Za-z0-9]+', '', date)


    def detail_requests(self, response):
        news_link = response.css('.th-list-posts  h3 > a::attr(href)').extract()

        requests = []

        for color in news_link:
            # url = add_or_replace_parameter(response.url, "color", color)
            requests += [Request(url=color, callback=self.parse_news, dont_filter=True)]

        # For handling those requests which doesn't has color_requests
        return requests
    
    
    def parse_news(self, response):
        product = response.meta['product']
        requests = response.meta['requests']

        product['news'].update(self.product_sku(response))

        return self.extract_requests(requests, product)

    def product_sku(self, response):
        global count
        sku = {}

        sku['news_detail'] = self.product_desc(response)
        sku['title'] = self.product_detail_title(response)
        sku['date'] = self.product_Date(response)
        sku_id = count
        count = count + 1
        return {sku_id: sku}
    
    @staticmethod
    def extract_requests(requests, product):
        if requests:
            request = requests.pop()
            request.meta['product'] = product
            request.meta['requests'] = requests
            yield request
        else:
            yield product




class YNewsCralwer(YNewsMixin, CrawlSpider):
    name = 'ynews'
    items_per_page = 10
    start_url = 'http://ythisnews.com/aur/'

    spider_parser = YNewsParserSpider()

    allowed_domain = YNewsMixin.allowed_domain

    


    # rules = (
    #     Rule(LinkExtractor(restrict_css='.pagination.clearfix'), callback=spider_parser.product_news),
    # )

    def start_requests(self): 
        yield Request(url=self.start_url, callback=self.parse_listing, dont_filter=True)

    def parse_listing(self, response):
        global count
        count = 1
        urls = response.css('.main-navigation a::attr(href)').extract()[1:-1]
        for url in urls:
            yield Request(url=url, callback=self.parse_pagination, dont_filter=True)

    def parse_pagination(self, response):
        common_meta = {}
        common_meta['trail'] = [response.url]
        pages = response.css('.nav-links a:nth-last-child(2)::text').extract_first()

        total_pages = 1

        if pages:
            total_pages = int(pages)

            for page in range(1, total_pages):
                url = response.url + '/page' + str(page)
                meta = deepcopy(common_meta)
                yield Request(url=url, callback=self.spider_parser.product_news, meta=meta)
        else: 
            yield Request(url=self.start_url, callback=self.spider_parser.product_news)
        
    def parse(self, response):
        response.meta['trail'] = response.meta.get('trail', [])
        response.meta['trail'] += [response.url]

        for request in super().parse(response):
            request.meta['trail'] = response.meta['trail']
            yield request