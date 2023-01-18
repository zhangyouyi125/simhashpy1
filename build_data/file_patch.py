'''
Author: zyy
Date: 2022-11-12 19:41:18
LastEditTime: 2022-11-17 16:15:25
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
file_patch = "_patch"
# set_nums_repeat = 3
# set_nums_file = 48
set_nums_repeat = 2
set_nums_file = 72
#set_nums_sentence = 8
set_nums_sentence_file = 2
set_nums_sentence = 6
split_str = '。”|。）|[!！。？?]'

def patch_file():
    dirs = os.listdir(dirs_path)
    print(dirs)
    for dir in dirs:
        targetdir = os.path.join(sim_path, dir+"-sim", "patch")
        if not os.path.exists(targetdir):  #判断是否存在文件夹如果不存在则创建为文件夹
            os.makedirs(targetdir)
        print(targetdir)
        print(dir)
        count = 1
        sourcedir = os.path.join(dirs_path, dir)
        files = os.listdir(sourcedir)
        files.sort()

        '''文件拼凑'''
        #一共操作得到 set_nums_file * set_nums_repeat个相似文件对
        # 对 set_nums_file 个文件进行修改操作
        for j in range(set_nums_file):
            # 对文件j进行拼凑操作，一个文件生成 set_nums_repeat 个相似文件
            for i in range(1, set_nums_repeat + 1):
                filename = files[j]
                #文件按照patch编号排序
                filename_delete = filename[:-4] + file_patch + str(i) + fileSuffix
                #存储相似文件对的路径
                sourcepath = os.path.join(sourcedir, filename)
                targetpath = os.path.join(targetdir, filename_delete)
                print(sourcepath ,targetpath)

                # 获取文本中句子个数     
                with open(sourcepath, mode='r', encoding='utf8') as f:
                    file = f.read()
                    #拼凑set_nums_sentence个句子
                    sentence_list = re.split(split_str, file)
                    sentence_total = len(sentence_list)
               
                set_nums_sentence = 6
                set_nums_sentence = max(math.ceil(sentence_total/12), set_nums_sentence)

                # 随机选取其他set_nums_sentence个文件中的句子，进行拼凑
                n = len(files)
                sentence_patch = []
                for k in range(set_nums_file + set_nums_sentence_file*j, set_nums_file + set_nums_sentence_file*(j + 1)):
                    file_path = os.path.join(sourcedir, files[k])
                    with open(file_path, mode='r', encoding='utf8') as f:
                        file_temp = f.read()
                        sentence_list = re.split(split_str, file_temp)
                        sentence_total = len(sentence_list)
                        # if sentence_total < set_nums_sentence:
                        #     slen = len(sentence_patch) + sentence_total
                        # else:
                        slen = len(sentence_patch) + set_nums_sentence
                        while len(sentence_patch) < slen:
                            index = random.randint(1, sentence_total - 1)
                            #print(len(sentence_patch), slen)
                            sentence = sentence_list[index]
                            sentence_patch.append(sentence)
                            
                
                # 将其他文件中的句子，拼凑到file[j]中，得到file内容     
                with open(sourcepath, mode='r', encoding='utf8') as f:
                    file = f.read()
                    #拼凑set_nums_sentence个句子
                    sentence_list = re.split(split_str, file)
                    sentence_total = len(sentence_list)
                    sentence_index = [] #保存待拼凑句子的下标
                    print(sourcepath)

                    # 随机选取set_nums_sentence个句子的下标
                    while (len(sentence_index) < len(sentence_patch)):
                        index = random.randint(1, sentence_total - 1)
                        #print(len(sentence_index),set_nums_sentence_file * set_nums_sentence)
                        if index not in sentence_index:
                            sentence_index.append(index)
                    
                    # 句子拼凑
                    for k in range(len(sentence_index)):
                        sentence_source = sentence_list[sentence_index[k]]
                        sentence_target = sentence_patch[k]
                        file = file.replace(sentence_source, sentence_target, 1)
                    
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
    patch_file()