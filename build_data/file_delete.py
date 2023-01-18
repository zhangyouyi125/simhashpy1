'''
Author: zyy
Date: 2022-11-09 11:47:51
LastEditTime: 2022-11-17 11:10:31
Description: 
'''

import os
from chardet import detect
import csv
import random
import jieba
import re
import math

fileSuffix = '.txt'
dirs_path = "./build_data/dataset"
sim_path = "./build_data/dataset-sim"
label_path = "./build_data/labels"
stop_words_path = "./data/stopwords_sum.txt"
fileadd = "_add"
file_delete = "_delete"
# set_nums_repeat = 3
# set_nums_file = 48
set_nums_repeat = 2
set_nums_file = 72
#set_nums_sentence = 2
set_nums_sentence = 6
#set_nums_word = 10
set_nums_word = 25
split_str = '。”|。）|[!！。？?]'

def delete_file():
    dirs = os.listdir(dirs_path)
    print(dirs)
    for dir in dirs:
        targetdir = os.path.join(sim_path, dir+"-sim", "delete")
        if not os.path.exists(targetdir):  #判断是否存在文件夹如果不存在则创建为文件夹
            os.makedirs(targetdir)
        print(targetdir)
        print(dir)
        count = 1
        sourcedir = os.path.join(dirs_path, dir)
        files = os.listdir(sourcedir)
        files.sort()

        '''文件修改'''
        #一共操作得到 set_nums_file * set_nums_repeat个相似文件对
        for filename in files:
            # 对 set_nums_file 个文件进行增删操作
            if count > set_nums_file:
                break
            count+=1
            set_nums_sentence = 6
            # 对每个文件进行增删操作，一个文件生成 set_nums_repeat 个相似文件
            for i in range(1, set_nums_repeat + 1):
                #文件按照delete编号排序
                filename_delete = filename[:-4] + file_delete + str(i) + fileSuffix
                #存储相似文件对的路径
                sourcepath = os.path.join(sourcedir, filename)
                targetpath = os.path.join(targetdir, filename_delete)
                print(sourcepath ,targetpath)
                #随机删除句子和词语，得到file内容
                with open(sourcepath, mode='r', encoding='utf8') as f:
                    file = f.read()
                    '''删除两个句子'''
                    sentence_list = re.split(split_str, file)
                    sentence_total = len(sentence_list)
                    sentence_index = [] #保存待删除句子下标
                    #随机选取句子的下标
                    # num = set_nums_sentence
                    set_nums_sentence = max(set_nums_sentence,math.ceil(sentence_total/6))
                    while (len(sentence_index) < set_nums_sentence):
                        index = random.randint(1, sentence_total - 1)
                        if index not in sentence_index:
                            sentence_index.append(index)
                    #删除句子
                    for i in range (0, len(sentence_index)):
                        #print(sentence_list[sentence_index[i]])
                        #file = re.sub(sentence_list[sentence_index[i]],'',file, 1)
                        file = file.replace(sentence_list[sentence_index[i]],'',1)

                    '''删除词语'''
                    #分词，获取词语list
                    stopword_set = [line.strip() for line in open(stop_words_path, 'r', encoding='utf-8').readlines()]
                    word_list = jieba.cut(file, cut_all=False)
                    word_list = [token for token in word_list if token.strip() != u'' and not token in stopword_set]
                    word_total = len(word_list)
                    #随机选取词语
                    word_index = []
                    while (len(word_index) < set_nums_word):
                        index = random.randint(0, word_total - 1)
                        if index not in word_index:
                            word_index.append(index)
                    #删除词语
                    for i in range (0, len(word_index)):
                        #file = re.sub(word_list[word_index[i]],'',file, 1)
                        file = file.replace(word_list[word_index[i]],'',1)

                '''文件保存'''
                #另存增删后的文件
                with open(targetpath, mode='w', encoding='utf8') as w:
                    w.write(file)
                #将相似文件对的路径和label记录在对应csv文件中
                filecsv = os.path.join(label_path, dir +".csv")
                print(filecsv)
                with open(filecsv, mode='a+', encoding='utf8') as f:
                    csv_write = csv.writer(f)
                    #data_row = [file, filename_delete, 1]
                    data_row = [sourcepath, targetpath, 1]
                    csv_write.writerow(data_row)
           
if __name__ == "__main__":
    delete_file()