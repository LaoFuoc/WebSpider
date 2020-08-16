#encoding: utf-8
import pandas as pd
import pymongo
import jieba
from wordcloud import WordCloud
from matplotlib import pyplot as plt
import re
import random

client = pymongo.MongoClient()  # 链接pymongo数据库
collection = client['51Job']['Java12_1']
print("数据表名称：",collection.name)
data = collection.find()
df = pd.DataFrame(data)  # 读取整张表 (DataFrame)
print("包含数据%s条"%len(df))
del df['_id']#删除id列
df.drop_duplicates(['职位链接'],inplace = True)#去重，保留唯一值,inplace = True
print("去重之后剩余%s条信息"%len(df))
get_data = df[df['工作岗位'].str.contains('java' ,case=False)]

print("得到有效数据%s条"%len(get_data))

information = get_data['职位信息']
information.to_csv('test.txt', encoding = 'utf-8-sig',index=False)

def fenCi():

    f = open("test.txt",'r',encoding='utf-8')
    f1 = open("seg.txt",'w',encoding='utf-8')
    line = f.readline()
    while line:
        line = line.strip(' ')
        words =" ".join(jieba.cut(line))
        words = words.replace("，","").replace("！","").replace("“","")\
            .replace("”","").replace("。","").replace("？","").replace("：","")\
            .replace("...","").replace("、","").strip(' ')
        if words.startswith('-') or words == '\r\n' or words.startswith('.') or len(words)<10 :
            line = f.readline()
            continue
        words = words.strip('\n')
        f1.writelines(words)
        line = f.readline()

fenCi()

def get_txt():
    txt = open("seg.txt", "r", encoding='UTF-8').read()
    txt = txt.lower()
    for ch in '!"#$%&()*+,-./:;<=>?@[\\]^_‘{|}~':
        txt = txt.replace(ch, "")      # 将文本中特殊字符替换为空格
    text = re.sub('[\u4e00-\u9fa5]', '', txt)
    text = re.sub('0', '', text)

    return text

def yingwen():
    file_txt = get_txt()
    print(type(file_txt))
    words = file_txt.split()    # 对字符串进行分割，获得单词列表
    counts = {}
    for word in words:
        if len(word) < 2:
            continue
        else:
            counts[word] = counts.get(word, 0) + 1
    word = {'and', 'the', 'with', 'in', 'by', 'its', 'for', 'of', 'an', 'to'}#排除特定的单词
    for i in word:
        del (counts[i])
    #生成元组列表，并进行降序排列
    items = list(counts.items())
    items.sort(key=lambda x: x[1], reverse=True)

    for i in range(20):
        word, count = items[i]
        print("{0:<5}->{1:>5}".format(word, count))

    print(items[:40])
yingwen()