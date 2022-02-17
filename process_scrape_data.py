# Runs the spiders and methods that process the scraped data, then save it to the sqlite database
from quotes_scrapy.quotes_scrapy.spiders.quotes_spider import Process_Scraped_Data

process_data = Process_Scraped_Data()
process_data.save_sraped_data()