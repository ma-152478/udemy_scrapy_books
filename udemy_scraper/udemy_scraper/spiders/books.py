import scrapy
from scrapy import Spider
from scrapy.http import Request
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
        name = response.xpath('.//*[@class="col-sm-6 product_main"]/h1/text()').extract_first()
        category = response.xpath('.//*[@class="breadcrumb"]/li[3]/a/text()').extract_first()
        avail_string = response.xpath('.//*[@class="instock availability"]/text()').extract()
        availability = avail_string[1].split()[0] +' '+ avail_string[1].split()[1]
        price = response.xpath('.//*[@class="table table-striped"]/tr[4]/td/text()').extract()
        temp_rating = response.xpath('.//*[@class="col-sm-6 product_main"]/p[3]/@class').extract()        
        print "temp-rating:"
        print temp_rating
        rating = temp_rating[0]
        rating = rating[12:]
        rating = rating.lower()
        rating = rating + " of five stars"
        print rating
        image_url = response.xpath('.//*[@class="item active"]/img').extract_first()
        string_len = len(image_url)
        jpg_found = image_url.find("jpg")
        jpg_found = jpg_found + 3
        delete_chars = string_len - jpg_found
        image_url = image_url[:-delete_chars]
        image_url = image_url[10:]
        image_url_complete = response.urljoin(image_url)
        description = response.xpath('.//*[@class="product_page"]/p/text()').extract()
        yield {"Name": name, "Category": category, "Availability": availability, "Price (incl.tax)": price, "Rating": rating, "Image URL": image_url_complete,"Description": description}