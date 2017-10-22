# -*- coding: utf-8 -*-
from scrapy.spiders import Rule
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy_redis.spiders import RedisCrawlSpider
from News_scrapy.items import NewsItem


class Dgtle(RedisCrawlSpider):
    # 爬虫名
    name = "dgtle"
    # 爬取域范围, 允许爬虫在这个域名下进行爬取
    allowed_domains = ["dgtle.com"]
    # 起始url列表, 爬虫执行后的第一批请求, 队列处理
    redis_key = 'dgtle:start_urls'
    # start_urls = ['http://www.dgtle.com/']


    rules = (
        # 从起始页提取匹配正则式'/channel/\d{1,3}\.html'的链接，并使用parse来解析
        Rule(LxmlLinkExtractor(allow=(r'/portal.php\?mod=list&catid=\d{2}', )), follow=True),
        # 提取匹配'/article/[\d]+.html'的链接，并使用parse_item_yield来解析它们下载后的内容，不递归
        Rule(LxmlLinkExtractor(allow=(r'/article[\d|-]+\.html', )), callback='parse_item'),
    )


    def parse_item(self, response):
        item = NewsItem()
        item['url'] = response.url
        item['title'] =  response.xpath('/html/body/div[3]/h2/a/text()').extract()[0].strip()
        item['pub_time'] = response.xpath('/html/body/div[3]/div/div[1]/i/text()').extract()[0].strip()
        item['content_code'] = response.xpath('/html/body/div[4]/div[1]').extract()[0].strip()


        # 返回每个提取到的item数据, 给管道文件处理, 同时还会回来执行后面的代码
        yield item