#encoding: utf-8
import pandas as pd
import pymongo

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

edu = ['本科', '大专', '不限', '硕士', '中专', '中技']

"""学历要求-平均薪资"""
#全国部分
def Edu_Salary(Edu_name):
    work_salas = get_data[get_data['学历要求'].str.contains('{}'.format(Edu_name))]
    sums = [sala for sala in work_salas['平均薪资'] if type(sala) == int]#工资列表
    avg = int(sum(sums)/int(len(sums)))

    return avg

#单个城市
def One_City(Edu_name,city):
    work_salas = get_data[get_data['学历要求'].str.contains('{}'.format(Edu_name))]
    ChongQing = work_salas[work_salas['城市'].str.contains('{}'.format(city))]
    CQ_sum = [sala for sala in ChongQing['平均薪资'] if type(sala) == int]  # 工资列表
    try:
        if len(CQ_sum) < 3:    #过滤掉只包含三个职位的学历
            avg = 0
        else:
            avg = int(sum(CQ_sum) / int(len(CQ_sum)))
    except:
        avg = 0
    return avg

edul = ['不限','中技','中专','大专','本科','硕士']


#单个城市，招聘数量统计
def A_Ctiys(city):
    value_edul = []
    A_City = get_data[get_data['城市'].str.contains('{}'.format(city))]
    Data1 = A_City['学历要求'].value_counts()
    for i in edul:
        try:
            value_edul.append(int(Data1[i]))
            # if int(Data1[i]) == 1:
            #     value_edul.append(0)
            # else:
            #     value_edul.append(int(Data1[i]))
        except:
            value_edul.append(0)
    return value_edul

value_edu1 = A_Ctiys('重庆')
value_edu2 = A_Ctiys('北京')
value_edu3 = A_Ctiys('上海')
value_edu4 = A_Ctiys('广州')
value_edu5 = A_Ctiys('深圳')
value_edu6 = A_Ctiys('成都')
print('重庆',value_edu1,'\n','北京',value_edu2,'\n','上海',value_edu3,
      '\n','广州',value_edu4,'\n','深圳',value_edu5,'\n','成都',value_edu6)
print(edul)#学历


All_avgs= [Edu_Salary(i) for i in edul]  #所有城市平均薪资
One_avgs= [One_City(i,'重庆') for i in edul]    #单个城市平均薪资
Two_avgs= [One_City(i,'北京') for i in edul]
Three_avgs= [One_City(i,'上海') for i in edul]
Four_avgs= [One_City(i,'广州') for i in edul]
Five_avgs= [One_City(i,'深圳') for i in edul]
Six_avgs = [One_City(i,'成都') for i in edul]


from pyecharts import options as opts
from pyecharts.charts import Bar,Line,Page,Scatter

def bar_markline_type() -> Bar:
    c = (
        Bar()
        .add_xaxis(edul)
        .add_yaxis("全国", All_avgs, category_gap="50%")
        .add_yaxis("重庆", One_avgs, category_gap="50%")
        .reversal_axis()
        .set_global_opts(title_opts=opts.TitleOpts(title="Java岗位学历平均薪资"))
        .set_series_opts(
            label_opts=opts.LabelOpts(position="right"),
            markline_opts=opts.MarkLineOpts(
                # data=[
                #     opts.MarkLineItem(type_="min", name="最小值"),
                #     opts.MarkLineItem(type_="max", name="最大值"),
                #     opts.MarkLineItem(type_="average", name="平均值"),
                # ]
            )
        )
    )
    return c

def line_smooth() -> Line:
    c = (
        Line()
        .add_xaxis(edul)
        .add_yaxis("重庆", value_edu1, is_smooth=True)
        .add_yaxis("北京", value_edu2, is_smooth=True)
        .add_yaxis("上海", value_edu3, is_smooth=True)
        .add_yaxis("广州", value_edu4, is_smooth=True)
        .add_yaxis("深圳", value_edu5, is_smooth=True)
        .add_yaxis("成都", value_edu6, is_smooth=True)
        .set_global_opts(title_opts=opts.TitleOpts(title="一线城市招聘数量对比图"))
    )
    return c

def scatter_visualmap_color() -> Scatter:
    c = (
        Scatter()
        .add_xaxis(edul)
        .add_yaxis("重庆", One_avgs)
        .add_yaxis("北京", Two_avgs)
        .add_yaxis("上海", Three_avgs,is_selected=False)
        .add_yaxis("广州", Four_avgs ,is_selected=False)
        .add_yaxis("深圳", Five_avgs ,is_selected=False)
        .add_yaxis("成都", Six_avgs, is_selected=False)
        .set_global_opts(
            title_opts=opts.TitleOpts(title="一线城市平均薪资对比图"),
            visualmap_opts=opts.VisualMapOpts(type_="size", max_=22000, min_=0),
        )
    )
    return c

page = Page()
page.add(bar_markline_type(),line_smooth(),scatter_visualmap_color())
page.render('一线城市学历平均薪资对比图.html')


