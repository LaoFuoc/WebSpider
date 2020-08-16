import requests
import math
import time
import csv

def get_json(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0',
        'X-Requested-With': 'XMLHttpRequest', 'X-Anit-Forge-Token': 'None',
        'Referer': 'https://sou.zhaopin.com/?jl=551&kw=python&kt=3&sf=0&st=0'
    }
    session = requests.session()
    res = session.get(url,headers=headers)
    return res

def parse_json(res):
    resp = res.json()
    positions = resp['data']['results']
    info_list=[]
    for position in positions:
        jobName = position['jobName']#工作岗位
        company = position['company']['name']#公司名称
        type = position['company']['type']['name']#融资类型
        size = position['company']['size']['name']#公司规模
        city = position['city']['display']#城市
        updateDate = position['updateDate']#发布时间
        salary = position['salary']#薪水
        eduLevel = position['eduLevel']['name']#学历要求
        if ("workingExp" in position):
            workingExp = position['workingExp']['name']#工作经验
        else:
            workingExp = '无经验'
        positionURL = position['positionURL']#职位链接
        welfare = position['welfare']#公司福利
        info = [jobName,city,salary,eduLevel,workingExp,company,type,size,updateDate,welfare,positionURL]
        print(info)#打印每一条招聘信息
        info_list.append(info)
    return info_list

def get_page_num(count):
    page_num = math.ceil(count / 89)
    print("一共有%d页招聘信息"%page_num)
    return page_num

if __name__ == '__main__':
    url = 'https://fe-api.zhaopin.com/c/i/sou?pageSize=90&cityId=551&workExperience=-1&education=-1&companyType=-1&employmentType=-1&jobWelfareTag=-1&kw=python&kt=3'
    resp = get_json(url)
    infolist = parse_json(resp)
    # print(infolist)
    resp = resp.json()
    counts = resp['data']['count']
    time.sleep(3)
    for i in range(2,get_page_num(counts)+1):
        url = 'https://fe-api.zhaopin.com/c/i/sou?start={}&pageSize=90&cityId=551&salary=0,0&workExperience=-1&education=-1&companyType=-1&employmentType=-1&jobWelfareTag=-1&kw=python&kt=3'.format((i-1)*90)
        print(url)
        resp = get_json(url)
        infolists = parse_json(resp)
        infolist += infolists#整合所有的信息到一个列表
        time.sleep(3)
    print(len(infolist))
    with open('ZhiLian-ZhaoPin.csv','w',newline='',encoding='utf-8-sig') as fp:
        title = ['工作岗位', '城市', '薪水', '学历要求', '工作经验', '公司名称', '融资类型', '公司规模', '发布时间', '公司福利', '职位链接']
        writer = csv.writer(fp)
        writer.writerow(title)
        writer.writerows(infolist)
