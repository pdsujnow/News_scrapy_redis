# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from News_scrapy.items import AitistsItem


# FIXME: some problems about allowed_domains, Fail to crawl article
class Xtecher(CrawlSpider):
    # 爬虫名
    name = "aitists"
    # 爬取域范围, 允许爬虫在这个域名下进行爬取
    allowed_domains = ["aitists.com", "https://mp.weixin.qq.com"]
    # 起始url列表, 爬虫执行后的第一批请求, 队列处理
    start_urls = ['http://www.aitists.com/']


    rules = (
        # 从起始页提取匹配正则式'/channel/\d{1,3}\.html'的链接，并使用parse来解析
        Rule(LxmlLinkExtractor(allow=(r'/category/.+', )), follow=True),
        # 提取匹配'/article/[\d]+.html'的链接，并使用parse_item_yield来解析它们下载后的内容，不递归
        Rule(LxmlLinkExtractor(allow=(r'/s/.+', )), callback='parse_item'),
    )


    def parse_item(self, response):
        item = AitistsItem()
        item['url'] = response.url
        item['title'] =  response.xpath('//*[@id="activity-name"]/text()').extract()[0].strip()
        item['pub_time'] = response.xpath('//*[@id="post-date"]/text()').extract()[0].strip()
        item['content_code'] = response.xpath('//*[@id="index_content"]/div[1]/div[4]').extract()[0]

        # 返回每个提取到的item数据, 给管道文件处理, 同时还会回来执行后面的代码
        yield item