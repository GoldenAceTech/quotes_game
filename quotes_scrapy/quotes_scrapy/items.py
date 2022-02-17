import scrapy

class QuotesScrapyItem(scrapy.Item):
    quote = scrapy.Field()
    author = scrapy.Field()

class AuthorScrapyItem(scrapy.Item):
    name = scrapy.Field()
    date_of_birth = scrapy.Field()
    place_of_birth = scrapy.Field()