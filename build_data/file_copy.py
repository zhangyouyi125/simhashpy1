'''
Author: zyy
Date: 2022-11-09 11:47:51
LastEditTime: 2022-11-17 16:22:40
Description: 
'''

import os
from chardet import detect
import csv

fileSuffix = '.txt'
dirs_path = "./build_data/dataset"
sim_path = "./build_data/dataset-sim"
file_copy = "_copy"
set_nums_repeat = 1
set_nums_file = 24
label_path = "./build_data/labels"

def copy_file():
    dirs = os.listdir(dirs_path)
    print(dirs)
    for dir in dirs:
        targetdir = os.path.join(sim_path, dir+"-sim", "copy")
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
            # 对 set_nums_file 个文件进行复制操作
            if count > set_nums_file:
                break
            count+=1
            # 对每个文件进行复制操作，一个文件生成 set_nums_repeat 个相似文件
            for i in range(1, set_nums_repeat + 1):
                #复制的文件按照copy编号排序
                filename_copy = filename[:-4] + file_copy + str(i) + fileSuffix
                #存储相似文件对的路径
                sourcepath = os.path.join(sourcedir, filename)
                targetpath = os.path.join(targetdir, filename_copy)
                print(sourcepath ,targetpath)
                #复制文件
                copycommand = "cp " + sourcepath + " " + targetpath
                os.popen(copycommand)
                #将相似文件对的路径和label记录在对应csv文件中
                filecsv = os.path.join(label_path, dir +".csv")
                print(filecsv)
                with open(filecsv, mode='a+', encoding='utf8') as f:
                    csv_write = csv.writer(f)
                    #data_row = [file, filename_copy, 1]
                    data_row = [sourcepath, targetpath, 1]
                    csv_write.writerow(data_row)


if __name__ == "__main__":
    copy_file()
    # s = "cp ./build_data/copy.py ./build_data/2.txt.py"
    # os.popen(s)