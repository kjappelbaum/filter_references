import scrapy
from scrapy.http import FormRequest
from scrapy.utils.response import open_in_browser
from scrapy.selector import HtmlXPathSelector
from scrapy.spiders import CrawlSpider, Rule
import requests
import re 
import pandas as pd 
from io import StringIO
from bs4 import BeautifulSoup
from lxml import html
from urllib.request import urlopen
from requests_html import HTMLSession
import html
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import pandas as pd 

class WaterSpider(scrapy.Spider):
    name = "water"
    start_urls = ["http://chemsearch.kovsky.net/index.php"]

    def __init__(self, reference=None):
        self.download_delay = 0.25
        self.reference = reference
    

    def parse(self, response):
        formdata = {'q': self.reference}
        yield FormRequest.from_response(response,
                                formnumber=0,
                                formdata=formdata,
                                callback=self.parse1)

    def parse1(self, response):
        is_redirect = response.xpath('/html/body/div/div/center/a[2]').extract()
        is_redirect = html.unescape(is_redirect[0])
        print(is_redirect)
        url = re.findall(r'"([^"]*)"', is_redirect)[0]
        print(url)
        self.parse_redirect_page(url)
        #else:
        #    ...

    def parse_redirect_page(self, url):
        session = HTMLSession()
        r = session.get(url)
        r.html.render(timeout=0, sleep=10)
        string = r.html.full_text
        search = re.findall(r'water.isotherm', string)
        result_list.append(
            {
                'reference' : self.reference, 
                'result': search
            })

if __name__ == '__main__':

    with open('test_list.txt', 'r') as tl:
        references = tl.readlines()

    result_list = []
    for reference in references:
        print(reference)
        reference = reference.strip('CrossRef').strip('CAS').strip('Pubmed')
        reference = ''.join(reference.split(',')[-4:])

        settings = get_project_settings()
        crawler = CrawlerProcess(settings)
        spider = WaterSpider()
        crawler.crawl(spider, reference)
        crawler.start()
    
    df = pd.DataFrame(result_list)
    print(df.head())