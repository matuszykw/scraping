import scrapy
from selenium import webdriver
from scrapy.http import HtmlResponse
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from ..items import FilmwebItem
from scrapy.loader import ItemLoader

class MovieSpider(scrapy.Spider):
    name = 'movies'
    allowed_domains = ['www.filmweb.pl']
    start_urls = ['https://www.filmweb.pl/ranking/film']
    # download_delay = 1.0
            
            
    def __init__(self, *args, **kwargs):
        super(MovieSpider, self).__init__(*args, **kwargs)
        chromedriver_path = r"C:\Selenium_Drivers\chromedriver.exe"
        chrome_service = ChromeService(chromedriver_path)
        self.driver = webdriver.Chrome(service=chrome_service)     
            
    def scroll_down(self):
        current_scroll_height = self.driver.execute_script("return document.body.scrollHeight;")
        new_scroll_position = max(current_scroll_height - 4000, 0)
        self.driver.execute_script(f"window.scrollTo(0, {new_scroll_position});")
        time.sleep(1)
        

    def parse(self, response):
        self.driver.get(response.url)
        
        try:
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="didomi-notice-agree-button"]'))
            ).click()
        except Exception as e:
            self.log(f"Could not find or click the cookies accept button: {e}")
            
        try:
            max_scrolls = 20
            for _ in range(max_scrolls):
                self.scroll_down()

            body = self.driver.page_source
            response = HtmlResponse(url=response.url, body=body, encoding='utf-8')


            yield from self.parse_urls(response)

        finally:
            self.driver.quit() 
        
    def parse_urls(self, response):
        elements = response.css('.rankingType')
        for element in elements:
            relative_url = element.css('h2.rankingType__title a::attr(href)').get()
            if relative_url:
                movie_url = f"https://www.filmweb.pl{relative_url}"
                yield response.follow(movie_url, callback=self.parse_movie)
                
    
    def parse_movie(self, response):
        original_title = response.css('.filmCoverSection__originalTitle::text').get()
        if not original_title:
            original_title = response.css('h1.filmCoverSection__title::text').get()
        
        l = ItemLoader(item=FilmwebItem(), response=response)
        
        l.add_css('global_ranking', 'button.worldRankingButton span:first-child')
        l.add_value('title', original_title)
        l.add_css('rating', '.filmRating::attr(data-rate)')
        l.add_css('num_of_ratings', '.filmRating::attr(data-count)')
        l.add_css('genre', 'div[itemprop="genre"] span a span')
        l.add_css('country_of_origin', '.filmPosterSection__info > div:nth-of-type(4) span a span')
        l.add_css('release_date', 'span[itemprop="datePublished"]:first-child::attr(content)')
        l.add_xpath('us_gross', '//*[@id="site"]/div[3]/div[2]/div/div[11]/section[1]/div/div[2]/div/div/div[1]/div[2]/div[2]')
        l.add_xpath('worldwide_gross', '//*[@id="site"]/div[3]/div[2]/div/div[11]/section[1]/div/div[2]/div/div/div[1]/div[2]/div[1]/text()')
        l.add_xpath('budget', '//*[@id="site"]/div[3]/div[2]/div/div[11]/section[1]/div/div[2]/div/div/div[1]/div[4]/text()')
        
        # data = {
        #     'global_ranking': response.css('button.worldRankingButton span:first-child::text').get(),
        #     'title': original_title,
        #     'rating': response.css('.filmRating::attr(data-rate)').get(),
        #     'num_of_ratings': response.css('.filmRating::attr(data-count)').get(),
        #     'genre': response.css('div[itemprop="genre"] span a span::text').get(),
        #     'country_of_origin': response.css('.filmPosterSection__info > div:nth-of-type(4) span a span::text').get(),
        #     'release_date': response.css('span[itemprop="datePublished"]:first-child::attr(content)').get(),
        #     'us_gross': response.xpath('//*[@id="site"]/div[3]/div[2]/div/div[11]/section[1]/div/div[2]/div/div/div[1]/div[2]/div[2]/text()').get(),
        #     'worldwide_gross': response.xpath('//*[@id="site"]/div[3]/div[2]/div/div[11]/section[1]/div/div[2]/div/div/div[1]/div[2]/div[1]/text()').get(),
        #     'budget': response.xpath('//*[@id="site"]/div[3]/div[2]/div/div[11]/section[1]/div/div[2]/div/div/div[1]/div[4]/text()').get()
        # }
        
        yield l.load_item()
        