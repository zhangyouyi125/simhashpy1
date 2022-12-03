'''
Author: zyy
Date: 2022-11-18 09:07:08
LastEditTime: 2022-11-29 11:28:06
Description: 
'''
#!/usr/bin/env python
# -*-coding:utf8-*-
import os, sys
from decimal import Decimal
#from gensim.models import Word2Vec
from gensim import models
from gensim.models import Word2Vec

import fnv
import time



def hamming_distance(hash_a, hash_b, hashbits=128):
    x = (hash_a ^ hash_b) & ((1 << hashbits) - 1)
    tot = 0
    while x:
        tot += 1
        x &= x-1
    return tot

class SimhashBuilder:
    def __init__(self, words={}, hashsize=64):
        self.words = words
        self.hashsize = hashsize
        self.model = models.KeyedVectors.load_word2vec_format('data/news_12g_baidubaike_20g_novel_90g_embedding_64.bin',binary=True)
        # self.hashval_list = [self.vectorize(word) for word in words]
        # print ('Totally: %s words' %(len(self.hashval_list),))
        """
        with open('word_hash.txt', 'w') as outs:
            for word in word_list:
                outs.write(word+'\t'+str(self._string_hash(word))+os.linesep)
        """
    def vectorize(self, words):
        finger_vec = [0]*self.hashsize 
        #获取分词hash和权重 
        features = self._getFeatures(words)
        #加权合并
        for hash , weight in features.items():
            for i in range(0, self.hashsize):
                bitmask = 1<<i
                if bitmask&hash != 0:
                    finger_vec[i] += Decimal(str(weight))
                else:
                    finger_vec[i] -= Decimal(str(weight))
        # 计算文档的fingerprint     
        fingerprint = 0
        for i in range(self.hashsize):
            if finger_vec[i] >= 0:
                fingerprint += 1 << i
        print(fingerprint)
        return fingerprint
        
    def _getFeatures(self, words):
        features = {}
        for word, weight in words.items():
            hash = self._hash(word)
            features[hash] = weight
        return features

    def _hash(self, word):
        # word to hash
        if word == "":
            return 0
        else:
            hash = fnv.hash(bytes(word, encoding = "utf8"), algorithm=fnv.fnv_1a, bits=64)
        return hash
    
    # Word2Vec
    def vectorize_w2v(self, words):
        finger_vec = [0]*self.hashsize 
        #获取分词hash和权重 
        # self._hash_w2v()
        finger_vec = self._getFeatures_w2v(words)
        # 计算文档的fingerprint     
        fingerprint = 0
        for i in range(self.hashsize):
            if finger_vec[i] >= 0:
                fingerprint += 1 << i
        print(fingerprint)
        return fingerprint
        
    def _getFeatures_w2v(self, words):
        features = []
        #model = models.KeyedVectors.load_word2vec_format('data/news_12g_baidubaike_20g_novel_90g_embedding_64.bin',binary=True)
        finger_vec = [0]*self.hashsize
        for word, weight in words.items():
            #hash
            if word == "":
                hash = [0]*self.hashsize 
            else:
                if word in self.model:
                    hash = self.model[word]
                else:
                    hash = self._hash(word)
                    for i in range(0, self.hashsize):
                        bitmask = 1<<i
                        if bitmask&hash != 0:
                            finger_vec[i] += Decimal(str(weight))
                        else:
                            finger_vec[i] -= Decimal(str(weight))
                    continue
            for i in range(len(hash)):
                if hash[i] > 0:
                    finger_vec[i] += Decimal(str(weight))
                else:
                    finger_vec[i] -= Decimal(str(weight))
        return finger_vec
        
    def _hash_w2v(self):
        start = time.time()
        #model=models.Word2Vec.load('data/news.model')

        start = time.time()
        #model=models.Word2Vec.load('data/news.model')

        model=models.KeyedVectors.load_word2vec_format('data/news_12g_baidubaike_20g_novel_90g_embedding_64.bin',binary=True)
        if "卡辛" in model:
            print("yes")
        else:
            print("no")
        end = time.time()                
        print ("time0**********",end-start)
        start = time.time()
        s1 = model['开心']
        end = time.time()
        print ("time1**********",end-start)
        start = time.time()
        s2 = model['高兴']
        end = time.time()
        print ("time2**********",end-start)
        print(s1, s2)
        # res = []
        # for i in range(0, 64):
        #     if s1[i] > 0  and s2[i] > 0:
        #         res.append(0)
        #     elif s1[i] < 0 and s2[i] < 0:
        #         res.append(0)
        #     else:
        #         res.append(1)
        # print(res)
        # end = time.time()
        # print (end-start)

    def hamming_distance(self, other_hash):
        x = (self.hash ^ other_hash.hash) & ((1 << self.hashsize) - 1)
        tot = 0
        while x:
            tot += 1
            x &= x-1
        return tot

    def similarity(self, other_hash):
        a = float(self.hash)
        b = float(other_hash)
        if a>b: return b/a
        return a/b


if __name__ == '__main__':
    #看看哪些东西google最看重？标点？
    #s = '看看哪些东西google最看重？标点？'
    #hash1 =simhash(s.split())
    #print("0x%x" % hash1)
    #print ("%s\t0x%x" % (s, hash1))

    #s = '看看哪些东西google最看重！标点！'
    #hash2 = simhash(s.split())
    #print ("%s\t[simhash = 0x%x]" % (s, hash2))

    #print '%f%% percent similarity on hash' %(100*(hash1.similarity(hash2)))
    #print hash1.hamming_distance(hash2),"bits differ out of", hash1.hashbits

    if len(sys.argv) < 4:
        print ("Usage:\tsimhash_imp.py <word_dict_path> <feature_file> <finger_print_file>")
        exit(-1)
    word_list = []
    with open(sys.argv[1], 'r') as ins:
        for idx, line in enumerate(ins.readlines()):
            word_list.append(line.split()[1])
            print ('\rloading word', idx,
    sim_b = SimhashBuilder(word_list))
    result_lines = []
    print ('')
    with open(sys.argv[2], 'r') as ins:
        for idx, line in enumerate(ins.readlines()):
            print ('\rprocessing doc', idx,
            feature_vec = line.strip().split())
            feature_vec = [(int(item.split(':')[0]),float(item.split(':')[1])) for item in feature_vec]
            fingerprint = sim_b.sim_hash_nonzero(feature_vec)
            result_lines.append(str(fingerprint)+os.linesep)
    with open(sys.argv[3], 'w') as outs:
        outs.writelines(result_lines)



