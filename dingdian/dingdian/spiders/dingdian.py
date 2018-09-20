import re
import scrapy
from scrapy import Request
from bs4 import BeautifulSoup
from dingdian.items import DingdianItem, DcontentItem
from dingdian.mysqlpipelines.sql import Sql

class MySpider(scrapy.Spider):
    name = "dingdian"
    allowed_domains = ['23us.so']
    base_url = 'https://www.23us.so/list/'

    def start_requests(self):
        for i in range(1, 10):
            url = self.base_url + str(i) + '_1' + '.html' #小说分类的url
            yield Request(url, self.parse)
        yield Request('https://www.23us.so/full.html', callback=self.parse) # 全本

    def parse(self, response):
        max_num = response.css('div.pagelink a.last::text').extract_first()

        for num in range(1, int(max_num) + 1):
            next_page = str(response.url)[:-7] + '_' + str(num) + '.html'
            if next_page is not  None:
                yield Request(next_page, callback=self.get_name)

    def get_name(self, response):
        tds = BeautifulSoup(response.text, 'lxml').find_all('tr', bgcolor='#FFFFFF')
        for td in tds:
            novelname = td.find('a').get_text()
            novelurl = td.find('a')['href']
            yield Request(novelurl, callback=self.get_chapterurl, meta={'name': novelname, 'url': novelurl})

    def get_chapterurl(self, response):
        item = DingdianItem()

        item['name'] = str(response.meta['name']).replace('\xa0', '')
        item['novelurl'] = response.meta['url']
        category = response.css('table a::text').extract_first()
        author = response.css('table td::text').extract()[1]

        # 最新章节
        bash_url = response.css('p.btnlinks a.read::attr(href)').extract_first()

        name_id = str(bash_url).split('/')[-2]

        item['category'] = str(category).replace('/', '')
        item['author'] = str(author).replace('/', '')
        item['name_id'] = name_id
        yield item

        yield Request(url=bash_url, callback=self.get_chapter, meta={'name_id': name_id})


    def get_chapter(self, response):
        num = 0
        urls = re.findall(r'<td class="L"><a href="(.*?)">(.*?)</a></td>', response.text)

        for url in urls:
            num = num + 1
            chapterurl = url[0]
            chaptername = url[1]
            rets = Sql.sclect_chapter(chapterurl)
            if rets[0] == 1:
                print('章节已经存在了')
                return False
            else:
                yield Request(chapterurl, callback=self.get_chaptercontent, meta={'num': num, 'name_id': response.meta['name_id'], 'chapterurl': chapterurl, 'chaptername': chaptername})


    def get_chaptercontent(self, response):
        item = DcontentItem()
        item['num'] = response.meta['num']
        item['id_name'] = response.meta['name_id']
        item['chaptername'] = str(response.meta['chaptername']).replace('\xa0', '')
        item['chapterurl'] = response.meta['chapterurl']
        content = response.css('dd#contents::text').extract()
        item['chaptercontent'] = str(content).replace('\xa0', '')
        yield item