# -*- coding: utf-8 -*-

import jieba
import os

stpwrdpath = "stop_words.txt"
stpwrd_dic = open(stpwrdpath, 'rb')
stpwrd_content = stpwrd_dic.read()
stpwrd_decode = stpwrd_content.decode('GBK')
stpwrdlst = stpwrd_decode.splitlines()
stpwrd_dic.close()


origin_text_dir = './origin_text/'
cut_text_dir = './cut_text/'

w2v_base = None


def word_cut():
    origin_text_files = os.listdir(origin_text_dir)
    # print(origin_text_dir+origin_text_files[1])

    for file in origin_text_files:
        with open(origin_text_dir + file, encoding='UTF-8') as f:
            document = f.read()
            # document = document.decode('utf-8')
            document_cut = jieba.cut(document)
            result = ' '.join(document_cut)
            result = result.encode('utf-8')

            with open(cut_text_dir + file, 'wb+') as c_f:
                c_f.write(result)


def word_to_vec():
    from sklearn.feature_extraction.text import TfidfVectorizer

    cut_text_files = os.listdir(cut_text_dir)
    # print(cut_text_files)

    corpus = []

    for file in cut_text_files:
        with open(cut_text_dir + file, encoding='UTF-8') as f:
            document = f.read()
            corpus.append(document)

    vector = TfidfVectorizer(stop_words=stpwrdlst)

    tfidf = vector.fit_transform(corpus)

    #print(tfidf)

    wordlist = vector.get_feature_names()
    weightlist = tfidf.toarray()

    #print(">>>wordlist  %d" % len(wordlist))

    #print(">>>weightlist  %d" % len(weightlist))

    #for i in range(10):
        #print(u"-----第", i+1 , u"段文本的词语tf-idf权重------")
        #for j in range(10):
            #print(wordlist[j+10000], weightlist[i][j+10000])

    return(cut_text_files, wordlist, weightlist)


def search_by_word(keyWord, w2v_base=None):
    word_index = w2v_base.wordlist.index(keyWord)
    file_index = -1
    max = 0

    for i in range(len(w2v_base.weightlist)):
        if w2v_base.weightlist[i][word_index] > max:
            max = w2v_base.weightlist[i][word_index]
            file_index = i

    return w2v_base.files[file_index]


def search_by_words(keywords):
    global w2v_base
    kw_list = jieba.cut(keywords.replace(' ', ''))

    kw_indexs = []
    file_indexs = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    file_rank = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    for keyword in kw_list:
        try:
            kw_indexs.append(w2v_base.wordlist.index(keyword))
        except ValueError as e:
            print(">>>>>关键词在库中未找到: " + ''.join(e.args))

    for i in range(len(w2v_base.weightlist)):
        rank = 0

        for kw_index in kw_indexs:
            rank += w2v_base.weightlist[i][kw_index]

        min_file_rank_index = file_rank.index(min(file_rank))

        if rank > file_rank[min_file_rank_index]:
            file_rank[min_file_rank_index] = rank
            file_indexs[min_file_rank_index] = i

    temp_results = {}
    results = {}
    text_titles = []

    for i in range(10):
        temp_results[w2v_base.files[file_indexs[i]]] = file_rank[i]

    for text in sorted(temp_results, key=temp_results.get, reverse=True):
        results[text[:4]] = temp_results[text]
        text_titles.append(get_text_title(text))

    print(results)
    print(text_titles)
    return results, text_titles, keywords


def get_text_title(file):
    with open('./origin_text/' + file, encoding='UTF-8') as f:
        title = f.readline()
        return title


class W2VBase:
    def __init__(self, files, wordlist, weightlist):
        self.files = files
        self.wordlist = wordlist
        self.weightlist = weightlist


def __init__():

    global w2v_base
    if not w2v_base:
        files, wordlist, weightlist = word_to_vec()
        w2v_base = W2VBase(files, wordlist, weightlist)



