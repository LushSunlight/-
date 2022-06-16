import gensim
import os
import math
import numpy

# 注释表明思路

# 导入清华，搜狗词库以及分词部分结果
import os

filesurl = "Dicts"
all_files = []
for root, dirs, files in os.walk(filesurl):
    all_files = files
all_list, label = [], []
for i in all_files:
    name = i.split('_')
    if len(name) == 1:
        code = 'gbk'
    else:
        code = 'utf-8'
    with open(filesurl + '/' + i, encoding=code, errors='ignore') as f:
        content = f.readlines()
        if len(name) == 1:
            kind = 'other'
        else:
            kind = name[1].split('.')[0]
        for i in content:
            if i == '\n':
                break
            x = i.split('\t')
            num = int(math.log2(1 + int(x[1])))
            for j in range(num):
                all_list.append(x[0])
                label.append(kind)

from trainer import trainer
trainer(all_list,label)