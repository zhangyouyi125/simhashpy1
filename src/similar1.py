'''
Author: zyy
Date: 2022-11-14 14:44:57
LastEditTime: 2022-12-01 16:17:01
Description: 
'''
#!/usr/bin/env python
# -*-coding:utf8-*-

import sys
from hamming import hamming_distance, similarity
from simhash import SimhashBuilder
from tokens import JiebaTokenizer
from features import FeatureBuilder
from Utils import norm_vector_nonzero, cosine_distance_nonzero


def similar_simhash(file_path_1, file_path_2, stopword_path, threshold):
    with open(file_path_1) as ins:
        doc_data_1 = ins.read().encode('utf8').decode('utf8')
        print ('Loaded', file_path_1)
    with open(file_path_2) as ins:
        doc_data_2 = ins.read().encode('utf8').decode('utf8')
        print ('Loaded', file_path_2)
     # Init tokenizer
    jt = JiebaTokenizer(stopword_path)

    # Tokenization & weight base
    doc_token_1 = jt.tokens(doc_data_1)
    doc_token_2 = jt.tokens(doc_data_2)

    doc_words_1 = jt.weight(doc_token_1)
    doc_words_2 = jt.weight(doc_token_2)

    print ('computing hash')
    # hash
    sim = SimhashBuilder()
    fingerprint_1 = sim.vectorize(doc_words_1)
    fingerprint_2 = sim.vectorize(doc_words_2)
    # Load word list from word_dict
    
    print ('Matching by Simhash + hamming distance')
    dist = hamming_distance(fingerprint_1, fingerprint_2)
    print("hamming distance: ", dist)
    sim = similarity(fingerprint_1, fingerprint_2)
    if sim > float(threshold):
        print ('Matching Result:\t<True:%s>' % sim)
    else:
        print ('Matching Result:\t<False:%s>' % sim)
    return dist, sim

# data/temp/C11-Space1076.txt data/temp/C11-Space1076copy.txt data/stopwords_sum.txt 0.8
if __name__ == "__main__":
    if len(sys.argv) < 5:
        print ("Usage:\tisSimilar.py <doc1> <doc2> <stopword_path> <threshold>")
        exit(-1)
    doc_path_1, doc_path_2, stopword_path, threshold = sys.argv[1:]
    print ('Arguments:', sys.argv[1:])
    with open(doc_path_1) as ins:
        doc_data_1 = ins.read().encode('utf8').decode('utf8')
        print ('Loaded', doc_path_1)
    with open(doc_path_2) as ins:
        doc_data_2 = ins.read().encode('utf8').decode('utf8')
        print ('Loaded', doc_path_2)

    # Init tokenizer
    jt = JiebaTokenizer(stopword_path, 'c')

    # Tokenization & weight base
    # doc_token_1 = jt.tokens(doc_data_1)
    # doc_token_2 = jt.tokens(doc_data_2)

    # doc_words_1 = jt.weight(doc_token_1)
    # doc_words_2 = jt.weight(doc_token_2)
   
    # Tokenization & weight 词频
    doc_token_1 = jt.tokens(doc_data_1)
    doc_token_2 = jt.tokens(doc_data_2)

    doc_words_1 = jt.weight(doc_token_1)
    doc_words_2 = jt.weight(doc_token_2)

    print ('computing hash')
    # hash
    sim = SimhashBuilder()
    fingerprint_1 = sim.vectorize(doc_words_1)
    fingerprint_2 = sim.vectorize(doc_words_2)
    # Load word list from word_dict
    
    print ('Matching by Simhash + hamming distance')
    dist = hamming_distance(fingerprint_1, fingerprint_2)
    print("hamming distance: ", dist)
    sim = similarity(fingerprint_1, fingerprint_2)
    if sim > float(threshold):
        print ('Matching Result:\t<True:%s>' % sim)
    else:
        print ('Matching Result:\t<False:%s>' % sim)