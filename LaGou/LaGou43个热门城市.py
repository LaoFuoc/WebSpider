# coding: UTF-8
import requests, time, csv, pymongo

citys = ['北京', '上海', '深圳', '广州', '杭州', '成都', '南京', '武汉', '西安', '厦门', '长沙', '天津',
         '重庆','郑州', '青岛', '合肥', '福州', '济南', '大连', '珠海', '无锡', '佛山', '东莞', '宁波', '常州', '沈阳','石家庄', '昆明', '南昌', '南宁',
         '哈尔滨', '海口', '中山', '惠州', '贵阳', '长春', '太原', '嘉兴', '泰安', '昆山', '烟台', '兰州', '泉州']

def get_json(url, page, job):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0',
        'X-Requested-With': 'XMLHttpRequest', 'X-Anit-Forge-Token': 'None',
        'Referer': 'https://www.lagou.com/jobs/list_python?city=%E5%85%A8%E5%9B%BD&cl=false&fromSearch=true&labelWords=&suginput='
    }
    data = {
        'first': 'true',
        'pn': page,
        'kd': job
    }
    session = requests.session()
    session.post('https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput=', headers=headers,data=data)
    res = session.post(url, headers=headers, data=data)
    return res

def parse_json(resp):
    res = resp.json()
    positions = res['content']['positionResult']['result']
    info_list = []
    for position in positions:
        try:
            details_url = 'https://www.lagou.com/jobs/{}.html'.format(position['positionId'])
            news = {'工作岗位': position['positionName'],  # 职位名称
                    '城市': position['city'],  # 城市
                    '地区':position['district'],#地区
                    '薪水': position['salary'],  # 薪水
                    '学历要求': position['education'],  # 学历要求
                    '工作经验': position['workYear'],  # 工作经验
                    '公司名称': position['companyFullName'],  # 公司名称
                    '融资类型': position['financeStage'],  # 融资阶段
                    '公司规模': position['companySize'],  # 公司大小
                    '发布时间': position['createTime'],  # 发布时间
                    '公司福利': position['companyLabelList'],  # 职位诱惑
                    '职位链接': details_url}  # 详情链接
        except Exception as e:
            print("--------------------------数据有问题，开始下一条---------------------------------------")
            continue
        info_list.append(news)
        # print(news)
    return info_list

def main():
    job = input("请输入工作：")  # 根据输入的职位爬取所有城市的招聘信息
    start = time.clock()
    client = pymongo.MongoClient()
    db = client.LaGou
    collection = db.city43[job]
    for city in citys:
        page = 1
        print(city)
        url = 'https://www.lagou.com/jobs/positionAjax.json?city={}&needAddtionalResult=false'.format(city)
        while page < 50:  # 获取每一页的招聘信息
            # 这里传入三个参数，url和页数，以及工作岗位。获取每一页职位信息
            print("开始第%s页"%page)
            try:
                info = parse_json(get_json(url, page, job))
                page += 1
                if info == []:  # 如果没有获取到职位，跳出当前循环，开始下一个城市的爬取
                    break
                collection.insert_many(info)
            except TypeError as e:
                print("--------------------------------------------插入数据库出错----------------------------------------------")
            except Exception as e:
                print("--------------------------------------------获取页面失败----------------------------------------------")
            time.sleep(1)
    end = time.clock()
    print("总耗时:"+str(end-start))

if __name__ == '__main__':
    main()



