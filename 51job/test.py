#encoding: utf-8
from pyecharts import options as opts
from pyecharts.charts import Radar
import random


list = [('java', 892), ('spring', 436), ('mysql', 320), ('oracle', 235), ('mybatis', 233), ('sql', 219), ('linux', 173), ('web', 164), ('redis', 156), ('j2ee', 137), ('jquery', 134), ('springmvc', 127), ('hibernate', 125), ('javascript', 108), ('tomcat', 107), ('html', 94), ('css', 89), ('mvc', 88), ('springboot', 87), ('ajax', 83), ('boot', 75), ('dubbo', 73), ('cloud', 68), ('springcloud', 62), ('git', 60), ('mongodb', 60), ('io', 60), ('jsp', 58), ('jvm', 57), ('js', 57), ('maven', 56), ('eclipse', 53), ('nginx', 53), ('weblogic', 49), ('struts', 48), ('kafka', 46), ('svn', 45), ('server', 43), ('vue', 41), ('zookeeper', 39)]

DaLuan = list[:10]
print(DaLuan)
random.shuffle(DaLuan)

print(DaLuan)