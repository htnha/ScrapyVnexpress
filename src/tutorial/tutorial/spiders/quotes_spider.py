import scrapy
from tutorial.items import BaiBaoItem

class QuotesSpider(scrapy.Spider):
    name = "vnexpress"

    def start_requests(self):
        urls = [
            'https://kenh14.vn/chao-nhe-mua-khai-truong-20220904231539784.chn',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        item = BaiBaoItem()
        item['title'] = response.xpath("//h1[@class='kbwc-title']/text()").get().strip()
        list_p = response.xpath("//div[@class='knc-content']//p//text()").getall()
        item['content'] = str(list_p)
        item['date'] = response.xpath("//span[@class='kbwcm-time']/text()").get().strip()
        item['url'] = response.request.url
        yield item