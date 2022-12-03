'''
Author: zyy
Date: 2022-11-13 18:32:10
LastEditTime: 2022-11-17 16:21:51
Description: 
'''
import os
from chardet import detect
import csv
import random
import jieba
import re
import synonyms
import math

sentence_temp = "*******************sentence_exchange_temp*******************"
fileSuffix = '.txt'
dirs_path = "./build_data/dataset"
sim_path = "./build_data/dataset-sim"
label_path = "./build_data/labels"
stop_words_path = "./data/stopwords_sum.txt"
file_synthesize = "_synthesize"
split_str = '。”|。）|[!！。？?]'
set_nums_repeat = 2
set_nums_file = 72
set_delete_sentence = 5
set_delete_word = 20
set_replace_word = 20
set_patch_sentence = 5
set_exchange_sentence = 8
# set_delete_sentence = 1
# set_delete_word = 10
# set_replace_word = 10
# set_patch_sentence = 3
# set_exchange_sentence = 5


def synthesize_file():
    dirs = os.listdir(dirs_path)
    print(dirs)
    for dir in dirs:
        targetdir = os.path.join(sim_path, dir+"-sim", "synthesize")
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
        for j in range(set_nums_file):
            # 对 set_nums_file 个文件进行综合操作
            filename = files[j]
            # 对每个文件进行综合操作，一个文件生成 set_nums_repeat 个相似文件
            for i in range(1, set_nums_repeat + 1):  
                #综合操作的文件按照synthesize编号排序
                filename_replace = filename[:-4] + file_synthesize + str(i) + fileSuffix
                #存储相似文件对的路径
                sourcepath = os.path.join(sourcedir, filename)
                targetpath = os.path.join(targetdir, filename_replace)
                print(sourcepath ,targetpath)
                #先读取文件内容
                with open(sourcepath, mode='r', encoding='utf8') as f:
                    file = f.read()

                '''综合操作'''
                # '词语增删： set_delete_sentence个句子、set_delete_word个词语'
                # 删除句子
                sentence_list = re.split(split_str, file)
                sentence_total = len(sentence_list)
                # 随机选取句子的下标
                set_delete_sentence = 5
                set_delete_sentence = max(math.ceil(sentence_total/10), set_delete_sentence)
                sentence_delete = []
                while len(sentence_delete) < set_delete_sentence:
                    index = random.randint(1, sentence_total - 1)
                    if index not in sentence_delete:
                            sentence_delete.append(index)
                # 删除句子
                for i in range (0, len(sentence_delete)):
                    file = file.replace(sentence_list[sentence_delete[i]],'',1)

                # 删除词语
                # 分词，获取词语list
                stopword_set = [line.strip() for line in open(stop_words_path, 'r', encoding='utf-8').readlines()]
                word_list = jieba.cut(file, cut_all=False)
                word_list = [token for token in word_list if token.strip() != u'' and not token in stopword_set]
                word_total = len(word_list)
                #随机选取词语
                word_index = []
                while (len(word_index) < set_delete_word):
                    index = random.randint(0, word_total - 1)
                    if index not in word_index:
                        word_index.append(index)
                #删除词语
                for i in range (0, len(word_index)):
                    file = file.replace(word_list[word_index[i]],'',1)

                '文本拼凑 patch'
                # 将其他文件中的句子，拼凑到file[j]中，得到file内容     
                # 拼凑set_nums_sentence个句子
                sentence_list = re.split(split_str, file)
                sentence_total = len(sentence_list)

                set_patch_sentence = 5
                set_patch_sentence = max(math.ceil(sentence_total/11), set_patch_sentence)

                # 从其他文件中选取句子
                sentence_patch = []
                # for k in range(set_nums_file + set_patch_sentence*j, set_nums_file + set_patch_sentence*(j + 1)):
                
                k = set_nums_file + j * set_nums_repeat + i - 1
                file_path = os.path.join(sourcedir, files[k])
                with open(file_path, mode='r', encoding='utf8') as f:
                    file_temp = f.read()
                    sentence_list = re.split(split_str, file_temp)
                    sentence_total = len(sentence_list)
                    while (len(sentence_patch) < set_patch_sentence):
                        index = random.randint(1, sentence_total - 1)
                        sentence = sentence_list[index]
                        sentence_patch.append(sentence)

                # 随机选取set_nums_sentence个句子的下标
                sentence_list = re.split(split_str, file)
                sentence_total = len(sentence_list)
                sentence_index = [] #保存待拼凑句子的下标
                
                while (len(sentence_index) < set_patch_sentence):
                    index = random.randint(1, sentence_total - 1)
                    if index not in sentence_index:
                        sentence_index.append(index)
                # 句子拼凑
                for k in range(len(sentence_index)):
                    sentence_source = sentence_list[sentence_index[k]]
                    sentence_target = sentence_patch[k]
                    file = file.replace(sentence_source, sentence_target, 1)
                
                '同义词替换: set_replace_word个词语'
                #随机选取set_replace_word个词语  
                #分词，获取词语list
                stopword_set = [line.strip() for line in open(stop_words_path, 'r', encoding='utf-8').readlines()]
                word_list = jieba.cut(file, cut_all=False)
                word_list = [token for token in word_list if token.strip() != u'' and not token in stopword_set]
                word_total = len(word_list)

                #随机选取词语，并进行同义词替换
                word_index = []
                while (len(word_index) < set_replace_word):
                    index = random.randint(0, word_total - 1)
                    if index not in word_index:
                        synonym = synonyms.nearby(word_list[index])
                        synonym_words = synonym[0]
                        if len(synonym_words) <= 2:  #同义词不存在
                            continue
                        else:
                            word_replace = synonym_words[1]
                            file = file.replace(word_list[index], word_replace, 1)
                            word_index.append(index)
                '句子顺序交换'
                # 交换set_exchange_sentence个句子顺序
                # 分局
                sentence_list = re.split(split_str, file)
                sentence_total = len(sentence_list)
                sentence_index = [] #保存待交换两个句子的下标
                #随机选取两个句子的下标
                #while (len(sentence_index) < set_nums_sentence):
                for i in range(set_exchange_sentence):
                    index1 = random.randint(1, sentence_total - 1)
                    index2 = random.randint(1, sentence_total - 1)
                    while index1 == index2:
                        index2 = random.randint(1, sentence_total - 1)
                    #句子交换
                    sentence1 = sentence_list[index1]
                    sentence2 = sentence_list[index2]
                    file = file.replace(sentence1, sentence_temp, 1)
                    file = file.replace(sentence2, sentence1, 1)
                    file = file.replace(sentence_temp, sentence2, 1)

                '''文件保存'''
                #另存综合操作后的文件
                with open(targetpath, mode='w', encoding='utf8') as w:
                    w.write(file)
                #将相似文件对的路径和label记录在对应csv文件中
                filecsv = os.path.join(label_path, dir +".csv")
                print(filecsv)
                with open(filecsv, mode='a+', encoding='utf8') as f:
                    csv_write = csv.writer(f)
                    data_row = [sourcepath, targetpath, 1]
                    csv_write.writerow(data_row)
           
if __name__ == "__main__":
    synthesize_file()