import os

import gensim


def trainer(all_list,label):
    model_path= 'svm.pickle'
    vector_list=w2v(all_list)
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(vector_list, label, test_size=0.33, random_state=1)
    # 将上述模型运用至分词部分结果得到类别
    if os.path.exists(model_path):
        with open(model_path,'rb') as f:
            import pickle
            svm = pickle.load(f)
    else:
        from sklearn.calibration import CalibratedClassifierCV
        from sklearn.svm import LinearSVC
        clf = LinearSVC()
        svm = CalibratedClassifierCV(clf)
    svm.fit(X_train, y_train)
    svm_y = svm.predict(X_test)
    accuracy_svm = (svm_y == y_test).astype(float).mean()
    print('svm分类准确率为：', accuracy_svm)
    with open(model_path, 'wb') as f:
        import pickle
        pickle.dump(svm, f)

def attriTrainer(attri_list,attri_label):
    model_path="moc.pickle"
    from sklearn.feature_extraction.text import TfidfTransformer
    from sklearn.feature_extraction.text import CountVectorizer
    vector_list=w2v(attri_list)
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(vector_list, attri_label, test_size=0.33, random_state=1)
    from xgboost import XGBClassifier
    from sklearn.model_selection import KFold
    from sklearn.multioutput import MultiOutputClassifier
    from sklearn.pipeline import Pipeline
    if os.path.exists(model_path):
        with open(model_path,'rb') as f:
            import pickle
            clf = pickle.load(f)
    else:
        classifier = MultiOutputClassifier(XGBClassifier())
        clf = Pipeline([('classify', classifier)])
    clf.fit(X_train,y_train)
    svm_y = clf.predict(X_test)
    accuracy_svm = (svm_y == y_test).astype(float).mean()
    print('moc分类准确率为：', accuracy_svm)
    with open(model_path, 'wb') as f:
        import pickle
        pickle.dump(clf, f)
    pass

def tester(all_list):
    model_path = 'svm.pickle'
    vector_list=w2v(all_list)
    # 将上述模型运用至分词部分结果得到类别
    with open(model_path, 'rb') as f:
        import pickle
        svm = pickle.load(f)
    svm_y = svm.predict(vector_list)
    return svm_y

def attriTester(attribute_list):
    model_path = 'moc.pickle'
    vector_list=w2v(attribute_list)
    # 将上述模型运用至分词部分结果得到类别
    with open(model_path, 'rb') as f:
        import pickle
        clf = pickle.load(f)
    moc_y = clf.predict(vector_list)
    return moc_y

def w2v(words):
    print('loading model')
    wv_from_text = gensim.models.KeyedVectors.load_word2vec_format("tencent-ailab-embedding-zh-d100-v0.2.0-s.txt", binary=False)
    print('loading finished')
    vectors=[]
    for word in words:
        try:
            vectors.append(wv_from_text[word])
        except KeyError:
            import random
            vectors.append([random.uniform(-1,1) for i in range(wv_from_text.vector_size)])
    return vectors