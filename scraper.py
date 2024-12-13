import scrapy

class LTMPTScraper(scrapy.Spider):
    name = "book-to-scrape"

    def start_requests(self):
      url = 'https://books.toscrape.com/'
      yield scrapy.Request(url=url, callback=self.parse)
    
    def parse(self, response):
      for data in response.css('ol li article'):
        yield {
            'image_url' : data.css('img::attr(src)').get(),
            'name' : data.css('h3 a::text').get(),
            'price': data.css('.price_color::text').get(),
            'availability': data.css('p.availability::text').get(),
            'rating': data.css('.star-rating::attr(class)').get()
        }
        
      next_button = response.css('li.next a::attr(href)').get()

      if next_button is not None:
        yield response.follow(next_button, callback=self.parse)
