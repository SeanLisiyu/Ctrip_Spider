# -*- coding: utf-8 -*-
import scrapy
import re
import string
from urllib import parse
from scrapy.http import Request
from ctrip_spider.items import CtripItermLoader
from ctrip_spider.items import CtripItem

# from ctrip_spider.zhihu_login import LoginZhiHu


class CtripSpiderSpider(scrapy.Spider):
    name = 'ctrip_spider'
    allowed_domains = ['vacations.ctrip.com']
    start_urls = ['http://vacations.ctrip.com/']
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"
    }

    # def login(self):
    #     login = LoginZhiHu("18221669254", "lsy13485340785")
    #     login.read_cookie_login()
    #     if login.verify_login():
    #         resp = login.session.get('https://www.zhihu.com/', headers=login.login_header)
    #         index_file = open("ZhiHu_index.html", mode="w+", encoding="utf-8")
    #         index_file.write(resp.text)
    #         index_file.close()

    # https://vacations.ctrip.com/whole-0B126/?searchValue=%E8%9C%9C%E6%9C%88%E6%B8%B8&searchText=%E8%9C%9C%E6%9C%88%E6%B8%B8

    def get_the_honey_moon(self, response):
        url = response.css("div.destination_col a#vac-103045-left-dest-2-蜜月游-2::attr(href)").extract_first()
        url = parse.urljoin("https:", url)
        return [scrapy.Request(url, headers=self.headers, callback=self.parse)]

    def start_requests(self):
        return [scrapy.Request(self.start_urls[0], callback=self.get_the_honey_moon)]

    def parse(self, response):

        """
        :param response:
        :return:

        1、获取列表url，并交给scrapy下载后解析
        2、获取下一页的URL 并交给scrapy进行下载，下载后交给parse
        """
        vendors = []
        node_list = response.css("div.product_main")
        for node in node_list:
            vendor_text = node.css("p.product_retail::text").extract()
            if len(vendor_text)>0:
                vendors.append(vendor_text[len(vendor_text)-1].replace("供应商：", ""))

        node_list = response.css("div.product_pic")
        i = 0
        for node in node_list:
            url = node.css("a::attr(href)").extract_first()
            url = parse.urljoin(response.url, url)
            trip_type = node.css("em::text").extract_first()
            yield Request(url, headers=self.headers, meta={"trip_type": trip_type, "vendor": vendors[i]},  callback=self.get_the_detail_info)
            i = i + 1
        pass
        # "//vacations.ctrip.com/whole-2B126P2/?searchValue=%e8%9c%9c%e6%9c%88%e6%b8%b8&amp;searchText=%e8%9c%9c%e6%9c%88%e6%b8%b8"
        next_pg = response.css("div#_pg a.down::attr(href)").extract_first()
        page_num_str = re.match(".*?P(\d+)/", next_pg, re.S).group(1)
        page_num = int(page_num_str)
        if page_num < 11:
            next_pg = parse.urljoin("https:", next_pg)
            yield Request(next_pg, headers=self.headers, callback=self.parse)

    def get_the_detail_info(self, response):

        trip_type = response.meta.get("trip_type", "")
        vendor = response.meta.get("vendor", "")
        if vendor == "携程自营":
            item_loader = CtripItermLoader(item=CtripItem(), response=response)
            item_loader.add_css("num", "div.prd_num::text")
            item_loader.add_value("url", response.url)
            # item_loader.add_value("trip_type", response.meta["trip_type"])
            item_loader.add_css("title", 'title::text')
            item_loader.add_css("price", "span.total_price em::text")
            item_loader.add_css("img_urls", 'img.pil-figure-image-placeholder::attr(src)')
            item_loader.add_value("trip_type", trip_type)
            item_loader.add_css("destination","a[data-reactid='8']::text")
            item_loader.add_value("vendor",vendor)
            item_loader.add_css("guarantee", "dd.service_guarantee span::text")
            ctrip_item = item_loader.load_item()
            yield ctrip_item
        pass
