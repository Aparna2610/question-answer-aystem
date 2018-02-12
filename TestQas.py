# -*- coding: utf-8 -*-
"""
Created on Sun Feb 11 17:49:53 2018

@author: Aparna Gangwar
"""

# Importing libraries
from nltk.tokenize import word_tokenize
from Question import Question
from p2 import Main
import json
import sys

class TestQas:

#    __init__: Initialization method.
#       returns null
    def __init__(self):
        return
        
#   readFile: Read file
#       Reads the file and parses it as json
#       Assigns title and jsonData attributes to obj
#       returns null           
    def readFile(self, filename):
        f = open(filename, 'r')
        data = f.readline()
        f.close()
        self.jsonData = json.loads(data)
        self.title = self.jsonData['title']
        return
        
#   getParagraph: Gets paragraphs from the dataset
#       Reads the paragraphs from the dataset passed
#       Takes filename as an optional argument. If filename is not passed,
#       make sure the obj has been initialized with all the required attributes.
#       returns a list of paragraphs
    def getParagraph(self, filename = None):
        if filename != None:
            self.readFile(filename)
        paras = []
        for paraIndex in range(0,len(self.jsonData['paragraphs'])):
            paras.append(self.jsonData['paragraphs'][paraIndex]['context'])
        return paras

#   getAccuracy: Gets Accuracy of the system for a data file
#       Finds the accuracy of the system by getting answers for all the questions
#       and matching them with the list of answers possible for that question.
#       returns accuarcy
    def getAccuracy(self, filename):
       if filename != None:
            self.readFile(filename)
       testPara = self.getParagraph()
       testPara = "    ".join(testPara)
       drm = Main()
       drm.tester(testPara)
       questionType = Question()
       result = []
       for index in range(0,len(self.jsonData['paragraphs'])):
           paras = self.jsonData['paragraphs'][index]
           for quesNo in range(0,len(paras['qas'])):
               question = paras['qas'][quesNo]['question']
                #print(question)
               qtype=questionType.classifyQues(question)
                #print(qtype)
               if(qtype not in ["PERSON", "LOCATION", "SUMMARY", "TIME"]):
                   continue
               ansr = drm.testAnswer(paras['qas'][quesNo]['question'])
               answers = []
               for ans in paras['qas'][quesNo]['answers']:
                   answers.append(ans['text'].lower())
               ansr = ansr.lower()
               isMatch = False
               for rt in word_tokenize(ansr):
                   if [rt in word_tokenize(ans) for ans in answers].count(True) > 0:
                        isMatch = True
                        break
#     Open the following lines to print all questions and their answers
#               try:
#               if isMatch:
#                   print(question,r,str(answers),isMatch)
#                   else:
#                       print("No Match")
#               except:
#                   print("Error")
               result.append((index, quesNo, question, ansr, str(answers),isMatch))
                    
       noOfResult = len(result)
       correct = [r[5] for r in result].count(True)
       if noOfResult == 0:
           accuracy = -1
       else:
            accuracy = correct/noOfResult
       return accuracy
    
#   runAll: Runs the system for all datasets and prints their accuracy
    def runAll(self): 
        files = ["d1.txt", "d2.txt", "d3.txt", "d4.txt", "d5.txt"]
        total = 0
        for file in files:
            d=self.getAccuracy(file)
            print("For "+ file + ", the accuracy is:",d)
            total += d
        print("The average accuracy of the system is: "+ str(total/len(files)))

if sys.argv[0] == "TestQas.py":        
    TestQas().runAll()