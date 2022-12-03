'''
Author: zyy
Date: 2022-11-14 13:29:06
LastEditTime: 2022-11-17 11:10:38
Description: 
'''

import os
from chardet import detect
import csv
import re
import random
import math

fileSuffix = '.txt'
dirs_path = "./build_data/dataset"
#set_nums_file = 720 # 30*24
set_nums_file = 360 # 30*24
set_repeat = 2

label_path = "./build_data/labels"
dissim_path = "./build_data/dataset-dissim"
file_dissim = "_dissim"
set_nums_sentence = 10
split_str = '。”|。）|[!！。？?]'

def dissim_file():
    if not os.path.exists(label_path):  #判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(label_path)
    dirs = os.listdir(dirs_path)
    print(dirs)
    for dir in dirs:
        targetdir = os.path.join(dissim_path, dir)
        if not os.path.exists(targetdir):  #判断是否存在文件夹如果不存在则创建为文件夹
            os.makedirs(targetdir)
        sourcedir = os.path.join(dirs_path, dir)
        files = os.listdir(sourcedir)
        files.sort()
        print(dir, len(files))

        '''不相似文件对'''
        #一共操作得到 set_nums_file * set_nums_repeat个相似文件对
        for i in range(set_nums_file):
            n = len(files)
            if i >= n - 1:
                p = i - n
                k = p + 2
            else:
                p = i
                k = p + 1
            for q in range(k, k + set_repeat):
                set_nums_sentence = 10
                filename1 = files[p]
                filename2 = files[q]
                file_path1 = os.path.join(dirs_path, dir, filename1)
                file_path2 = os.path.join(dirs_path, dir, filename2)
                print(file_path1, file_path2)

                filename_dissim = filename2[:-4] + file_dissim + str(q - k + 1) + fileSuffix
                target_path = os.path.join(dissim_path, dir, filename_dissim)

                 # 句子数量
                with open(file_path2, mode='r', encoding='utf8') as f:
                    file = f.read()
                    sentence_list = re.split(split_str, file)
                    sentence_total = len(sentence_list)
                    set_nums_sentence = 10
                    set_nums_sentence = max(set_nums_sentence, math.ceil(sentence_total/5) )
                    set_nums_sentence = min(set_nums_sentence, math.floor(sentence_total / 2) - 1)

                # 构建不相似文件对
                with open(file_path1, mode='r', encoding='utf8') as f:
                    file = f.read()
                    sentence_list = re.split(split_str, file)
                    sentence_total = len(sentence_list)
                    # if sentence_total <= set_nums_sentence * 2:
                    #     set_nums_sentence = math.floor(sentence_total / 2) - 1
                    # print(set_nums_sentence, sentence_total)
                    sentences1 = []
                    #随机选取句子的下标，用于替换目标文件中的句子
                    while (len(sentences1) < set_nums_sentence):
                        index = random.randint(1, sentence_total - 1)
                        sentence = sentence_list[index]
                        # if sentence not in sentences1:
                        sentences1.append(sentence)
                # 将句子填入另一文件中
                with open(file_path2, mode='r', encoding='utf8') as f:
                    file = f.read()
                    sentence_list = re.split(split_str, file)
                    sentence_total = len(sentence_list)
                    # set_nums_sentence = 10
                    # set_nums_sentence = max(set_nums_sentence, math.ceil(sentence_total / 2) - 1)
                    sentences2 = []
                    #随机选取句子的下标
                    while (len(sentences2) < set_nums_sentence):
                        index = random.randint(1, sentence_total - 1)
                        #print(len(sentences2),set_nums_sentence )
                        sentence = sentence_list[index]
                        # print(len(sentences2),set_nums_sentence, sentence_total)
                        if sentence not in sentences2:
                            sentences2.append(sentence)
                            
                for i in range(len(sentences2)):
                    file = file.replace(sentences2[i], sentences1[i], 1)
                # 文件保存
                with open(target_path, mode='w', encoding='utf8') as w:
                    w.write(file)
                    
                # 将不相似文件对的路径和label记录在对应csv文件中
                filecsv = os.path.join(label_path, dir +".csv")
                print(filecsv)
                with open(filecsv, mode='a+', encoding='utf8') as f:
                    csv_write = csv.writer(f)
                    data_row = [file_path1, target_path, 0]
                    csv_write.writerow(data_row)

if __name__ == "__main__":
    dissim_file()