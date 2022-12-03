'''
Author: zyy
Date: 2022-11-01 10:06:39
LastEditTime: 2022-11-16 11:37:39
Description:
'''
#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@brief: get tokens from input file by jieba
'''
from decimal import Decimal
import jieba
import jieba.analyse
import jieba.posseg as pseg
import os
import sys

class JiebaTokenizer:
    def __init__(self, stop_words_path, mode='s'):
        self.stopword_set = set()
        # load stopwords
        self.stopword_set = [line.strip() for line in open(stop_words_path, 'r', encoding='utf-8').readlines()]
        self.mode = mode
        self.word_list = []
        self.words = {}

    # 分词+计算权重，词频
    def tokens(self, intext):
        intext = u' '.join(intext.split())
        word_list = jieba.cut(intext, cut_all=False)
        word_list = [token for token in word_list if token.strip() != u'' and not token in self.stopword_set]
        return word_list

    def weight(self, word_list):
        words = {}
        for word in word_list:
            words[word] = words.get(word, 0) + 1
        return words

    # 分词+计算权重，TF-IDF
    def tokens_tfidf(self, input):
        input = u' '.join(input.split())
        word_list = jieba.analyse.extract_tags(input, topK=21474836473, withWeight=True, allowPOS=())
        word_list = [list(token) for token in word_list if not token[0] in self.stopword_set]
        words = {}
        for i in range(len(word_list)):
            words[word_list[i][0]] = word_list[i][1]
        return words
    
    # 分词+计算权重，TF-IDF + 词性 + 词语长度
    def tokens_sp(self, input):
        input = u' '.join(input.split())
        #word_list = jieba.analyse.extract_tags(input, topK=10000, withWeight=True, allowPOS=())
        word_list = jieba.cut(input, cut_all=False)
        word_list = [list(token) for token in word_list if not token[0] in self.stopword_set]
        # 词性
        pos_weight = {'n': 0.4, 'v': 0.3, 'a': 0.2}
        word_pos = {}
        tags = pseg.cut(input)
        for word, tag in tags:
            word_pos[word] = tag

        # 词语长度
        len_weight = {4: 0.24, 5: 0.24, 3: 0.16, 6: 0.16, 2: 0.07, 7: 0.07}

        #综合权重计算，tf-idf * (1 + len + pos)
        for i, word in enumerate(word_list):
            # 计算词语长度权重
            word_len = len(word[0])
            word_len_weight = len_weight.get(word_len, 0)
            # 计算词性权重
            if word[0] in word_pos: #判断该词语的词性是否存在
                if word_pos[word[0]] in pos_weight: #判断词性
                    word_pos_weight = pos_weight[word_pos[word[0]]]
                else:
                    word_pos_weight = 0.1
            else:
                word_pos_weight = 0.1
            weight = word_list[i][1] * (1 + float(Decimal(str(word_len_weight))) + float(Decimal(str(word_pos_weight))))
            word_list[i].append(weight)
            word_list[i][1] = weight
        
        words = {}
        for i in range(len(word_list)):
            words[word_list[i][0]] = word_list[i][1]
        return words


    def tokens_sp2(self, input):
        input = u' '.join(input.split())
        word_list = jieba.cut(input, cut_all=False)
        word_list = [token for token in word_list if token.strip() != u'' and not token in self.stopword_set]
        # 词性
        pos_weight = {'n': 0.4, 'v': 0.3, 'a': 0.2}
        word_pos = {}
        tags = pseg.cut(input)
        for word, tag in tags:
            word_pos[word] = tag

        # 词语长度
        len_weight = {4: 0.24, 5: 0.24, 3: 0.16, 6: 0.16, 2: 0.07, 7: 0.07}

        #综合权重计算，tf-idf * (1 + len + pos)
        for i, word in enumerate(word_list):
            # 计算词语长度权重
            word_len = len(word[0])
            word_len_weight = len_weight.get(word_len, 0)
            # 计算词性权重
            if word[0] in word_pos: #判断该词语的词性是否存在
                if word_pos[word[0]] in pos_weight: #判断词性
                    word_pos_weight = pos_weight[word_pos[word[0]]]
                else:
                    word_pos_weight = 0.1
            else:
                word_pos_weight = 0.1
            words = self.weight(word_list)
            weight = words[word] * (1 + float(Decimal(str(word_len_weight))) + float(Decimal(str(word_pos_weight))))
            words[word] = weight
        
        # words = {}
        # for i in range(len(word_list)):
        #     words[word_list[i][0]] = word_list[i][1]
        return words

def token_single_file(input_fname, output_fname):
    result_lines = []
    with open(input_fname) as ins:
        for line in ins:
            line = line.strip().decode('utf8')
            tokens = jt.tokens(line)
            result_lines.append(u' '.join(tokens).encode('utf8'))
    open(output_fname, 'w').write(os.linesep.join(result_lines))
    print ('Wrote to ', output_fname)


if __name__ == "__main__":
    if len(sys.argv) < 6 or sys.argv[1] not in ['-s', '-m'] or sys.argv[4] not in ['c', 's']:
        print ("Usage:\ttokens.py <file_mode(-s/-m)> <input_file/input_folder> " \
              "<output_file/output_folder> <cut_mode(c/s)> <stopword.list>")
        print ("file_mode:\t-s:\tsingle file")
        print ("\t\t-m:\tmultiple files")
        print ("cut_mode:\tc:\tnormal mode of Jieba")
        print ("\t\ts:\tcut_for_search mode of Jieba")
        exit(-1)
    file_mode, input_filepath, output_filepath, cut_mode, stopword_file = sys.argv[1:]
    jt = JiebaTokenizer(stopword_file, cut_mode)
    # extract tokens and filter by stopwords
    if file_mode == '-s':
        token_single_file(input_filepath, output_filepath)
    elif file_mode == '-m':
        for input_file in os.listdir(input_filepath):
            prefix = input_file.rsplit(os.sep, 1)[0]
            token_single_file(os.path.join(input_filepath, input_file),
                              os.path.join(output_filepath, prefix+'.token'))
