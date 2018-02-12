# -*- coding: utf-8 -*-
"""
Created on Fri Feb  9 21:07:30 2018

@author: Aparna Gangwar
"""
# Importing libraries
from processData import processData
from Question import Question
from Answer import Answer
import json
import re
import sys
import math
import operator

class Main:
#    __init__: Initialization method
#       Initialize the system with the dataset passed as command line argument 1.
#       Prompt the user to start entering questions
#       While the user doesn't enter "exit" or "bye", keep taking questions.
#       returns null
    def __init__(self):
        if sys.argv[0] == "p2.py":
            filename = sys.argv[1]
            f = open(filename, 'r')
            data = f.readline()
            f.close()
            self.jsonData = json.loads(data)
            paras = []
            for paraIndex in range(0,len(self.jsonData['paragraphs'])):
                paras.append(self.jsonData['paragraphs'][paraIndex]['context'])
            self.text = "\n\n\n\n".join(paras)
            print("The system is ready! You may start now.")
            print("Enter bye or exit to exit the system.")
            while True:
                self.question = input(">")
                if self.question not in ["Bye".lower(), "Exit".lower()]:
                    answer = self.main()
                    print(answer)
                else:
                    print("Exiting...")
                    exit()
        return

    def tester(self,paragraph):
        self.text = paragraph
    
    def testAnswer(self,question):
        self.question = question
        return self.main()
        
#   Main method: The driver method for the system
#       Split the text input into paragraphs
#       Find the query vector using processData.queryVector()
#       For every para find the tfVector using processData.findTfVector()
#       For every word in text, find the idf vector
#       Finds the similarity between a para and the query and finds the most similar paragraphs using tf-idf index.
#       Classify the query to find the type of question by calling Question.classifyQues()
#       Find the answer using the question type by calling Answer.getAnswer()   
#       returns answer 
    def main(self):
        self.idf = {}
        self.paras = re.split('\s{4,}',self.text)

        N = len(self.paras)
        ni = {}
        tf = []

        self.qv = processData(self).queryVector(self.question)

        for para in self.paras:    
            pd = processData(self)
            temp = pd.findTfVector(para)
            tf.append(temp)
            for word in temp.keys():
                if not word in ni:
                    ni[word] = 0
                ni[word] +=1
        for word in ni: 
            self.idf[word] = math.log((N+1)/ni[word])
        sim = []
        for tfForDoc in tf:
            sim.append(processData(self).findSim(self.qv, tfForDoc, self.idf))
        self.sim = sorted(enumerate(sim), key = operator.itemgetter(1), reverse = True)
        self.question_type = Question().classifyQues(self.question)
        self.answer = Answer().getAnswer(self)
        return self.answer

# If the script is run by name then the obj is created and instantiated from here.
# This is checked to avoid multiple instantiations when the obj is instantiated from TestQas.py.
if sys.argv[0] == "p2.py":
    Main()