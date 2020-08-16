import requests
from lxml import etree
import time
import random
import re

# headers = {
#     'Host': 'www.lagou.com',
#     'Origin': 'https://www.lagou.com',
#     'Referer': 'https://www.lagou.com/jobs/list_python?city=%E5%85%A8%E5%9B%BD&cl=false&fromSearch=true&labelWords=&suginput=',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0',
# }
def get_headers():#设置随机请求头
    header_list=["Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
                 "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
                 "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
                 "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
                 "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36"
]
    User_Agent = random.choice(header_list)
    headers = {
    'Host': 'www.lagou.com',
    'Origin': 'https://www.lagou.com',
    'Referer': 'https://www.lagou.com/jobs/list_python?city=%E5%85%A8%E5%9B%BD&cl=false&fromSearch=true&labelWords=&suginput=',
        'Connection': 'keep - alive',
    'User-Agent': User_Agent,
}
    return headers

def get_json():
    data = {
        'first': 'true',
        'pn': 1,
        'kd': 'python'
    }
    r = session.post('https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput=',
                     headers=get_headers(), data=data)
    Ajax_url = 'https://www.lagou.com/jobs/positionAjax.json?city=%E4%B8%8A%E6%B5%B7&needAddtionalResult=false'
    resp = session.post(Ajax_url, headers=get_headers(), data=data)
    get_resp = resp.json()
    return get_resp

def parse_id_html():
    positions = get_json()['content']['positionResult']['result']
    for positionId in positions:
        Id = positionId['positionId']
        details_url = 'https://www.lagou.com/jobs/{}.html'.format(Id)  # 获取详情页的url
        print(details_url)
        details_resp = session.get(details_url, headers=get_headers())  # 获取详情页
        html = etree.HTML(details_resp.text)
        position_name = html.xpath('//div[@class="job-name"]/h1/text()')
        job_description = html.xpath('//*[@id="job_detail"]/dd[2]/div/p/text()')#职位描述
        job_request_spans = html.xpath("//dd[@class='job_request']//span")
        salary = job_request_spans[0].xpath(".//text()")[0].strip()
        city = job_request_spans[1].xpath(".//text()")[0].strip()
        city = re.sub(r"[\s/]", "", city)
        work_years = job_request_spans[2].xpath(".//text()")[0].strip()
        work_years = re.sub(r"[\s/]", "", work_years)
        education = job_request_spans[3].xpath(".//text()")[0].strip()
        education = re.sub(r"[\s/]", "", education)
        desc = "".join(html.xpath("//dd[@class='job_bt']//text()")).strip()
        print(position_name,salary,city,work_years,education,desc)
        print("="*30)

if __name__ == '__main__':
    session = requests.session()
    parse_id_html()
