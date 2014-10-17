# coding:utf-8
import urllib2
import os

from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from helloscrapy.items import DoubanImageItem
from scrapy.http import Request

class DoubanImage(BaseSpider):
    name = 'doubanImage'
    allowed_domains = ['douban.com'] #域名
    start_urls = [
            'http://movie.douban.com/subject/1474243/photos?type=S',
            'http://movie.douban.com/subject/21327878/photos?type=S',
            'http://movie.douban.com/subject/24697949/photos?type=S'
            ]  #要爬的网站
    page = 0  # 页码
    count = 0  #计数
    title = ''  
    def parse(self, response):
        self.page += 1 #每次页码+1
        self.count = 0
        items = []  
        hxs = HtmlXPathSelector(response)  #
        self.title = hxs.select('//title/text()').extract()[0].strip().replace(' ', '_')
        sites = hxs.select('//ul/li/div/a/img/@src').extract()  # html的路径.
        for site in sites:
            site = site.replace('thumb', 'raw')  #因为点开原图,路径中thumb变成了raw.处理路径.
            item = DoubanImageItem()
            item['address'] = site
            items.append(item)
            self.count += 1
            self.download(site, self.title, self.page, self.count)
        #得到下一页的网站.
        nextPageSite = hxs.select("//div[@class='paginator']/span[@class='next']/a/@href").extract()[0]
        return Request(nextPageSite, callback = self.parse)  # 

    def download(self, site, title, page, count): #下载函数.
        try:
            u = urllib2.urlopen(site)  #打开站点
            r = u.read()  #读取站点html.
            # 下面是路径. 然后是标题_页码_第几张_格式.以.区分得到后缀
            savePath = '/home/zyvas/py-scrapy/helloscrapy/image/%s_%d_%d.%s'%(title, page,count,site.split('.')[-1])
            print 'Download...', savePath
            downloadFile = open(savePath,'wb') #二进制格式写入图片
            downloadFile.write(r)  
            u.close()
            downloadFile.close()
        except:
            print savePath, 'can not download.'

