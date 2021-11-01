import scrapy
from ..items import RoomInfoHzItem  # 相对引用items.py中定义的类


class RoomSpider(scrapy.Spider):
    name = "room_spider"
    start_urls = ["https://hz.zu.anjuke.com/fangyuan/",
                  "https://hz.zu.anjuke.com/fangyuan/p2"]
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
    }

    # 重写start_request 方法, 自行设置代理
    def start_requests(self):
        for url in RoomSpider.start_urls:
            yield scrapy.Request(url=url, callback=self.parse, headers=RoomSpider.headers)

    # 对获取的字符串类别进行清理
    @staticmethod
    def clean(info: list) -> list:
        result = []
        for x in info:
            x = x.strip()
            if x:
                result.append(x)
        return result

    def parse(self, response):
        for room in response.xpath('//div[@class="zu-itemmod"]'):
            yield {
                'title': room.xpath('.//h3/a/b//text()').extract_first().strip(),
                'price': int(room.xpath('./div[@class="zu-side"]//b/text()').extract_first()),
                'address': self.clean(room.xpath('.//address/a/text() | .//address/text()').extract()),
                'area': float(room.xpath('.//p[@class="details-item tag"]/b[3]/text()').extract_first()),
                'floor': room.xpath('.//p[@class="details-item tag"]/text()[5]').extract_first().strip(),
                'house_type': (int(room.xpath('.//p[@class="details-item tag"]/b[1]/text()').extract_first()),
                               int(room.xpath('.//p[@class="details-item tag"]/b[2]/text()').extract_first())),
                'rent_type': room.xpath('.//span[@class="cls-1"]/text()').extract_first(),
                'other': self.clean(room.xpath('.//p[@class="details-item bot-tag"]//text()').extract())[1:]
            }

        # next_page_url = response.xpath('//a[@class="aNxt"]/@href').extract_first()
        # if next_page_url:
        #     yield scrapy.Request(next_page_url)
