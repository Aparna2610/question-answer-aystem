# -*- coding: utf-8 -*-
"""
Created on Sat Feb 10 16:38:11 2018

@author: Aparna Gangwar
"""
# Importing libraries
from nltk.tokenize import word_tokenize

class Question:
    
#    __init__: Initialization method
#       Intialize the question_type attribute
#       Question types can me amongst the following:
#       question_types = ["where" => GPE, "when" => TIME, "who/whose/whom" => PERSON, "what/why/how" => SUMMARY]
#       returns null
    def __init__(self):
        self.question_type = ""
        return
        
#   classifyQuestion: Method to assign a question type to the input query
#        returns the question type
    def classifyQues(self, ques):
        qv = [x.lower() for x in word_tokenize(ques)]
        if "where" in qv:
            self.question_type = "GPE"
        elif "who" in qv or "whom" in qv or "whose" in qv:
            self.question_type = "PERSON"
        elif "when" in qv:
            self.question_type = "TIME"
        elif "what" in qv or "how" in qv or "why" in qv:
            self.question_type = "SUMMARY"
        
        return self.question_type