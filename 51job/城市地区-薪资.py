#encoding: utf-8
import pandas as pd
import pymongo
from pyecharts import options as opts
from pyecharts.charts import Geo,Page
from pyecharts.globals import ChartType

client = pymongo.MongoClient()  # 链接pymongo数据库
collection = client['51Job']['Scrapy']
print("数据表名称：",collection.name)
data = collection.find()
df = pd.DataFrame(data)  # 读取整张表 (DataFrame)
print("包含数据%s条"%len(df))
del df['_id']#删除id列
df.drop_duplicates(['职位链接'],inplace = True)#去重，保留唯一值,inplace = True
print("去重之后剩余%s条信息"%len(df))
get_data = df[df['工作岗位'].str.contains('java' ,case=False)]
print("得到有效数据%s条"%len(get_data))

def Get_Top_attr_value(name):
    Data = get_data['{}'.format(name)].str.lower().value_counts()
    attr = list(Data.index)  # 列表形式，统计名称
    value = [int(i) for i in list(Data.values)]

    return attr, value

"""城市-平均薪资"""
def City_Salary(City_name):
    work_salas = get_data[get_data['城市'].str.contains('{}'.format(City_name))]
    sums = [sala for sala in work_salas['平均薪资'] if type(sala) == int]#工资列表
    avg = int(sum(sums)/int(len(sums)))#平均工资

    def Area_Salary():
        Data = work_salas['地区'].value_counts()
        attr = list(Data.index)
        value = [int(i) for i in list(Data.values)]
        print(attr)#统计地区
        print(value)#统计地区的数量

        return attr, value  #返回地区以及对应的数量

    return avg      #返回平均薪资

citys , values = Get_Top_attr_value('城市')
print(citys)        #各城市
print(values)   #城市招聘信息数量

City_Avg_Salary = []        #各城市平均薪资
for i in citys:
    try:
        Avg = City_Salary(i)
        if i == '异地招聘':
            continue
        else:
            City_Avg_Salary.append(Avg)
    except:
        Avg = 0
        City_Avg_Salary.append(Avg)

# citys.remove('异地招聘')
# print(citys)
print(City_Avg_Salary)

def geo_base() -> Geo:
    c = (
        Geo()
        .add_schema(maptype="china",)
        .add('',[list(z) for z in zip(citys[:120], values[:120])],symbol_size=16,type_=ChartType.EFFECT_SCATTER,)
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(visualmap_opts=opts.VisualMapOpts(is_calculable=True,min_=0,max_=2000,
                                                           pos_top='center',
                                                           ),#调整图例参数
                title_opts=opts.TitleOpts(title="全国Java招聘数量分布图",pos_left='center')
        )
    )

    return c

def geo_heatmap() -> Geo:
    c = (
        Geo()
        .add_schema(maptype="china")
        .add(
            "",
            [list(z) for z in zip(citys[:120], City_Avg_Salary[:120])],
            type_=ChartType.HEATMAP,
        )
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(
            visualmap_opts=opts.VisualMapOpts(pos_top='center',min_=0,max_=15000,),
            title_opts=opts.TitleOpts(title="全国Java薪资分布图",pos_left='center'),
        )
    )
    return c

page = Page()
page.add(geo_base(),geo_heatmap())
page.render('全国岗位薪资分布图.html')


