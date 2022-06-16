import gensim
import os
import math
import numpy

# 注释表明思路

# 导入清华，搜狗词库以及分词部分结果
import os

filesurl = "classify"
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

# 将清华，搜狗词库的向量提取出来训练一个SVM，其中存在于搜狗而不存在于清华的看作其他类
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer

vec = CountVectorizer()  # 使用前必须实例化！！！
tf = TfidfTransformer()
x = []
X = vec.fit_transform(all_list)
TFIDF = tf.fit_transform(X)  # 文本语料转化为词向量矩阵
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(TFIDF, label, test_size=0.33, random_state=1)
# 将上述模型运用至分词部分结果得到类别
from sklearn.calibration import CalibratedClassifierCV
from sklearn.svm import LinearSVC

svm_distortions = []
clf = LinearSVC()
svm = CalibratedClassifierCV(clf)
classifier = svm.fit(X_train, y_train)
svm_y = svm.predict(X_test)
accuracy_svm = (svm_y == y_test).astype(float).mean()
print('svm分类准确率为：', accuracy_svm)
svm_distortions.append(accuracy_svm)

import pickle

with open('svm.pickle', 'wb') as f:
    pickle.dump(svm, f)
