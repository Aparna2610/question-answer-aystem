# -*- coding: utf-8 -*-
"""
Created on Fri Feb  9 21:15:21 2018

@author: Aparna Gangwar
"""
# Importing libraries
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter
import math

class processData:
    
#   __init__: Initialization method
#       Assign stop_words from nltk.corpus.stopwords
#       Assign idf from the object passed from main method      
#       returns null
    def __init__(self, mainObj):
        self.idf = mainObj.idf
        self.stop_words = set(stopwords.words('english'))
        return

#   findTfVector: The method to find the term frequency vector 
#       Tokenize the paragraph passed as text
#       Filter the stop words and stem the tokens
#       Remove the punctuations and empty tokens
#       Calculate the term frequencies for words in text
#       returns the term freq vector, tf
    def findTfVector(self, text):
        self.text = text
        self.tf = []
        temp = []
        tokenized = [x.lower() for x in word_tokenize(self.text)]
        filtered = [w for w in tokenized if not w in self.stop_words]
        for word in filtered:
            temp.append(PorterStemmer().stem(word))        
        temp = [x for x in temp if x not in ('(', ')', ',', ';', '?', '!', '.', ' ' )]
        self.tf = dict(Counter(temp))
        return self.tf
       
#   queryVector: The method to find the query vector
#       Tokenize the question query
#       Filter the stop words, blank and punctuation tokens
#       Stem the tokens list
#       Count the frequencies of tokens in query vector and return
#       returns the query vector, qv
    def queryVector(self, question):
         self.question = question 
         self.qv = {}
         temp = []
         tokenized = [x.lower() for x in word_tokenize(self.question)]
         filtered = [w for w in tokenized if not w in self.stop_words]
         for word in filtered:
            temp.append(PorterStemmer().stem(word))
         terms = [x for x in temp if x not in ('(', ')', ',', ';', '?', '!', '.', ' ' )]
         self.qv = dict(Counter(terms))
         return self.qv
         
#   findSim: The method to find the similarity 
#       between query vector(qv), idf vector and the vector that conains the tf's
#       of the words in the paras, ie, sv
#       returns tf-idf similarity coefficient
    def findSim(self, qv, sv, idf):
        sim = []
        dr1 = 0
        for word in qv:
                if word in idf:
                    dr1 += math.pow((idf[word]*qv[word]),2)
        
        dr2 = 0
        for word in sv:
            dr2 += math.pow((idf[word]*sv[word]),2)
        
        numr = 0
        for word in qv.keys():
            if word in idf and word in sv:
                numr += qv[word]*sv[word]*idf[word]*idf[word]
        if math.sqrt(dr1)*math.sqrt(dr2) != 0:
            sim = numr/math.sqrt(dr1)*math.sqrt(dr2)
        
        return sim

