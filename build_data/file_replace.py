'''
Author: zyy
Date: 2022-11-10 22:39:09
LastEditTime: 2022-11-17 11:10:57
Description: 
'''
import os
from chardet import detect
import csv
import random
import jieba
import re
import synonyms

fileSuffix = '.txt'
dirs_path = "./build_data/dataset"
sim_path = "./build_data/dataset-sim"
label_path = "./build_data/labels"
stop_words_path = "./data/stopwords_sum.txt"
file_replace = "_replace"
set_nums_repeat = 2
set_nums_file = 72
#set_nums_word = 30
set_nums_word = 40

def replace_file():
    dirs = os.listdir(dirs_path)
    print(dirs)
    for dir in dirs:
        targetdir = os.path.join(sim_path, dir+"-sim", "replace")
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
            # 对 set_nums_file 个文件进行同义词替换操作
            if count > set_nums_file:
                break
            count+=1
            # 对每个文件进行同义词替换，一个文件生成 set_nums_repeat 个相似文件
            for i in range(1, set_nums_repeat + 1):  
                #同义词替换的文件按照replace编号排序
                filename_replace = filename[:-4] + file_replace + str(i) + fileSuffix
                #存储相似文件对的路径
                sourcepath = os.path.join(sourcedir, filename)
                targetpath = os.path.join(targetdir, filename_replace)
                print(sourcepath ,targetpath)

                '''替换同义词'''
                #随机选取20个词语
                with open(sourcepath, mode='r', encoding='utf8') as f:
                    file = f.read()
                    #分词，获取词语list
                    stopword_set = [line.strip() for line in open(stop_words_path, 'r', encoding='utf-8').readlines()]
                    word_list = jieba.cut(file, cut_all=False)
                    word_list = [token for token in word_list if token.strip() != u'' and not token in stopword_set]
                    word_total = len(word_list)

                    #随机选取词语，并进行同义词替换
                    word_index = []
                    while (len(word_index) < set_nums_word):
                        index = random.randint(0, word_total - 1)
                        if index not in word_index:
                            synonym = synonyms.nearby(word_list[index])
                            synonym_words = synonym[0]
                            if len(synonym_words) <= 2:  #同义词不存在
                                continue
                            else:
                                word_replace = synonym_words[1]
                                #print(word_list[index], word_replace,len(word_index))
                                file = file.replace(word_list[index], word_replace, 1)
                                word_index.append(index)

                '''文件保存'''
                #另存同义词替换后的文件
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
    replace_file()