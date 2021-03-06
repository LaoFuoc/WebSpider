#encoding: utf-8
import time
import json
import random
import requests

ua_list = [
  'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1',
  'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0',
  'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; InfoPath.3)',
]

class TencentSpider(object):
    def __init__(self):
        self.one_url = 'https://careers.tencent.com/tencentcareer/api/post/Query?timestamp=1563912271089&countryId=&cityId=&bgIds=&productId=&categoryId=&parentCategoryId=&attrId=&keyword=&pageIndex={}&pageSize=10&language=zh-cn&area=cn'
        self.two_url = 'https://careers.tencent.com/tencentcareer/api/post/ByPostId?timestamp=1563912374645&postId={}&language=zh-cn'
        self.f = open('tencent.json', 'a')  # 打开文件
        self.item_list = []  # 存放抓取的item字典数据

    # 获取响应内容函数
    def get_page(self, url):
        headers = {'User-Agent': random.choice(ua_list)}
        html = requests.get(url=url, headers=headers).text
        html = json.loads(html)  # json格式字符串转为Python数据类型

        return html

    # 主线函数: 获取所有数据
    def parse_page(self, one_url):
        html = self.get_page(one_url)
        item = {}
        for job in html['Data']['Posts']:
            item['name'] = job['RecruitPostName']  # 名称
            post_id = job['PostId']  # postId，拿postid为了拼接二级页面地址
            # 拼接二级地址,获取职责和要求
            two_url = self.two_url.format(post_id)
            item['duty'], item['require'] = self.parse_two_page(two_url)
            print(item)
            self.item_list.append(item)  # 添加到大列表中

    # 解析二级页面函数
    def parse_two_page(self, two_url):
        html = self.get_page(two_url)
        duty = html['Data']['Responsibility']  # 工作责任
        duty = duty.replace('\r\n', '').replace('\n', '')  # 去掉换行
        require = html['Data']['Requirement']  # 工作要求
        require = require.replace('\r\n', '').replace('\n', '')  # 去掉换行

        return duty, require

    # 获取总页数
    def get_numbers(self):
        url = self.one_url.format(1)
        html = self.get_page(url)
        numbers = int(html['Data']['Count']) // 10 + 1  # 每页有10个推荐

        return numbers

    def main(self):
        number = self.get_numbers()
        for page in range(1, 3):
            one_url = self.one_url.format(page)
            self.parse_page(one_url)

        # 保存到本地json文件:json.dump
        json.dump(self.item_list, self.f, ensure_ascii=False)
        self.f.close()


if __name__ == '__main__':
    start = time.time()
    spider = TencentSpider()
    spider.main()
    end = time.time()
    print('执行时间:%.2f' % (end - start))
