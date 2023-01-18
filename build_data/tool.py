'''
Author: zyy
Date: 2022-11-16 10:08:27
LastEditTime: 2022-11-16 10:35:51
Description: 
'''
import os
from chardet import detect
import csv
import re
import random

fileSuffix = '.txt'
dirs_path = "./build_data/dataset/C19-Computer"
#set_nums_file = 720 # 30*24
set_nums_file = 360 # 30*24
set_repeat = 2

label_path = "./build_data/labels"
dissim_path = "./build_data/dataset-dissim"
file_dissim = "_dissim"
set_nums_sentence = 10
split_str = '。”|。）|[!！。？?]'

def dissim_file():

    files = os.listdir(dirs_path)
    files.sort()
    print(dir, len(files))

    '''不相似文件对'''
    #一共操作得到 set_nums_file * set_nums_repeat个相似文件对
    for file in files:
        fp = os.path.join(dirs_path,file)

        with open(fp, mode='r', encoding='utf8') as f:
            file = f.read()
            print(file)
            file, sep, tail = file.partition("参考文献")
            #print(file, sep, tail)
            f.write(file)
        with open(fp, mode='w', encoding='utf8') as f:
            f.write(file)



if __name__ == "__main__":
    dissim_file()