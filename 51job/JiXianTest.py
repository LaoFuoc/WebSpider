#encoding: utf-8
import requests
from lxml import etree
import time
import random
from threading import Thread
from queue import Queue
import pymongo
import re
import math

ua_list = [
  'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1',
  'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0',
  'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; InfoPath.3)',
]

class TencentSpider(object):
    def __init__(self):
        self.one_url = 'https://search.51job.com/list/000000,000000,0000,00,9,99,java,2,{}.html?'
        self.two_url = ''
        self.q = Queue()

    # 获取响应内容函数
    def get_page(self, url):
        headers = {'User-Agent': random.choice(ua_list)}
        html = requests.get(url, headers=headers)
        html.encoding = 'gbk'
        html = etree.HTML(html.text)

        return html

    # 主线函数: 获取所有数据
    def parse_page(self):
        while True:
            if not self.q.empty():
                one_url = self.q.get()
                html = self.get_page(one_url)
                results = html.xpath('//div[@id="resultList"]/div[@class="el"]')
                info_list_db = []
                news = {}
                for result in results:
                    position = result.xpath('./p/span/a/text()')[0].strip()
                    LianJie = result.xpath('./p/span/a/@href')[0]
                    company = result.xpath('./span[1]/a/@title')[0].strip()
                    city = result.xpath('./span[2]/text()')[0].strip()
                    try:
                        salary = result.xpath('./span[3]/text()')[0].strip()
                    except IndexError as e:
                        salary = '薪资面议'
                    times = result.xpath('./span[4]/text()')[0].strip()
                    two_url = LianJie
                    news = {'职位名': position, '公司名': company, '工作地点': city, '薪资': salary, '发布时间': times, '职位链接': LianJie}
                    # news['工作经验'],news['学历要求'],news['招人'],news['职位信息'] = self.parse_two_page(two_url)
                    print(news)
                    info_list_db.append(news)
                collection.insert_many(info_list_db)
                # time.sleep(random.uniform(0, 1))
            else:
                break

    # 解析二级页面函数
    # def parse_two_page(self, two_url):
    #     html = self.get_page(two_url)
    #     more = html.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/p[2]/text()')
    #     workyear = '不限'
    #     edu = '不限'
    #     Recruit = '不限'
    #     for i in range(0,len(more)):
    #         if '经验' in more[i]:
    #             workyear = more[i].strip()
    #         if '中' in more[i]:
    #             edu = more[i].strip()
    #         if '专' in more[i]:
    #             edu = more[i].strip()
    #         if '本' in more[i]:
    #             edu = more[i].strip()
    #         if '士' in more[i]:
    #             edu = more[i].strip()
    #         if '招' in more[i]:
    #             Recruit = more[i].strip()
    #     # print(workyear,edu,Recruit)
    #     results = html.xpath('/html/body/div[3]/div[2]/div[3]/div[1]/div//text()')
    #     results = [x.strip() for x in results if x.strip().replace('微信分享','') != '']
    #
    #     return workyear,edu,Recruit,results

    # 获取总页数
    def get_numbers(self):
        url = self.one_url.format(1)
        html = self.get_page(url)
        results = html.xpath('//*[@id="resultList"]/div[2]/div[4]/text()')[0].strip()
        nums = re.search('\d+', results)
        numbers = math.ceil(int(nums.group()) / 50)

        return numbers

    def main(self):
        # one_url入队列
        number = self.get_numbers()
        for page in range(1, number + 1):
            one_url = self.one_url.format(page)
            self.q.put(one_url)

        t_list = []
        for i in range(20):
            t = Thread(target=self.parse_page)
            t_list.append(t)
            t.start()

        for t in t_list:
            t.join()


if __name__ == '__main__':
    start = time.time()
    client = pymongo.MongoClient()  # 链接pymongo数据库
    db = client['51Job']  # 创建数据库
    collection = db.JiXianTest
    spider = TencentSpider()
    spider.main()
    end = time.time()
    count = collection.find().count()
    print("获取到职位信息%s条" % count)
    print('执行时间:%.2f' % (end - start))
