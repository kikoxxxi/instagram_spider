# -*- coding:utf-8 -*-

__author__ = 'kikoxxxi'

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import json
import scrapy
import requests
from lxml import etree
from scrapy.http import Request
from scrapy.exceptions import CloseSpider
from ..items import InstagramSpiderItem
from ..mongodb import mongodb_operations
from ..mongodb.mongodb_operations import MongodbOperations


class AhmadMonkSpider(scrapy.Spider):
    name = 'jacobbix_spider'
    proxy = {
        'http': 'http://127.0.0.1:1087',
        'https': 'https://127.0.0.1:1087'
    }
    query_hash = '472f257a40c653c64c666ce877d59d2b'
    query_id = '7609498'
    query_name = 'jacobbix'
    url = 'https://www.instagram.com/jacobbix/'
    headers = {
        "Referer": "https://www.instagram.com/jacobbix/",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Upgrade-Insecure-Requests": "1",
    }

    def start_requests(self):
        return [Request(url=self.url, headers=self.headers, meta={'download_timeout': 6, "is_first_page": True}, callback=self.parse)]

    def parse(self, response):
        data = self.get_data(response.text)  # 获取包含图片URL等信息的json数据块,并存储为dict
        # 第一页json数据结构不同于其他页面
        # 设置第一页的总数据节点
        if response.meta["is_first_page"]:
            common_node = data[
                "entry_data"]["ProfilePage"][0]["graphql"]["user"]["edge_owner_to_timeline_media"]
        # 设置其他页面的总数据节点
        else:
            common_node = data["data"]["user"]["edge_owner_to_timeline_media"]
        item = InstagramSpiderItem()
        data_nodes = common_node["edges"]
        # 获取每张图片我所需要的信息
        for data_node in data_nodes:
            data_node = data_node["node"]
            mongodb = MongodbOperations("Query")
            # 获取该图片对应的具体详情网址
            shortcode = data_node["shortcode"]
            original_url = 'https://www.instagram.com/p/{}/?taken-by={}'.format(
                shortcode, self.query_name)
            if mongodb.find_one(original_url):
                raise CloseSpider("更新完毕！！！！！！！！")
            else:
                item["original_url"] = original_url
                try:
                    # 取值取决于发布者有没有为该图片配文
                    item["image_text"] = data_node["edge_media_to_caption"]["edges"][0]["node"]["text"]
                except IndexError, KeyError:
                    item["image_text"] = ""
                item["image_url"] = data_node["display_url"]
                item["comment_count"] = data_node["edge_media_to_comment"]["count"]
                item["preview_like_count"] = data_node["edge_media_preview_like"]["count"]
                # instagram为用户提供三种分享类型：单张图片发布、多张图片发布、视频发布
                # 对于多张图片类型，需进入图片详情网址抓取每张图片的url
                item["type_name"] = data_node["__typename"]
                # 获取多张图片分享类型的每张图片的url
                if item["type_name"] == "GraphSidecar":
                    image_urls = self.get_sidecar_image_urls(original_url)
                    item["image_url"] = image_urls
                yield item

        has_next_page = common_node["page_info"]["has_next_page"]
        end_cursor = common_node["page_info"]["end_cursor"]
        # 翻页
        if has_next_page:
            next_page_url = 'https://www.instagram.com/graphql/query/?query_hash=%s&variables={"id":"%s","first":12,"after":"%s"}' % (
                self.query_hash, self.query_id, end_cursor)
            yield Request(url=next_page_url, headers=self.headers, meta={'download_timeout': 6, 'is_first_page': False}, callback=self.parse)

    # 获取包含图片URL等信息的json数据块,返回数据类型为dict
    def get_data(self, html_content):
        html = etree.HTML(html_content)
        # 第一页网页结构不同于其他页面
        # 第一页数据
        if html.xpath('//script[contains(., "window._sharedData")]/text()'):
            json_data = html.xpath(
                '//script[contains(., "window._sharedData")]/text()')  # 找到包含图片URL等信息的json数据块
            data = json.loads(json_data[0].replace(
                "window._sharedData = ", "")[:-1])  # 清理数据即开头多余部分以及最后的分号，并转成dict
        # 其他页面的数据
        else:
            data = json.loads(html_content)
        return data

    # 获取多张图片发布类型的每张图片的url
    def get_sidecar_image_urls(self, sidecar_url):
        result = requests.get(
            sidecar_url, headers=self.headers, proxies=self.proxy).text
        data = self.get_data(result)
        data_nodes = data[
            "entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]["edge_sidecar_to_children"]["edges"]
        sidecar_image_urls = [data_node["node"]["display_url"]
                              for data_node in data_nodes]
        return sidecar_image_urls
