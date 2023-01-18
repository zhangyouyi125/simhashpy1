'''
Author: zyy
Date: 2022-11-14 14:12:03
LastEditTime: 2022-11-18 13:21:17
Description: 
'''

import os
from decimal import Decimal
from chardet import detect
from numpy import *
import csv
import sys 
import time
sys.path.append('src/')
import similar5
from simhash1 import SimhashBuilder

label_path = "./build_data/labels"
stop_words_path = "./data/stopwords_sum.txt"
threshold = 3
result_path = "./lab/lab5/result"

def lab5():
    dir = os.listdir(label_path)
    print(dir)
    accuracy_avg = []
    precision_avg = []
    recall_avg = []
    F1_avg = []
    # 初始化sim
    sim = SimhashBuilder()
    if not os.path.exists(result_path):  #判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(result_path)
    # 全部结果写入地址，包括每一类的和平均的
    res_all_path = os.path.join(result_path, "res_all.csv")
    with open(res_all_path, 'w', encoding='utf8') as fa:
        res_write = csv.writer(fa)
        res_write.writerow(["Category", "Accuracy", "Recall", "F1-Score", "Precision", "Time"])
    time_all = 0
    for filename in dir:
        file_path = os.path.join(label_path, filename)
        print(file_path)
        # 保存结果
        if not os.path.exists(result_path):  #判断是否存在文件夹如果不存在则创建为文件夹
            os.makedirs(result_path)
        res_csv_path = os.path.join(result_path, filename)
        f = open(res_csv_path, 'w', encoding='utf8')
        res_csv_write = csv.writer(f)
        # 对label中的相似对和不相似对文本进行simhash计算
        total = 0
        TP = 1
        FP = 1
        TN = 1
        FN = 1
        time_start = time.time()
        with open(file_path, 'r', encoding='utf8') as f:
            reader = csv.reader(f)
            for row_data in reader:
                file1 = row_data[0]
                file2 = row_data[1]
                sim_sample = int(row_data[2])
                res_dist, res_sim = similar5.similar_simhash(file1, file2, stop_words_path, 0.8, sim)
                if res_dist > threshold:
                    sim_exp = 0
                else:
                    sim_exp = 1
                data_row = [file1, file2, sim_sample, sim_exp]
                res_csv_write.writerow(data_row)
                # 结果为相似（正）
                if sim_exp == 1: 
                    if sim_sample == 1: 
                        TP += 1    # 样本为正
                    else: 
                        FP += 1    # 样本为负
                # 结果为不相似（负）
                else:
                    if sim_sample == 0: 
                        TN += 1
                    else:
                        FN += 1
                total += 1

        time_end = time.time()
        time_use = time_end - time_start
        time_all += time_use
        accuracy =  (TP + TN )/( TP + FP + TN + FN)
        precision = TP / (TP + FP)
        recall = TP / (TP + FN)
        F1 = 2 * precision * recall / (precision + recall)
        accuracy_avg.append(accuracy)
        precision_avg.append(precision)
        recall_avg.append(recall)
        F1_avg.append(F1)
        res_path = os.path.join(result_path, filename[:-4] + "_res.csv")
        # 写入准确率、精确率、召回率、F1的结果
        with open(res_path, 'w', encoding='utf8') as fs:
            res_write = csv.writer(fs)
            res_write.writerow(["total", total])
            res_write.writerow(["TP", TP])
            res_write.writerow(["FP", FP])
            res_write.writerow(["TN", TN])
            res_write.writerow(["FN", FN])
            res_write.writerow(["accuracy", accuracy])
            res_write.writerow(["precision", precision])
            res_write.writerow(["recall", recall])
            res_write.writerow(["F1-Score", F1])
            res_write.writerow(["time", time_use])

        # 每一类的结果写入res_all_path地址
        # ["Category", "Accuracy", "Recall", "F1-Score", "Precision"]
        with open(res_all_path, 'a+', encoding='utf8') as fa:
            res_write = csv.writer(fa)
            res_write.writerow([filename[:-4], accuracy, recall, F1, precision, time_use])
            
    # 平均值结果写入res_all_path地址
    with open(res_all_path, 'a+', encoding='utf8') as fa:
        res_write = csv.writer(fa)
        res_write.writerow(["Avg_score", mean(accuracy_avg), mean(recall_avg), mean(F1_avg), mean(precision_avg), time_all])
        # res_avg_write.writerow(["accuracy_avg", mean(accuracy_avg)])
        # res_avg_write.writerow(["precision_avg", mean(precision_avg)])
        # res_avg_write.writerow(["recall_avg", mean(recall_avg)])
        # res_avg_write.writerow(["F1_avg", mean(F1_avg)])


if __name__ == "__main__":
    lab5()
