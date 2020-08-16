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
import urllib3

class QianChengWuYouSpider(object):
    def __init__(self):
        self.ua_list = [
                        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1',
                        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0',
                        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; InfoPath.3)']

        self.one_url = 'https://search.51job.com/list/000000,000000,0000,00,9,99,{},2,{}.html?'
        self.two_url = ''
        self.q = Queue()

    # 获取响应内容函数
    def get_page(self, url):
        headers = {'User-Agent': random.choice(self.ua_list)}
        urllib3.disable_warnings()
        html = requests.get(url, headers=headers, verify=False)
        html.encoding = 'gbk'
        html = etree.HTML(html.text)

        return html

    # 获取总页数
    def get_numbers(self):
        url = self.one_url.format(job,1)
        html = self.get_page(url)
        results = html.xpath('//*[@id="resultList"]/div[2]/div[4]/text()')[0].strip()
        nums = re.search('\d+', results)
        numbers = math.ceil(int(nums.group()) / 50)

        return numbers

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
                    position = result.xpath('./p/span/a/text()')[0].strip().lower()
                    LianJie = result.xpath('./p/span/a/@href')[0]
                    company = result.xpath('./span[1]/a/@title')[0].strip()
                    citys = result.xpath('./span[2]/text()')[0].strip()
                    citys = re.split(r'-', citys)
                    city = citys[0]
                    Area = citys[-1]
                    try:
                        salary = result.xpath('./span[3]/text()')[0].strip()
                        if '万/月' in salary:
                            sala1 = re.split(r'-', salary[:-3])
                            min = float(sala1[0])
                            max = float(sala1[1])
                            avgs = int(round((min + (max - min) * 0.4) * 10000, 0))

                        if '万/年' in salary:
                            sala2 = re.split(r'-', salary[:-3])
                            min = float(sala2[0])
                            max = float(sala2[1])
                            avgs = int(round((min + (max - min) * 0.4) / 12 * 10000, 0))

                        if '千/月' in salary:
                            sala3 = re.split(r'-', salary[:-3])
                            min = float(sala3[0])
                            max = float(sala3[1])
                            avgs = int(round((min + (max - min) * 0.4) * 1000, 0))

                        if '元/天' in salary:
                            sala4 = re.split(r'-', salary[:-3])
                            avgs = int(round(float(sala4[0]) * 30, 0))

                    except IndexError as e:
                        salary = '薪资面议'
                        avgs = '薪资面议'
                    times = result.xpath('./span[4]/text()')[0].strip()
                    two_url = LianJie
                    news = {'工作岗位': position, '公司名称': company, '城市': city, '地区': Area, '薪资范围':salary, '平均薪资': avgs, '发布时间': times, '职位链接': LianJie}
                    news['工作经验'],news['学历要求'],news['招聘人数'],news['公司福利'],news['公司类型'],news['公司规模'],news['职位信息'] = self.parse_two_page(two_url)
                    print(news)
                    info_list_db.append(news)

                collection.insert_many(info_list_db)
            else:
                break

    # 解析二级页面函数
    def parse_two_page(self, two_url):
        html = self.get_page(two_url)
        more = html.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/p[2]/text()')#多种信息
        workyear = '不限'
        edu = '不限'
        ZhaoRen = '招若干人'
        edulist = [ '初中及以下','高中', ]
        hight_edu = ['不限','中专', '中技','大专', '本科', '硕士', '博士',]

        for i in range(0,len(more)):
            #工作经验处理
            if '经验' in more[i]:
                if '无工作经验' in more[i]:
                    workyear = '不限'
                else:
                    workyear = more[i].strip()

            # 学历处理
            if more[i].strip() in hight_edu:
                edu = more[i].strip()
            if more[i].strip() in edulist:
                edu = '不限'

            # 招人处理
            if '招' in more[i]:
                if '招若干人' in more[i]:
                    ZhaoRen = '招若干人'
                else:
                    ZhaoRen = more[i].strip()

        results = html.xpath('/html/body/div[3]/div[2]/div[3]/div[1]/div//text()')#职位详情
        results = [x.strip() for x in results if x.strip().replace('微信分享','') != '']#去除空格，以及部分字
        results = '\n'.join(results)
        financeStage = ''.join(html.xpath('/html/body/div[3]/div[2]/div[4]/div[1]/div[2]/p[1]/text()'))
        companysize = ''.join(html.xpath('/html/body/div[3]/div[2]/div[4]/div[1]/div[2]/p[2]/text()'))
        try:
            welfare = html.xpath('/html/body/div[3]/div[2]/div[2]/div/div[1]/div/div//text()')  # 公司福利
            welfare = ','.join([x.strip() for x in welfare if x.strip() != ''])
        except:
            welfare = ''

        return workyear,edu,ZhaoRen,welfare,financeStage,companysize,results


    def main(self):
        # one_url入队列
        number = self.get_numbers()
        print("一共有%s页"%number)
        for page in range(1, number + 1):
            one_url = self.one_url.format(job,page)
            self.q.put(one_url)

        t_list = []
        for i in range(20):
            t = Thread(target=self.parse_page)
            t_list.append(t)
            t.start()

        for t in t_list:
            t.join()

if __name__ == '__main__':
    job = input("请输入你想要获取的职位名称：")
    start = time.time()
    client = pymongo.MongoClient()  # 链接pymongo数据库
    db = client['51Job']  # 创建数据库
    collection = db.java12_4111
    spider = QianChengWuYouSpider()
    spider.main()
    end = time.time()
    print("获取到职位信息%s条" % collection.find().count())
    print('执行时间:%.2f' % (end - start))

