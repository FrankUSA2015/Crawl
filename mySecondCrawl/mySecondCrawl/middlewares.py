# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import json
import traceback#处理异常的

class MysecondcrawlSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.
    date1=[]
    def __init__(self):
        file1 = open(r"E:\date\cookie\cookie.json", 'r')#添加cookie的文件所在的位置。
        self.date1 = json.load(file1)

    def process_request(self, request, spider):

        chrome_options = Options()
        chrome_options.add_argument('--headless')  # 使用无头谷歌浏览器模式
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        #chrome_options.add_argument('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36')
        # 指定谷歌浏览器路径
        self.driver = webdriver.Chrome(chrome_options=chrome_options,
                                       executable_path='C:\SOFT\soft1\chromedriver32\chromedriver.exe')#executable_path添加上你的chrome驱动的位置
        try:
            self.driver.get(request.url)
            print("已经发送出URL："+request.url)
            time.sleep(1)
            for dat1 in self.date1:
                self.driver.add_cookie(dat1)
            self.driver.refresh()  # 加了cookie必须刷新，不刷新没有效果
            js = "var q=document.documentElement.scrollTop=100000"#把网页下拉到最下面
            self.driver.execute_script(js)
            time.sleep(30)
            str1=request.url.rstrip("?diff=split").replace('/','_').replace('https:__github.com','').lstrip()
            aa = self.driver.find_elements_by_css_selector('div > include-fragment > div.js-diff-load-button-container > button > div')  # 找到网页并且点击需要加载的部分
            flage=0
            if len(aa):
                flage=1
                n=0
                temp=[]
                temp.append(request.url)
                ff1= open(r'E:\date\reget\url' + str1 + '.json', 'w')
                json.dump(temp, ff1, indent=1)
                print("数据存储完成！")
                ff1.close()
                for dat2 in aa:
                    try:
                        webdriver.ActionChains(self.driver).move_to_element(dat2).click(dat2).perform()
                        n=n+1
                        print("已经运行了："+request.url)
                        print(str(n))
                        time.sleep(1)
                        if n>=700:
                            ff1 = open(r'', 'w')
                            ff1.write(request.url + '\n')
                            ff1.close()
                            break
                    except Exception as e :
                        ff =open(r'', 'a')
                        traceback.print_exc(file=ff)#错误存储
                        ff.close()
            if flage!=0:
                time.sleep(30)
            print("网址："+request.url)
            print("数据下载完成！")
            html = self.driver.page_source
            self.driver.quit()
            return scrapy.http.HtmlResponse(url=request.url, body=html.encode('utf-8'), encoding='utf-8',
                                            request=request)
        except Exception as e:
            ff1 = open(r'', 'a')#存放错误所在的位置
            traceback.print_exc(file=ff1)  # 错误存储
            ff1.close()

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class MysecondcrawlDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
