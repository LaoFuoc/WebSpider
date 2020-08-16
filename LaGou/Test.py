#encoding: utf-8
from urllib.parse import quote
import requests
from  lxml import etree
import math
import time
import xlsxwriter
import pandas as pd

tag_name = ['公司名称','公司规模','融资阶段','城市','区域','职位名称','职位链接', '工作经验', '学历要求' ,'薪资','职位福利','职位详述']
fin_result = [[] for i in range(30)]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0',
    'X-Requested-With': 'XMLHttpRequest','X-Anit-Forge-Token': 'None',
    'Referer': 'https://www.lagou.com/jobs/list_python?city=%E5%85%A8%E5%9B%BD&cl=false&fromSearch=true&labelWords=&suginput='
}

def request_list_page(city_name,keyword,num):
    city_code=city_name
    if(city_name=='全国'):
        url='https://www.lagou.com/jobs/positionAjax.json?city=全国&needAddtionalResult=false'
    else:
        url='https://www.lagou.com/jobs/positionAjax.json?px=default&city=%s&needAddtionalResult=false'%city_code
    # print(url)
    data={
        'first':'true',
        'pn':num,
        'kd':keyword
    }
    session = requests.session()
    session.post('https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput=', headers=headers,data=data)
    response=session.post(url,headers=headers,data=data)
    result=response.json()
    return result

def get_page_num(counts):
    nums=math.ceil(counts/15)
    print(nums)
    if(nums>30):
        return 30
    else:
        return nums

def get_page_info(city,keyword,num):
    job = xlsxwriter.Workbook(r'%s.xls' % keyword)
    tmp=job.add_worksheet()
    tmp.write_row('A1',tag_name)
    ind = 2
    total_inf=[]
    for x in range(1,num+1):
        page=request_list_page(city,keyword,x)
        positions = page['content']['positionResult']['result']
        page_info_list=[]
        for position in positions:
            page_info = []
            page_info.append(position['companyFullName'])
            #page_info.append(position['companyShortName'])
            page_info.append(position['companySize'])
            page_info.append(position['financeStage'])
            page_info.append(position['city'])
            page_info.append(position['district'])
            page_info.append(position['positionName'])
            position_id = position['positionId']
            position_url = 'https://www.lagou.com/jobs/%s.html' % position_id
            page_info.append(position_url)
            page_info.append(position['workYear'])
            page_info.append(position['education'])
            page_info.append(position['salary'])
            page_info.append(position['positionAdvantage'])
            page_info.append(position_detail(position_url))
            con_pos='A%s'%ind
            tmp.write_row(con_pos,page_info)
            ind+=1
            page_info_list.append(page_info)
            time.sleep(1)
        if(x==4):
            break
        print("第{}页已经抓取完成".format(x))
        total_inf += page_info_list
        time.sleep(4)
    df = pd.DataFrame(data=total_inf,columns=tag_name)
    df.to_excel(city+'_'+keyword+'.xls')
    df.to_csv(city+'_'+keyword+'.csv',index=False)
    print("已保存为csv文件")
    job.close()

def position_detail(url):
    response=requests.get(url,headers=headers)
    text=response.text
    html=etree.HTML(text)
    desc="".join(html.xpath("//dd[@class='job_bt']//text()")).strip()
    return desc

if __name__ == '__main__':
    city=input("请输入你要查找的城市：")
    keyword = input('请输入您要搜索的语言类型：')
    page_1=request_list_page(city,keyword,1)

    total_page = page_1['content']['positionResult']['totalCount']
    num = get_page_num(total_page)
    print("共找到：{}条招聘信息，显示为{}页".format(total_page, num))
    result=get_page_info(city,keyword,num)

