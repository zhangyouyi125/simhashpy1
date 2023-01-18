'''
Author: zyy
Date: 2022-11-11 16:22:43
LastEditTime: 2022-11-17 11:10:44
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
file_exchange = "_exchange"
set_nums_repeat = 2
set_nums_file = 48
#set_nums_sentence = 10
set_nums_sentence = 20
split_str = '。”|。）|[!！。？?]'
sentence_temp = "*******************sentence_exchange_temp*******************"

def exchange_file():
    dirs = os.listdir(dirs_path)
    print(dirs)
    for dir in dirs:
        targetdir = os.path.join(sim_path, dir+"-sim", "exchange")
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
            # 对 set_nums_file 个文件进行修改操作
            if count > set_nums_file:
                break
            count+=1
            # 对每个文件进行交换操作，一个文件生成 set_nums_repeat 个相似文件
            for i in range(1, set_nums_repeat + 1):
                #文件按照exchange编号排序
                filename_delete = filename[:-4] + file_exchange + str(i) + fileSuffix
                #存储相似文件对的路径
                sourcepath = os.path.join(sourcedir, filename)
                targetpath = os.path.join(targetdir, filename_delete)
                print(sourcepath ,targetpath)
                #随机交换文件中句子的顺序，交换set_nums_sentence次，得到file内容
                with open(sourcepath, mode='r', encoding='utf8') as f:
                    file = f.read()
                    '''交换句子'''
                    sentence_list = re.split(split_str, file)
                    sentence_total = len(sentence_list)
                    sentence_index = [] #保存待交换两个句子的下标
                    set_nums_sentence = 20
                    set_nums_sentence = max(math.ceil(sentence_total/3), set_nums_sentence)
                    #随机选取两个句子的下标
                    #while (len(sentence_index) < set_nums_sentence):
                    for i in range(set_nums_sentence):
                        index1 = random.randint(1, sentence_total - 1)
                        index2 = random.randint(1, sentence_total - 1)
                        while index1 == index2:
                            index2 = random.randint(1, sentence_total - 1)
                        # if index not in sentence_index:
                        #     sentence_index.append(index)
                        #句子交换
                        sentence1 = sentence_list[index1]
                        sentence2 = sentence_list[index2]
                        file = file.replace(sentence1, sentence_temp, 1)
                        file = file.replace(sentence2, sentence1, 1)
                        file = file.replace(sentence_temp, sentence2, 1)
            
                '''文件保存'''
                #另存句子交换后的文件
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
    exchange_file()