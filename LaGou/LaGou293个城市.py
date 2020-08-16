# coding: UTF-8
import requests, time, csv, pymongo, random
citys = ['深圳', '上海', '苏州', '沈阳', '石家庄', '汕头', '绍兴', '宿迁', '三亚', '上饶', '韶关', '汕尾', '遂宁', '宿州', '三门峡', '邵阳', '十堰', '商丘', '三沙', '松原', '三明', '绥化', '朔州','天津', '太原', '唐山', '台州', '泰安', '泰州', '通辽', '铜陵', '天水', '铜川', '铁岭', '铜仁', '天门', '通化','武汉', '无锡', '温州', '乌鲁木齐', '潍坊', '芜湖', '威海', '乌兰察布', '渭南', '梧州', '武威', '乌海', '吴忠', '文山', '西安', '厦门', '徐州', '西宁', '香港特别行政区', '新乡', '邢台', '咸阳', '襄阳', '许昌', '信阳', '孝感', '宣城', '西双版纳', '湘潭', '咸宁', '湘西土家族苗族自治州', '忻州', '新余', '兴安盟','烟台', '扬州', '银川', '盐城', '宜昌', '运城', '榆林', '岳阳', '宜宾', '永州', '云浮', '阳江', '宜春', '雅安', '玉林', '玉溪','鹰潭', '益阳', '阳泉','伊犁', '延安', '营口','郑州', '珠海', '中山', '镇江', '淄博', '肇庆', '湛江', '株洲', '漳州', '张家口', '遵义', '长治', '枣庄', '周口', '舟山',  '资阳', '驻马店', '自贡', '昭通', '张家界','安庆', '安康', '安阳', '澳门特别行政区', '阿勒泰', '安顺', '鞍山','北京', '保定', '蚌埠', '包头', '宝鸡', '北海', '保山', '滨州', '巴中', '亳州', '毕节', '百色', '本溪','成都', '长沙', '重庆', '长春', '常州', '沧州', '赤峰', '潮州', '承德', '常德', '郴州', '滁州', '池州', '楚雄', '昌吉','东莞', '大连', '德阳', '德州', '大庆', '大同', '大理', '达州', '定西', '儋州', '东营', '迪庆','鄂尔多斯', '鄂州', '恩施','佛山', '福州', '阜阳', '抚州', '抚顺', '阜新', '防城港','广州', '贵阳', '桂林', '赣州', '广元', '贵港', '广安','杭州', '合肥', '哈尔滨', '惠州', '海口', '呼和浩特', '淮安', '湖州', '菏泽', '河源', '邯郸', '黄石', '衡阳', '海外', '衡水', '黄冈', '淮北', '汉中','呼伦贝尔', '淮南', '黄山', '河池', '红河', '怀化', '和田', '海东', '鹤壁', '鹤岗', '葫芦岛','济南', '金华', '嘉兴', '江门', '济宁', '吉林', '晋中', '吉安', '荆州', '揭阳', '焦作', '晋城', '九江', '荆门', '锦州', '景德镇', '金昌', '佳木斯','嘉峪关','昆明', '开封', '克拉玛依', '喀什','兰州', '洛阳', '廊坊', '临沂', '六安', '聊城', '柳州', '拉萨', '连云港', '乐山', '临汾', '泸州', '龙岩', '丽水', '凉山彝族自治州', '吕梁', '漯河','陇南', '丽江', '六盘水', '来宾', '临沧', '莱芜', '辽阳','绵阳', '眉山', '马鞍山', '茂名', '梅州', '牡丹江','南京', '宁波', '南昌', '南宁', '南通', '南阳', '南充', '宁德', '内江', '南平','濮阳', '莆田', '萍乡', '普洱', '盘锦', '平顶山', '攀枝花','青岛', '泉州', '秦皇岛', '清远', '衢州', '齐齐哈尔', '黔西南', '曲靖', '黔东南', '黔南', '庆阳', '钦州','日照','黔南', '庆阳', '钦州','日照']
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
    session.post('https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput=', headers=headers, data=data)
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
                    '地区':position['district'],
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
    collection = db[job+'11_27']
    for city in citys:
        page = 1
        print(city)
        url = 'https://www.lagou.com/jobs/positionAjax.json?city={}&needAddtionalResult=false'.format(city)
        while page < 50:  # 获取每一页的招聘信息
            # 这里传入三个参数，url和页数，以及工作岗位。获取每一页职位信息
            print("开始第%s页" % page)
            try:
                info = parse_json(get_json(url, page, job))
                page += 1
                if info == []:  # 如果没有获取到职位，跳出当前循环，开始下一个城市的爬取
                    break
                collection.insert_many(info)
            except TypeError as e:
                print(
                    "--------------------------------------------插入数据库出错----------------------------------------------")
            except Exception as e:
                print(
                    "--------------------------------------------获取页面失败----------------------------------------------")
            time.sleep(random.uniform(0, 1))  # 设置随机的延时，反反爬虫
    end = time.clock()
    print("总耗时:" + str(end - start))
    count = collection.find().count()
    print("获取到职位信息%s条" % count)

if __name__ == '__main__':
    main()
