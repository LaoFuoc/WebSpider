#encoding: utf-8
import pandas as pd
import pymongo
from pyecharts import options as opts
from pyecharts.charts import Bar, Line, Page ,Pie


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

work = ['3-4年经验', '无工作经验', '5-7年经验', '2年经验', '1年经验', '8-9年经验', '10年以上经验']
workyear = ['无工作经验','1年经验','2年经验','3-4年经验','5-7年经验','8-9年经验','10年以上经验']

def Get_Photo(City_name):

    Data = get_data[get_data['城市'].str.contains('{}'.format(City_name))]
    print("得到有效数据%s条" % len(Data))
    """计算不同工作经验对应的平均薪资"""
    def Work_Salary(Work_name):

        work_salas = Data[Data['工作经验'].str.contains('{}'.format(Work_name))]
        sums = [sala for sala in work_salas['平均薪资'] if type(sala) == int]  # 工资列表
        try:
            avg = int(sum(sums) / int(len(sums)))
        except:
            avg = 0

        return avg

    All_avgs = [Work_Salary(i) for i in workyear]
    print('平均薪资', All_avgs)

    # 工作经验部分,排序处理
    def workyear_ChuLi(Data):
        value_workyear = []
        for i in workyear:
            try:
                value_workyear.append(int(Data[i]))
            except:
                value_workyear.append(0)
        return value_workyear

    # 统计工作经验对应得岗位数量
    Data1 = Data['工作经验'].value_counts()
    value_workyear1 = workyear_ChuLi(Data1)
    print(workyear)
    print(value_workyear1)

    """工作经验文本饼图"""

    def pie_rich_label() -> Pie:
        c = (
            Pie()
                .add(
                "",
                [list(z) for z in zip(workyear, value_workyear1)],
                radius=["40%", "55%"],
                label_opts=opts.LabelOpts(
                    position="outside",
                    formatter="{a|{a}}{abg|}\n{hr|}\n {b|{b}: }{c}  {per|{d}%}  ",
                    background_color="#eee",
                    border_color="#aaa",
                    border_width=1,
                    border_radius=4,
                    rich={
                        "a": {"color": "#999", "lineHeight": 22, "align": "center"},
                        "abg": {
                            "backgroundColor": "#e3e3e3",
                            "width": "100%",
                            "align": "right",
                            "height": 22,
                            "borderRadius": [4, 4, 0, 0],
                        },
                        "hr": {
                            "borderColor": "#aaa",
                            "width": "100%",
                            "borderWidth": 0.5,
                            "height": 0,
                        },
                        "b": {"fontSize": 16, "lineHeight": 33},
                        "per": {
                            "color": "#eee",
                            "backgroundColor": "#334455",
                            "padding": [2, 4],
                            "borderRadius": 2,
                        },
                    },
                ),
            )
                .set_global_opts(title_opts=opts.TitleOpts(title="{}Java岗位-工作经验需求占比".format(City_name), pos_left='center'),
                                 legend_opts=opts.LegendOpts(
                                     orient="vertical", pos_top="5%", pos_left="1%")
                                 )
        )
        return c

    def overlap_bar_line() -> Bar:
        bar = (
            Bar()
                .add_xaxis(workyear)
                .add_yaxis("岗位数量", value_workyear1, category_gap="50%")
                .extend_axis(
                yaxis=opts.AxisOpts(
                    axislabel_opts=opts.LabelOpts(formatter="{value} /月"), interval=5000
                )
            )
                .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
                .set_global_opts(
                title_opts=opts.TitleOpts(title="{}岗位数量-平均薪资对比图".format(City_name)),
                yaxis_opts=opts.AxisOpts(
                    axislabel_opts=opts.LabelOpts(formatter="{value} 个")
                ),
            )
        )

        line = Line().add_xaxis(workyear).add_yaxis("平均薪资", All_avgs, yaxis_index=1, is_smooth=True) \
            .set_global_opts(title_opts=opts.TitleOpts(title="Line-smooth"))

        bar.overlap(line)
        return bar

    page = Page()
    page.add(pie_rich_label(), overlap_bar_line())
    page.render('{}经验-薪资对比图.html'.format(City_name))


"""输入单个城市，如果想要全国，则不输入"""

name = input("输入单个城市(如果想要全国，则不输入)：")
Get_Photo(name)





