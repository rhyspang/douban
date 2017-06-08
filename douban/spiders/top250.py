# -*- coding: utf-8 -*-
import scrapy

from douban import settings
from douban.items import MovieItem


class Top250Spider(scrapy.Spider):
    name = "top250"
    base_url = 'https://movie.douban.com/top250'
    start_urls = ['https://www.douban.com/accounts/login']

    def parse(self, response):
        yield scrapy.FormRequest.from_response(
            response,
            formdata={'form_email': settings.DOUBAN_USERNAME, 'form_password': settings.DOUBAN_PASS},
            callback=self.after_login,
        )

    def after_login(self, response):
        urls = [self.base_url + '?start={}'.format(25 * i) for i in range(1)]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_page)

    def parse_page(self, response):
        detail_urls = response.xpath('//div[@class="info"]/div[@class="hd"]/a/@href').extract()
        for detail_url in detail_urls:
            yield scrapy.Request(url=detail_url, callback=self.parse_detail)

    def parse_detail(self, response):
        movie = MovieItem()
        movie['name'] = response.xpath('//span[@property="v:itemreviewed"]/text()').extract_first()
        movie['director'] = response.xpath('//a[@rel="v:directedBy"]/text()').extract_first()
        movie['year'] = response.xpath('/html/body/div[3]/div[1]/'
                                       'h1/span[2]/text()').re('(\d+)')[0]
        movie['stars'] = response.xpath('/html/body/div[3]/div[1]/'
                                        'div[3]/div[1]/div[1]/div[1]/div[1]/'
                                        'div[2]/span[3]/span[2]/a/text()').extract()
        movie['types'] = response.xpath('//span[@property="v:genre"]/text()').extract()
        movie['country'] = response.xpath('/html/body/div[3]/div[1]/'
                                          'div[3]/div[1]/div[1]/div[1]/'
                                          'div[1]/div[2]').re('制片国家/地区:</span>(.+)<br>')[0].strip()
        movie['language'] = response.xpath('/html/body/div[3]/div[1]/'
                                           'div[3]/div[1]/div[1]/div[1]/'
                                           'div[1]/div[2]').re('语言:</span>(.+)<br>')[0].strip()
        movie['runtime'] = response.xpath('//span[@property="v:runtime"]/@content').extract_first()

        movie['rating'] = response.xpath('//strong[@property="v:average"]/text()').extract_first()
        movie['url'] = response.url
        yield movie
