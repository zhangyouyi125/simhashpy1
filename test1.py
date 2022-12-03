import OpenHowNet
import math
# OpenHowNet.download()
# hownet = OpenHowNet.HowNetDict()
# result_list = hownet_dict.get_sense("苹果")
# print(len(result_list))
# print(result_list[0])
# result_list = hownet['开心']
# print(len(result_list))
# print(result_list[0])
# result_list = hownet['高兴']
# print(len(result_list))
# print(result_list[0])
j = 0
j = max(j, 4)
print(j)

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
set_nums_repeat = 3
set_nums_file = 48
#set_nums_sentence = 2
set_nums_sentence = 6
#set_nums_word = 10
set_nums_word = 25
split_str = '。”|。）|[!！。？?]'

def delete_file():

    print(set_nums_sentence)
                
           
if __name__ == "__main__":
    delete_file()