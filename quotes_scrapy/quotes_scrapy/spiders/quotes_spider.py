import scrapy
from scrapy.loader import ItemLoader
from ..items import QuotesScrapyItem,AuthorScrapyItem
from db_method.save_data import Save_Scraped_Data
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from typing import Generator, Any

db_name = "quotes.db"
data_insert = Save_Scraped_Data(db_name)
data_insert.create_quote_table()
data_insert.create_author_table()

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = ["http://quotes.toscrape.com/page/1/"]

    def parse(self, response) -> Generator[scrapy.Item | Any, None, None]:
        """Calls the parse_quote method, search for a next link and request it to scrape quotes using the parse_quote method till there is no link 

        Args:
            response: The response gotten from the request

        Yields:
            scrapy.Item: srapy.Item object containing all quotes and quthor's name from each page
        """
        yield self.parse_quotes(response)
        next_page = response.css("li.next a::attr(href)").get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def parse_quotes(self, response) -> scrapy.Item:
        """Extracts data from the response using a item loader, process the item loader for use to insert data in the sqlite3 database

        Args:
            response: The response object to extract data from

        Returns:
            scrapy.Item: A scrapy.Item object containg extracted datas
        """
        l = ItemLoader(item=QuotesScrapyItem(), response=response)
        l.add_css("quote", "span.text::text")
        l.add_css("author", "span small::text")
        quotes_data = list(zip(*l.load_item().values()))
        insert_query = "INSERT INTO quotes (quote, author) VALUES (?, ?)"
        data_insert.insert_data(insert_query, quotes_data)
        return l.load_item()


class AuthorSpider(scrapy.Spider):
    name = "author"

    start_urls = ["http://quotes.toscrape.com/"]

    def parse(self, response):
        """look for links to authors page from quotes and scrape each page, then looks for the link to next quotes page and repeat the process till there is no next qoute page link

        Args:
            response (_type_): The response data  gotten from the request

        Yields:
            _type_: A scrapy.Item object containing author's data from each quote page
        """
        author_page_links = response.css(".author + a")
        yield from response.follow_all(author_page_links, self.parse_author)
        pagination_links = response.css("li.next a")
        yield from response.follow_all(pagination_links, self.parse)

    def parse_author(self, response):
        """Extracts data from the response using a item loader, process the item loader for use to insert data in the sqlite3 database

        Args:
            response (_type_): The response object to extract data from

        Returns:
            scrapy.Item: A scrapy.Item object containg extracted datas
        """
        l = ItemLoader(item=AuthorScrapyItem(), response=response)
        l.add_css("name", "h3.author-title::text")
        l.add_css("date_of_birth", ".author-born-date::text")
        l.add_css("place_of_birth", ".author-born-location::text")

        loader = l.load_item()

        name = loader['name'][0].strip()
        d_o_b = loader['date_of_birth'][0].strip()
        place_of_birth = loader['place_of_birth'][0].strip().removeprefix('in ')
        author_data =[(name, d_o_b, place_of_birth)]
        insert_query = """INSERT INTO authors (author, date_of_birth, place_of_birth) 
        VALUES (?, ?, ?)
        """
        data_insert.insert_data(insert_query, author_data)

        yield loader

class Process_Scraped_Data:
    configure_logging({"LOG_FORMAT": "%(levelname)s: %(message)s"})
    runner = CrawlerRunner()

    @defer.inlineCallbacks
    def crawl(self):
        """Runs the crawler runner inside of a twisted reactor

        Yields:
            The spiders running
        """
        runner = Process_Scraped_Data.runner
        yield runner.crawl(QuotesSpider)
        yield runner.crawl(AuthorSpider)
        reactor.stop()

    def save_sraped_data(self):
        """Calls the crawl method and run the reactor
        """
        self.crawl()
        reactor.run()