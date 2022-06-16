import os
def trainer(all_list,label):
    model_path='svm.pickle'
    from sklearn.feature_extraction.text import TfidfTransformer
    from sklearn.feature_extraction.text import CountVectorizer

    vec = CountVectorizer()  # 使用前必须实例化！！！
    tf = TfidfTransformer()
    X = vec.fit_transform(all_list)
    TFIDF = tf.fit_transform(X)  # 文本语料转化为词向量矩阵
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(TFIDF, label, test_size=0.33, random_state=1)
    # 将上述模型运用至分词部分结果得到类别
    svm_distortions = []
    if os.path.exists(model_path):
        with open(model_path,'rb') as f:
            import pickle
            svm = pickle.load(f)
    else:
        from sklearn.calibration import CalibratedClassifierCV
        from sklearn.svm import LinearSVC
        clf = LinearSVC()
        svm = CalibratedClassifierCV(clf)
    classifier = svm.fit(X_train, y_train)
    svm_y = svm.predict(X_test)
    accuracy_svm = (svm_y == y_test).astype(float).mean()
    print('svm分类准确率为：', accuracy_svm)
    svm_distortions.append(accuracy_svm)
    with open(model_path, 'wb') as f:
        import pickle
        pickle.dump(clf, f)
