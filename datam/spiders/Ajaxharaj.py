# -*- coding: utf-8 -*-
import datetime
import re
import time
from scrapy import Request, Spider
from datam.items import datamItem

#from mss.utils.strings import process_string


class DataM(Spider):

    name = "harajAjax"

    def start_requests(self):
        base_url = 'https://haraj.com.sa/jsonGW/getadsx.php?link=https://haraj.com.sa/tags/%D9%83%D9%84%20%D8%A7%D9%84%D8%AD%D8%B1%D8%A7%D8%AC/'
        for i in range(1, 500):
            url = base_url + str(i)
            yield Request(url, dont_filter=False, callback=self.parse_list)

    def parse_list(self, response):
        hrefs = response.xpath('//body/div[*]/div[1]/div[1]/a/@href').extract()
        for href in hrefs:
            yield Request(response.urljoin(href), callback=self.parse_details)

    def parse_details(self, response):
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
        #related=response.xpath('//div[contains (@class, "ads")]/div[*]/a[*]/@href').extract()
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