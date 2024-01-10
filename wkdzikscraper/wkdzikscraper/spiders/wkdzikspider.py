import scrapy
from ..items import WkdzikscraperItem
from scrapy.loader import ItemLoader

class WkdzikSpider(scrapy.Spider):
    name = 'wkdzik'
    allowed_domains = ['wkdzik.pl']
    start_urls = ['https://wkdzik.pl/ubrania']
    
    def parse(self, response):
        products = response.css('div.product')
        for product in products:
            relative_url = product.css('a.prodname::attr(href)').get()
            if relative_url:
                prod_url = f'https://wkdzik.pl{relative_url}'
            yield response.follow(prod_url, callback=self.parse_item)
            
        next_page = response.css('li.last a::attr(href)').get()
        if next_page:
            next_page_url = f'https://wkdzik.pl{next_page}'
            yield response.follow(next_page_url, callback=self.parse)
            
    def parse_item(self, response):
        l = ItemLoader(item=WkdzikscraperItem(), response=response)
        l.add_css('name', 'h1.name')
        l.add_css('price', 'em.main-price')
        
        return l.load_item()