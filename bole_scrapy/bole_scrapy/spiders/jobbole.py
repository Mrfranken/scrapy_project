# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.http import Request
from scrapy.loader import ItemLoader


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/'] #['http://blog.jobbole.com/']

    def parse(self, response):
        """
        1. 获取文章列表页中的文章的url并交给解析函数进行解析
        2. 作为回调函数解析获取下一页文章的列表
        :param response:
        :return:
        """

        # 解析列表页中所有文章的url
        article_url_xpath = '//a[@class="archive-title"]/@href'
        all_articles_url = response.xpath(article_url_xpath).extract()
        for article_url in all_articles_url:
            yield Request(article_url, callback=self.parse_detail)

        # 解析下一页文章
        next_page_xpath = '//a[@class="next page-numbers"]/@href'
        next_page_url = response.xpath(next_page_xpath).extract_first()
        if next_page_url:
            yield Request(next_page_url, callback=self.parse)

    def parse_detail(self, response):
        """
        作为回调函数解析文章的详细内容
        :param response:
        :return:
        """
        article_title_xpath = '//div[@class="entry-header"]/h1/text()'
        article_date_xpath = '//p[@class="entry-meta-hide-on-mobile"]/text()'
        article_tag_xpath = '//p[@class="entry-meta-hide-on-mobile"]//a'
        article_like_num_xpath = '//span[contains(@class, "vote-post-up")]/h10/text()'
        article_collect_num_xpath = '//span[contains(@class, "bookmark-btn")]/text()'
        article_comment_num_xpath = '//div[@class="post-adds"]//i[contains(@class, "fa-comments-o")]/../text()'

        article_title = response.xpath(article_title_xpath).extract_first()
        article_date = response.xpath(article_date_xpath).extract_first().strip().split(' ')[0]
        article_tags = response.xpath('//p[@class="entry-meta-hide-on-mobile"]//a/text()').extract()
        article_tag = [tag for tag in article_tags if not tag.strip().endswith(r'评论')]

        article_like_num = int(response.xpath(article_like_num_xpath).extract_first())

        article_collects = response.xpath(article_collect_num_xpath).extract_first().strip()
        is_exist_collect = re.match('(\d+)', article_collects)
        if is_exist_collect:
            article_collect = int(is_exist_collect.group(1))
        else:
            article_collect = 0

        article_comments = response.xpath(article_comment_num_xpath).extract_first().strip()
        is_exist_comment = re.match('(\d+)', article_comments)
        article_comment = int(is_exist_comment.group(1)) if is_exist_comment else 0
