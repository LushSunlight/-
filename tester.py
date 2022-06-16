def tester(all_list, result_path):
    model_path = 'svm.pickle'
    from sklearn.feature_extraction.text import TfidfTransformer
    from sklearn.feature_extraction.text import CountVectorizer

    vec = CountVectorizer()  # 使用前必须实例化！！！
    tf = TfidfTransformer()
    X = vec.fit_transform(all_list)
    TFIDF = tf.fit_transform(X)  # 文本语料转化为词向量矩阵
    # 将上述模型运用至分词部分结果得到类别
    with open(model_path, 'rb') as f:
        import pickle
        svm = pickle.load(f)
    svm_y = svm.predict(TFIDF)
    with open(result_path, 'w', errors='ignore') as f:
        for i in range(len(svm_y)):
            f.writelines([all_list[i],svm_y[i]])
