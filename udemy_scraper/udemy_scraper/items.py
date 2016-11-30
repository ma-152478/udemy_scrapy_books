import scrapy


class UdemyScraperItem(scrapy.Item):
    name = scrapy.Field()
    category = scrapy.Field()
    availability = scrapy.Field()
    price = scrapy.Field()
    rating = scrapy.Field()
    image_url = scrapy.Field()
    description = scrapy.Field()



    
    
