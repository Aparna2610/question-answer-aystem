# -*- coding: utf-8 -*-
"""
Created on Sat Feb 10 17:22:52 2018

@author: Aparna Gangwar
"""
# Importing libraries
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.tag import pos_tag
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.chunk import ne_chunk
from nltk.tree import Tree
from collections import Counter

import TemporalValGetter as de
import math
import operator 

class Answer:
    
# Valid question_types: ["what" => THING, "why" => DESCRIPTION, "where" => GPE, "when" => TIME, "who" => PERSON]
    
#   __init__: Initialization method
#       Intializes answer attr to empty string
#       Intializes stop words from nltk.corpus.stop_words
#       returns null
    def __init__(self):
        self.answer = ""
        self.stop_words = set(stopwords.words('english'))
        return

#   getAnswer: Method to get the answer based on question_type
#       For a "PERSON" or "LOCATION" type question, call getPersonOrPlaceAnswers()
#       For a "TIME" type question, call getTemporalAnswer()
#       For any other question type, return std answer string
#        returns answer 
    def getAnswer(self, mainObj):
        if mainObj.question_type == "PERSON" or mainObj.question_type == "GPE":
            self.getPersonOrPlaceAnswers(mainObj)
        elif mainObj.question_type == "TIME":
            self.getTemporalAnswer(mainObj)
        elif mainObj.question_type == "SUMMARY":
            self.getSummary(mainObj)
        else:
            self.answer = "Question type not supported. Do you have any other question ?"
        if self.answer == "":
            self.answer = "Could not find the answer to your query.. DO you have any another question"
        return self.answer

#   getTemporalAnswer: Method to find answers to queries of type TIME
#       Finds the relevance of paragraphs using tf-idf
#       Extracts dates from ith most relevant paragraph until it finds a date
#       returns date  
    def getTemporalAnswer(self, mainObj):
        corrIndex = 0
        itr = 0
        while self.answer == "" and corrIndex < len(mainObj.sim) and itr < 4:
            currentPara = mainObj.paras[mainObj.sim[corrIndex][0]]
            simCoeff = self.getSentQueryCorrelation(mainObj.question, mainObj.qv, currentPara)
            sentences = sent_tokenize(currentPara)
            answers = []
            for iSimilarSent in simCoeff:
                sent = sentences[iSimilarSent[0]]
                dates = de.extractDate(sent)
                if len(dates) > 0:
                    self.answer = dates[0]
                    return self.answer
            itr+=1
        return self.answer
   
#   getSummary: Method to retrieve the summarized answer to "how", "what" or "why" question types
#       finds the sentence relevance using tf-idf correlation in ith most relevant paragraph
#       returns the most relevant sentence
    def getSummary(self, mainObj):
        corrIndex = 0
        while self.answer == "" and corrIndex < len(mainObj.sim[:3]):
            currentPara = mainObj.paras[mainObj.sim[corrIndex][0]]
            simCoeff = self.getSentQueryCorrelation(mainObj.question, mainObj.qv, currentPara)
            sentences = sent_tokenize(currentPara)
            for iSimilarSent in simCoeff:
                self.answer = sentences[iSimilarSent[0]]
                return
            corrIndex += 1
        return self.answer
        
#   getPersonOrPlaceAnswers: Method to get the answers to question types PERSON and LOCATION
#       The system tries to find the answer in an iterative fashion, going from most relevant 
#       para to the least. Loop until an answer is found or all the relevant paras have been searched.
#       Find the ith most relevant para
#       Get the tf-idf correlation between all the sentences and the qv
#       For the ith similar sentence, tokenize it, pos_tag it and chunk it based on named-entity recognition.
#       Parse chunked tree returned by ne_chunk()
#       Find the first LOCATION/PERSON tag in the chunked obj
#       returns answer       
    def getPersonOrPlaceAnswers(self, mainObj):
        corrIndex = 0
        itr = 0
        while self.answer == "" and corrIndex < len(mainObj.sim) and itr < 4:
            currentPara = mainObj.paras[mainObj.sim[corrIndex][0]]
            simCoeff = self.getSentQueryCorrelation(mainObj.question, mainObj.qv, currentPara)
            sentences = sent_tokenize(currentPara)
            answers = []
            for iSimilarSent in simCoeff:
                sent = sentences[iSimilarSent[0]]
                taggedSent = pos_tag(word_tokenize(sent))
                chunked = ne_chunk(taggedSent)
                temp = {}
                for chunk in chunked:
                    if type(chunk) == Tree:
                        temp[chunk.label()] = [c[0] for c in chunk]
                answers.append(temp)
            for entity in answers:
                if mainObj.question_type in entity.keys():
                    tAnswer = entity[mainObj.question_type][0]
                    if PorterStemmer().stem(tAnswer.lower()) not in mainObj.qv.keys():
                        self.answer = tAnswer
                        break
            corrIndex+=1
            itr += 1
        return self.answer
            
#   getSentQueryCorrelation: Method to find correlation between sentences and query
#       find the sv and idf vectors by calling findSentVector
#       find similarity coeff between sv and qv
#       returns similarity
    def getSentQueryCorrelation(self, ques, qv, text):
        sv, idf = self.findSentVector(text)
        return self.findSim(sv, qv, idf)
        
#   findSentVector: Method to find the sent vector for all the sentences in the para
#       Tokenize sentences from para
#       Find word tokens from sentence
#       Remove stop words
#       Filter the empty and punctuation tokens
#       TODO: Filter the tokens that are not words
#       Find tf for all terms in sentence
#       Find idf of all words in text
#       returns sv and idf for text
    def findSentVector(self, text):
        sent_tokenize_list = sent_tokenize(text)
        words = []
        sv = []
        ps = PorterStemmer()
        
        for sent in sent_tokenize_list:
            temp = []
            tokenized = word_tokenize(sent)
            filtered = [w for w in tokenized if not w in self.stop_words]
            
            for word in filtered:
                temp.append(ps.stem(word.lower()))
            temp = [x for x in temp if x not in ('(', ')', ',', ';', '?', '!', '.', ' ' )]
            words += temp
            sv.append(dict(Counter(temp)))
            words = list(set(words))
        idf = {}
        for word in words:
            count = 0
            for sent in sent_tokenize_list:
                wordsInSent = []
                tokenized = word_tokenize(sent)
                filtered = [w for w in tokenized if not w in self.stop_words]
                for w in filtered:
                    wordsInSent.append(ps.stem(w.lower()))
                if word in wordsInSent:
                    count += 1
            idf[word] = math.log(len(sent_tokenize_list)+1/count)
        
        return sv, idf
        
#   findSim: Method to find tf-idf similarity between the sentences and the qv
#       returns the sorted similarity index
    def findSim(self, sv, qv, idf):
        sim = []
        dr1 = 0
        for word in qv:
                if word in idf:
                    dr1 += math.pow((idf[word]*qv[word]),2)
        for sent in sv:
            numr = 0
            dr2 = 0
            for word in sent:
                dr2 += math.pow((idf[word]*sent[word]),2)
            for word in qv.keys():
                if word in idf and word in sent:
                    numr += qv[word]*sent[word]*idf[word]*idf[word]
            if math.sqrt(dr1)*math.sqrt(dr2) != 0:
                sim.append(numr/(math.sqrt(dr1)*math.sqrt(dr2)))
        sim = sorted(enumerate(sim), key = operator.itemgetter(1), reverse = True)
        
        return sim