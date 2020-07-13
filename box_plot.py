import pandas as pd
from pyecharts import Boxplot
data=pd.read_csv(r"C:\学习\python数据分析\数据\iris-data.csv")
x=list(data.columns[0:4])
y=[list(data.sepal_length_cm),
    list(data.sepal_width_cm),
    list(data.petal_length_cm),
    list(data.petal_width_cm)
]
boxplot=Boxplot("箱线图")
y_data=boxplot.prepare_data(y)
boxplot.add("",x,y_data)
boxplot.render()
