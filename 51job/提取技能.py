#encoding: utf-8
import pandas as pd
import pymongo
import jieba
from pyecharts import options as opts
from pyecharts.charts import Radar
from pyecharts.charts import Page, WordCloud
import re
import random

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


def Skills(City_name):
    Data = get_data[get_data['城市'].str.contains('{}'.format(City_name))]
    print("得到有效数据%s条" % len(Data))
    max = len(Data)
    information = Data['职位信息']
    txtl = jieba.cut(' '.join(information), cut_all=False)#jieba分词
    txt = ' '.join(txtl).replace('\n', ' ').lower()

    # for i in '!"#$%&()*+, ，、：。-./:;<=>?@[\\]^_‘{|}~':
    #     Txtx = txt.replace(i, "")  # 将文本中特殊字符替换为空格

    china = re.sub('[0-9a-zA-Z_]','', txt)#保留汉字
    text = re.sub('[\u4e00-\u9fa5]', '', txt)#去除汉字
    for i in '!"#$%&()*+, （）【】，；0．！、：。-./:;<=>?@[\\]^_‘{|}~':
        china = china.replace(i, " ")  # 将文本中特殊字符替换为空格
        text = text.replace(i,' ')
    print("请稍等，正在生成")

    Idioms = china.split()
    Icounts = {}
    for Idiom in Idioms:
        if len(Idiom) < 2:#过滤掉单个字
            continue
        else:
            Icounts[Idiom] = Icounts.get(Idiom, 0) + 1
    Idiom = {'工作','相关','以及','能力','使用','以上','职能','类别','要求','具有',
             '进行','产品','任职','具备','关键','关键字','岗位','资格','内容','参与','编写','以上学历','公司','岗位职责'}
    for i in Idiom:
        try:
            del (Icounts[i])
        except:
            continue
    chinas = list(Icounts.items())
    chinas.sort(key=lambda x: x[1], reverse=True)
    # for i in range(50):
    #     china, counts = chinas[i]
    #     print("{0:<5}->{1:>5}".format(china, counts))


    words = text.split()  # 对字符串进行分割，获得单词列表
    counts = {}
    for word in words:
        if len(word) < 2:  # 过滤掉单个字母
            continue
        else:
            counts[word] = counts.get(word, 0) + 1
    word = {'and', 'the', 'with', 'in', 'by',  'for', 'of', 'an', 'to'}#排除特定的单词
    for i in word:
        try:
            del (counts[i])
        except:
            continue
    #生成元组列表，并进行降序排列
    items = list(counts.items())
    items.sort(key=lambda x: x[1], reverse=True)

    for i in range(20):
        word, count = items[i]
        print("{0:<5}->{1:>5}".format(word, count))

    return items, max, chinas


def radar_selected_mode() -> Radar:
    DaLuan = list[1:10]
    print(list[:10])
    random.shuffle(DaLuan)
    print(DaLuan)
    c = (
        Radar()
        .add_schema(textstyle_opts={'color':'#c7a252',"fontSize": 16,},#文字样式的颜色
            schema=[
                opts.RadarIndicatorItem(name=list[0][0], max_=max),
                opts.RadarIndicatorItem(name=DaLuan[0][0], max_=max),
                opts.RadarIndicatorItem(name=DaLuan[1][0], max_=max ),
                opts.RadarIndicatorItem(name=DaLuan[2][0], max_=max ),
                opts.RadarIndicatorItem(name=DaLuan[3][0], max_=max),
                opts.RadarIndicatorItem(name=DaLuan[4][0], max_=max),
                opts.RadarIndicatorItem(name=DaLuan[5][0], max_=max),
                opts.RadarIndicatorItem(name=DaLuan[6][0], max_=max),
                opts.RadarIndicatorItem(name=DaLuan[7][0], max_=max),
                opts.RadarIndicatorItem(name=DaLuan[8][0], max_=max),
            ],
        )
        .add("Top10能力要求", [[max]+[DaLuan[i][1] for i in range(0,9)]],
             areastyle_opts={"color": '#009ad6'},linestyle_opts={"color": '#009ad6'})
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(
            legend_opts=opts.LegendOpts(selected_mode="single"),
            title_opts=opts.TitleOpts(title="岗位技能雷达图"),
        )
    )
    return c

def wordcloud_base() -> WordCloud:
    c = (
        WordCloud()
        .add("", chinas[:100], word_size_range=[20, 100])
        .set_global_opts(title_opts=opts.TitleOpts(title="岗位要求"))
    )
    return c


list, max, chinas = Skills('重庆')
page = Page()
page.add(wordcloud_base(),radar_selected_mode())
page.render('专业技能雷达图.html')



