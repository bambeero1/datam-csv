# -*- coding: utf-8 -*-
'''MSS: Google Play Store Spider'''
import re
import datetime
from datam.items import datamItem
from scrapy import Request, Spider
import time




class DataM(Spider):
        
    name = 'haraj_update_city'
    start_urls = [
        'https://haraj.com.sa/tags/الرياض_كل الحراج',
        'https://haraj.com.sa/tags/جده_كل الحراج',
        'https://haraj.com.sa/tags/الشرقيه_كل الحراج',
        'https://haraj.com.sa/tags/مكه_كل الحراج',
        'https://haraj.com.sa/tags/المدينة_كل الحراج',
        'https://haraj.com.sa/tags/أبها_كل الحراج',
        'https://haraj.com.sa/tags/القصيم_كل الحراج',
        'https://haraj.com.sa/tags/الطايف_كل الحراج',
        'https://haraj.com.sa/tags/تبوك_كل الحراج',
        'https://haraj.com.sa/tags/حائل_كل الحراج',
        'https://haraj.com.sa/tags/جيزان_كل الحراج',
        'https://haraj.com.sa/tags/حفر الباطن_كل الحراج',
        'https://haraj.com.sa/tags/نجران_كل الحراج',
        'https://haraj.com.sa/tags/الباحة_كل الحراج',
        'https://haraj.com.sa/tags/ينبع_كل الحراج',
        'https://haraj.com.sa/tags/الجوف_كل الحراج',
        'https://haraj.com.sa/tags/عرعر_كل الحراج',
        'https://haraj.com.sa/tags/الإمارات_كل الحراج',
        'https://haraj.com.sa/tags/الكويت_كل الحراج',
        'https://haraj.com.sa/tags/البحرين_كل الحراج',
        'https://haraj.com.sa/tags/قطر_كل الحراج',
                ]

    def parse(self, response):
        hrefs = response.xpath('//div[@class="adxTitle"]/a/@href').extract()
        for href in hrefs:
            if 'haraj.com' not in href:
                href = 'https://haraj.com.sa' + href
            yield Request(
                    href,
                    callback=self.parse_details,
                    )

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

