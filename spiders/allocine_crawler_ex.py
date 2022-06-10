# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from allocine_exemple.items import AllocineExempleItem


class BestMoviesSpider(CrawlSpider):
    name = 'best_movies'
    allowed_domains = ['www.allocine.fr']

    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'

    def start_requests(self):
        yield scrapy.Request(url='https://www.allocine.fr/film/meilleurs/', headers={
            'User-Agent': self.user_agent
        })

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//h2[@class='meta-title']/a"),
             callback='parse_item', follow=True, process_request='set_user_agent'),
        Rule(LinkExtractor(
            restrict_xpaths="(//a[contains(@class, 'button-right')]"), process_request='set_user_agent')
    )

    def set_user_agent(self, request, spider):
        request.headers['User-Agent'] = self.user_agent
        return request

    def parse_item(self, response):
        item = AllocineExempleItem()
        item['title'] = Selector(response).xpath(
            "//div[@class='titlebar-title titlebar-title-lg']/text()").get()
        yield item
