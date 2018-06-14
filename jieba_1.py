#-*- coding: utf-8 -*-

#引入结巴分词
import jieba


#加入词汇
# jieba.suggest_freq('沙瑞金', True)
# jieba.suggest_freq('易学习', True)
# jieba.suggest_freq('王大路', True)
# jieba.suggest_freq('京州', True)

#从文件导入停用词表
stpwrdpath = "stop_words.txt"
stpwrd_dic = open(stpwrdpath, 'rb')
stpwrd_content = stpwrd_dic.read()
stpwrd_decode = stpwrd_content.decode('GBK')
#将停用词表转换为list
stpwrdlst = stpwrd_decode.splitlines()
stpwrd_dic.close()


#中文分词
def word_cut():
    with open('./nlp_test_a.txt') as f:
        document = f.read()

        document_decode = document.decode('utf-8')
        document_cut = jieba.cut(document)

        result = ' '.join(document_cut)
        result = result.encode('utf-8')

        

        with open('./nlp_test_r1.txt', 'w') as f1:
            f1.write(result)

    f.close()
    f1.close()


    with open('./nlp_test_b.txt') as f:
        document = f.read()

        document_decode = document.decode('utf-8')
        document_cut = jieba.cut(document)

        result = ' '.join(document_cut)
        result = result.encode('utf-8')

        

        with open('./nlp_test_r2.txt', 'w') as f1:
            f1.write(result)

    f.close()
    f1.close()


#向量化-使用TF-IDF和标准化
def word_to_vec():
    from sklearn.feature_extraction.text import TfidfVectorizer

    with open('./nlp_test_r1.txt') as f1:
        res1 = f1.read()

    with open('./nlp_test_r2.txt') as f2:
        res2 = f2.read()

    corpus = [res1, res2]
    vector = TfidfVectorizer(stop_words=stpwrdlst)

    tfidf = vector.fit_transform(corpus)

    #输出向量
    print(tfidf)

    #获取词袋模型中的所有词
    wordlist = vector.get_feature_names()
    #tf-idf矩阵，元素a[i][j]表示j词在i类文本中的tf-idf权重
    weightlist = tfidf.toarray()

    #打印每类文本的tf-idf词语权重，第一个for便利所有文本，第二个for遍历某一类文本下的词语权重
    for i in range(len(weightlist)):
        print(u"-----第", i+1 , u"段文本的词语tf-idf权重------")
        for j in range(len(wordlist)):
            print(wordlist[j], weightlist[i][j])


if __name__ == "__main__":
    word_cut()
    word_to_vec()