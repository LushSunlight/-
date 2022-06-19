def getDicts():
    import gensim
    import os
    import math
    import numpy
    import gensim

    # 注释表明思路

    # 导入清华，搜狗词库以及分词部分结果
    import os
    with open('词性说明.txt') as f:
        content=f.readlines()
        index=0
        attri2index={}
        index2attri=[]
        for i in content:
            attriType=i.split()[0]
            attri2index[attriType]=index
            index2attri.append(attriType)
            index+=1
    filesurl = "Dicts"
    all_files = []
    for root, dirs, files in os.walk(filesurl):
        all_files = files
    all_list, label = [], []
    attribute_list,attribute_label=[],[]
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
                    if kind == 'other':
                        attriLabel=[0 for i in range(17)]
                        attris=x[2].split('\n')[0]
                        wordAttri=attris.split(',')
                        for k in wordAttri:
                            if k in attri2index.keys():
                                attriLabel[attri2index[k]]=1
                        attribute_list.append(x[0])
                        attribute_label.append(attriLabel)

    return all_list,label,attribute_list,attribute_label