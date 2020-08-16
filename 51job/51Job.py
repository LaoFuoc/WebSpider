#encoding: utf-8
import requests
from lxml import etree
import time
import re
import math
import pymongo

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0',
        'Referer': 'https://www.51job.com/',
        'Host': 'search.51job.com'
    }
session = requests.session()

client = pymongo.MongoClient()  # 链接pymongo数据库
db = client['51Job']  # 创建数据库
collection = db.java11_27
job = input("请输入想要获取的职位名称:")
start = time.clock()
for i in range(1,2000):
    url = 'https://search.51job.com/list/000000,000000,0000,00,9,99,{},2,{}.html?'.format(job,i)
    response = session.get(url, headers=headers)
    response.encoding = 'gbk'
    html = etree.HTML(response.text)

    counts = html.xpath('//div[@id="resultList"]//div[@class="rt"]/text()')[0].strip()
    nums = re.search('\d+', counts)
    page = math.ceil(int(nums.group()) / 50)
    time.sleep(2)
    print("一共发现%s条职位信息，共%s页" % (nums.group(), page))

    try:
        results = html.xpath('//div[@id="resultList"]/div[@class="el"]')
        info_list_csv = []
        info_list_db = []
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
            news = {'职位名': position, '公司名': company, '工作地点': city, '薪资': salary, '发布时间': times, '职位链接': LianJie}
            info = [position, company, city, salary, times, LianJie]
            print(info)
            info_list_db.append(news)
            # info_list_csv.append(info)
        collection.insert_many(info_list_db)
    except:
        break
end = time.clock()
print("总耗时:"+str(end-start))
count = collection.find().count()
print("获取到职位信息%s条"%count)

# with open('51Job.csv','w',encoding='gbk',newline='') as fp:
#     title = ['职位名','公司名','工作地点','薪资','发布时间', '职位链接']
#     writer = csv.writer(fp)
#     writer.writerow(title)
#     writer.writerows(info_list_csv)

"""使用BeautifulSoup解析网页"""
# soup = BeautifulSoup(response.content.decode('gbk'), 'lxml')
# resultLists = soup.find('div',class_='dw_table')
# for resultList in resultLists:
#     try:
#         position = resultList.p.span.a.attrs['title']
#         company = resultList.find("span", {"class": "t2"}).a.attrs['title']
#         city = resultList.find("span", {"class": "t3"}).string
#         salary = resultList.find("span", {"class": "t4"}).string
#         time = resultList.find("span", {"class": "t5"}).string
#         info = [position, company, city, salary, time]
#         print(info)
#     except AttributeError as e:
#         pass



