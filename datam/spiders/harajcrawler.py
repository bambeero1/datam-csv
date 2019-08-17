# -*- coding: utf-8 -*-
import re
import datetime
from datam.items import datamItem
from scrapy import Request
import time
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class harajCrawler(CrawlSpider):
    name = 'harajCrawler'
    allowed_domains = ['haraj.com.sa']
    start_urls = ['https://haraj.com.sa/']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//a[contains(@href,"/11")]'), callback='parse_item'),
        Rule(LinkExtractor(restrict_xpaths='//a[contains(@href,"/tags")]'), follow=True),
        Rule(LinkExtractor(restrict_xpaths='//a[contains(@href,"/city")]'), follow=True),
    )


    def parse_item(self, response):
        title = response.xpath(
            '//h3[@itemprop="name"]/text()').extract()[0].strip()
        usern = response.xpath(
            '//a[contains(@href, "/users/" )]/text()').extract()[0].strip()
        body = u"".join(response.xpath(
            '//div[@class="adxBody"]/text()').getall()).strip()
        try:
            contact = response.xpath(
                '//div[@class="contact"]//a/text()').extract()[0].strip()
            contact = re.sub('[^0-9]','', contact)
        except:
            contact = ''
        city = response.xpath(
            '//a[contains(@href, "/city/" )]/text()').extract()[0].strip()
        related=response.xpath('//div[contains (@class, "ads")]/div[*]/a[*]/@href').extract()
        #for url in related:
        #    url = 'https://haraj.com.sa' + url
        relatedtext = response.xpath(
            '//div[contains (@class, "ads")]/div[*]/a[*]/img/@alt').extract()
        relatedtext = [ x for x in [ x.strip() for x in relatedtext ] if x ]
        relatedtext = ','.join(relatedtext)
        if ',,,,,' in relatedtext:
            relatedtext = ''
        tags = response.xpath(
            '//a[contains(@class, "tag")]/text()').getall()
        tags = [ x for x in [ x.strip() for x in tags ] if x ]
        tags = set(tags)
        tags = ','.join(tags)
        images = ','.join(response.xpath(
            '//div[contains(@class,"adxBody")]//img/@src').extract())
        id = response.xpath(
            '//div[2]/div[1]/div[1]/div[1]/div[2]/div[2]/text()').extract()[0].strip()

        currentDT = datetime.datetime.now()
        date = str(currentDT)
        item = datamItem()
        item['usern'] = usern
        item['body'] = body
        item['title'] = title
        item['tags'] = tags
        item['images'] = images
        item['id'] = id
        item['date'] = date
        item['contact'] = contact
        item['url'] = response.url
        item['relatedtext'] = relatedtext
        item['city'] = city

        yield item
        for href in related:
            yield Request(
                response.urljoin(href),dont_filter=False,
                    callback=self.parse_item,
                    )