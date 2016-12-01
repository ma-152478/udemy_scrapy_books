import scrapy
from scrapy import Spider
from scrapy.loader import ItemLoader

from udemy_scraper.items import UdemyScraperItem

class BooksSpider(Spider):
    name = "books"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["http://books.toscrape.com/",]

    def parse(self, response):             
        products = response.xpath('//*[@class="product_pod"]')
        for product in products:
            link = product.xpath('.//*[@class="image_container"]/a/@href').extract_first()
#             print "link-address: " + link
            url_complete = response.urljoin(link)
#             print "complete URL: " + url_complete
            yield scrapy.Request(url_complete,callback = self.parse_detail)
        next_page = response.xpath('.//*[@class="next"]/a/@href').extract_first()
        if next_page is not None:
            fullNextUrl = response.urljoin(next_page)
            yield scrapy.Request(fullNextUrl,callback = self.parse)
            
    def parse_detail(self,response):
        l = ItemLoader(item=UdemyScraperItem(), response = response)
        name = response.xpath('.//*[@class="col-sm-6 product_main"]/h1/text()').extract_first()        
        category = response.xpath('.//*[@class="breadcrumb"]/li[3]/a/text()').extract_first()
        
        availability = response.xpath('.//*[@class="table table-striped"]/tr[6]/td/text()').extract_first()
        price = response.xpath('.//*[@class="table table-striped"]/tr[4]/td/text()').extract()        
        temp_rating = response.xpath('.//*[@class="col-sm-6 product_main"]/p[3]/@class').extract()        
        rating = temp_rating[0]
        rating = rating[12:]
        rating = rating.lower()
        rating = rating + " of five stars"        
        image_url = response.xpath('.//*[@class="item active"]/img').extract_first()
        string_len = len(image_url)
        jpg_found = image_url.find("jpg")
        jpg_found = jpg_found + 3
        delete_chars = string_len - jpg_found
        image_url = image_url[:-delete_chars]
        image_url = image_url[10:]
        image_url_complete = response.urljoin(image_url)
        description = response.xpath('.//*[@class="product_page"]/p/text()').extract()
        l.add_value('name', name)
        l.add_value('category', category)
        l.add_value('availability', availability)
        l.add_value('price', price)
        l.add_value('rating', rating)
        l.add_value('image_url', image_url_complete)
        l.add_value('description', description)
        return l.load_item()