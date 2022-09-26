import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from tutorial.items import BaiBaoItem
import re


def strip_value(value):
    m = re.search("http[^\s]+(\s)*h?(http[^\s>]+)(\s)*", value)
    if m:
        # print m.group(2).encode('UTF-8')
        return m.group(2)
    else:
        # print value.encode('UTF-8')
        return value

class QuotesSpider(CrawlSpider):
    name = "baodautu"
    allowed_domains = ['baodautu.vn']
    start_urls = [
            'https://baodautu.vn/batdongsan/',
            'https://baodautu.vn/quoc-te-d54/',
    ]
    rules = (

        Rule(LinkExtractor(allow='',
                           deny=['/abc/'],
                           process_value=strip_value,
                           restrict_xpaths=["//nav[@class='d-flex pagation align-items-center']"]), follow=True, process_links=None),
        Rule(LinkExtractor(allow='',
                           deny=['/abc/'],
                           process_value=strip_value,
                           restrict_xpaths=["//a[@class='fs22 fbold']"]), follow=False, callback='parse_item',
             process_links=None)
    )
    def parse_item(self, response):
        print('Parse Item>>>>>>>>>>>>>>>>>>>>>')
        item = BaiBaoItem()
        item['category'] = response.xpath("//div[@class='fs16 text-uppercase ']/a/text()").get().strip()
        item['title'] = response.xpath("//div[@class='title-detail']/text()").get().strip()
        item['image'] = response.xpath("//div[@id='content_detail_news']//img/@src").get().strip()
        list_p = response.xpath("//div[@id='content_detail_news']//p//text()").getall()
        item['content'] = str(list_p)
        item['date'] = response.xpath("//span[@class='post-time']/text()").get().strip().replace("-", "")
        item['url'] = response.request.url
        return  item



    # def start_requests(self):
    #     urls = [
    #         'https://kenh14.vn/star.chn',
    #         'https://kenh14.vn/tv-show.chn'
    #     ]
    #     for url in urls:
    #         yield scrapy.Request(url=url, callback=self.parse)
    #
    # def parse(self, response):
    #
    #     item = BaiBaoItem()
    #     item['title'] = response.xpath("//h1[@class='kbwc-title']/text()").get().strip()
    #     list_p = response.xpath("//div[@class='knc-content']//p//text()").getall()
    #     item['content'] = str(list_p)
    #     item['date'] = response.xpath("//span[@class='kbwcm-time']/text()").get().strip()
    #     item['url'] = response.request.url
    #     yield item