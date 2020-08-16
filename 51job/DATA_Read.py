#encoding: utf-8
import pandas as pd
import pymongo
import jieba
from wordcloud import WordCloud
from matplotlib import pyplot as plt
import random
import re

client = pymongo.MongoClient()  # 链接pymongo数据库
collection = client['51Job']['Scrapy']
print("数据表名称：",collection.name)
data = collection.find()
df = pd.DataFrame(data)  # 读取整张表 (DataFrame)
print("包含数据%s条"%len(df))
del df['_id']#删除id列
df.drop_duplicates(['职位链接'],inplace = True)#去重，保留唯一值,inplace = True
print("去重之后剩余%s条信息"%len(df))

# key1 = input("请输入专业：")
# key2 = input("请输入关键字2：")
# key3 = input("请输入关键字3：")
# key4 = input("请输入关键字4：")
# get_data1 = df[df['职位信息'].str.contains('{}'.format(key1),case=False)]
# get_data2 = get_data1[df['职位信息'].str.contains('{}'.format(key2) ,case=False)]
# get_data3 = get_data2[df['职位信息'].str.contains('{}'.format(key3) ,case=False)]
# get_data = get_data3[df['职位信息'].str.contains('{}'.format(key4) ,case=False)]

get_data = df[df['工作岗位'].str.contains('java' ,case=False)]

print("得到有效数据%s条"%len(get_data))

def Get_Top_attr_value(name) :
    Data = get_data['{}'.format(name)].str.lower().value_counts()
    attr = list(Data.index)  # 列表形式，统计名称
    value = [int(i) for i in list(Data.values)]

    # attr = attr[:20]#取前20个属性
    # value = value[:20]#取前20个属性对应的值
    # value.append(sum(value[20:]))#对后20的所有值求和，设为第21
    # attr.append('其它')#对应添加后20的属性名
    return attr,value

work = ['3-4年经验', '不限', '5-7年经验', '2年经验', '1年经验', '8-9年经验', '10年以上经验']
"""工作经验-平均薪资"""
def Work_Salary():
    work_salas = get_data[get_data['工作经验'].str.contains('1年经验')]
    print(work_salas['平均薪资'])

    sums = [ sala for sala in work_salas['平均薪资'] if type(sala) == int]#工资列表
    avg = int(sum(sums)/int(len(sums)))

    return avg


edu = ['本科', '大专', '不限', '硕士', '中专', '中技']
"""学历要求-平均薪资"""
def Edu_Salary(Edu_name):
    work_salas = get_data[get_data['学历要求'].str.contains('{}'.format(Edu_name))]
    print(work_salas['学历要求'])
    sums = [sala for sala in work_salas['平均薪资'] if type(sala) == int]#工资列表
    avg = int(sum(sums)/int(len(sums)))#平均工资

    return avg


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


"""     箱线图     """
from pyecharts import options as opts
from pyecharts.charts import Boxplot
def boxpolt_base() -> Boxplot:
    v1 = [
        [850, 740, 900, 1070, 930, 850, 950, 980, 980, 880]
        + [1000, 980, 930, 650, 760, 810, 1000, 1000, 960, 960],
        [960, 940, 960, 940, 880, 800, 850, 880, 900]
        + [840, 830, 790, 810, 880, 880, 830, 800, 790, 760, 800],
    ]
    v2 = [
        [890, 810, 810, 820, 800, 770, 760, 740, 750, 760]
        + [910, 920, 890, 860, 880, 720, 840, 850, 850, 780],
        [890, 840, 780, 810, 760, 810, 790, 810, 820, 850, 870]
        + [870, 810, 740, 810, 940, 950, 800, 810, 870],
    ]
    c = Boxplot()
    c.add_xaxis(["expr1", "expr2"])\
        .add_yaxis("A", c.prepare_data(v1))\
        .add_yaxis("B", c.prepare_data(v2)
    ).set_global_opts(title_opts=opts.TitleOpts(title="BoxPlot-基本示例"))
    return c


# Work_Salary()
# Edu_Salary()
# City_Salary('')


# x,y = Get_Top_attr_value('工作经验')
# print(x,y)
#
# x,y = Get_Top_attr_value('学历要求')
# print(x,y)
#
# x,y = Get_Top_attr_value('工作岗位')
# print(x[:10])
# print(len(x))
# print(y[:10])

# x,y = Get_Top_attr_value('公司福利')
# print(x)
# print(len(x))
# print(y)
#

x,y = Get_Top_attr_value('城市')
print(x,y)

x,y = Get_Top_attr_value('招聘人数')
print(x,y)

# information = get_data['职位信息']
# text = ''
# for i in information:
#     for word in i:
#         text += word
# cut_word = ','.join(jieba.cut(text.lower(),cut_all=False))

# print(cut_word)

# text=re.sub('[^a-zA-Z],','',cut_word)
# print(cut_word)

# wcd = WordCloud(width=800, height=600, background_color='white').generate(text)
# # 自定义词云字体颜色，本例是黑色
# def grey_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
#     return "hsl(0, 0%%, %d%%)" % random.randint(0, 10)
# fig = plt.figure(figsize=(8, 6))
# plt.imshow(wcd.recolor(color_func=grey_color_func, random_state=3))
# plt.axis("off")
# plt.show()

"""两种方式的技能词云"""
#
# english_only = ''.join(x for x in cut_word if ord(x) < 256)
#
# wcd = WordCloud(width = 800,height = 400,background_color = 'white',margin=2).generate(english_only)
#
# #自定义词云字体颜色为黑色
# def grey_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
#     return "hsl(0, 0%%, %d%%)" % random.randint(0, 10)
# fig = plt.figure(figsize=(12,8))
# plt.imshow(wcd.recolor(color_func=grey_color_func, random_state=50),interpolation='bilinear')
# plt.axis("off")
# plt.show()








