import gensim

import numpy

# 注释表明思路

# 导入清华，搜狗词库以及分词部分结果
import os
filesurl="classify"
all_files=[]
for root, dirs, files in os.walk(filesurl):
    all_files=files
dic = {}
for i in all_files:
    name = i.split('_')
    if len(name)==1:
        code = 'gbk'
    else:
        code = 'utf-8'
    with open(filesurl+'/'+i,encoding=code,errors='ignore') as f:
        content = f.readlines()
        if len(name)==1:
            for i in content:
                x=i.split('\t')
                dic[x[0]]=None
        else:
            kind=name[1].split('.')[0]
            for i in content:
                x=i.split('\t')
                dic[x[0]]=kind

# 将两者分别用gensim转化为向量
a=0
# 将清华，搜狗词库的向量提取出来训练一个kNN分类，其中存在于搜狗而不存在于清华的看作其他类

# 将上述模型运用至分词部分结果得到类别

# 保存结果