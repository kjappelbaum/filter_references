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

    def __init__(self, reference_list=None):
        self.download_delay = 0.25
        self.reference_list = reference_list
    

    def parse(self, response):
        for reference in self.reference_list:
            self.reference = reference 
            formdata = {'q': reference}
            yield FormRequest.from_response(response,
                                    formnumber=0,
                                    formdata=formdata,
                                    callback=self.parse1)

    def parse1(self, response):
        is_redirect = response.xpath('/html/body/div/div/center/a[2]').extract()
        is_redirect = html.unescape(is_redirect[0])
        url = re.findall(r'"([^"]*)"', is_redirect)[0]
        self.parse_redirect_page(url)


    def parse_redirect_page(self, url):
        session = HTMLSession()
        r = session.get(url)
        r.html.render(timeout=0, sleep=10)
        string = r.html.full_text
        search = re.findall(r'isotherm', string)
        with open('result_log.txt', 'w+') as rl:
            rl.write(self.reference + ' ' +  ''.join(search))

if __name__ == '__main__':

    with open('test_list.txt', 'r') as tl:
        references = tl.readlines()

    result_list = []
    reference_list = []
    for reference in references:
        print(reference)
        reference = reference.replace('CrossRef', '').replace('CAS', '').replace('PubMed', '')
        reference = ','.join(reference.split(',')[-4:])
        reference_list.append(reference)

        # settings = get_project_settings()
    crawler = CrawlerProcess()
    spider = WaterSpider()
    crawler.crawl(spider, reference_list)
    crawler.start()
    
