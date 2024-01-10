import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ..items import ReiscraperItem

class ProductSpider(CrawlSpider):
    name = 'product'
    allowed_domains = ['rei.com']
    start_urls = ['https://www.rei.com/c/camping-and-hiking']
    
    rules = (
        Rule(LinkExtractor(allow=(r'page='))),
        Rule(LinkExtractor(allow=('product')), callback='parse_item')
    )
    
    def parse_item(self, response):
        item = ReiscraperItem()
        
        item['name'] = response.css('h1#product-page-title::text').get()
        item['price'] = response.css('span#buy-box-product-price::text').get()
        item['item_no'] = response.css('span#product-item-number::text').get()
        item['rating'] = response.css('span.cdr-rating__number_13-5-3::text').get()
        
        yield item