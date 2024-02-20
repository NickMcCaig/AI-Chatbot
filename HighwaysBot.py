#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Basic chatbot design --- for your own modifications
"""
#######################################################
# Initialise Wikipedia agent
#######################################################
import wikipedia, csv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords
import nltk
import vision
import voice
import string
import Utilities
import highways
import game
import sentiment
import FOK
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from nltk.inference.resolution import ResolutionProver
from nltk.inference import Prover9, Prover9Command
from nltk.sem.logic import *
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('averaged_perceptron_tagger')
stopwords = stopwords.words('english')
voiceRec = False
#######################################################
# Initialise weather agent
#######################################################
import json, requests
#insert your personal OpenWeathermap API key here if you have one, and want to use this feature
APIkey = "" 
CSVFILEURI = 'new.csv'
KBURI = 'kb.txt'
LANGUAGE = 'en'
COMMENTCSV = 'comments.csv'
#######################################################
#  Initialise AIML agent
#######################################################
import aiml
# Create a Kernel object. No string encoding (all I/O is unicode)
kern = aiml.Kernel()
kern.setTextEncoding(None)
#if not FOK.validate_kb():
#    print("The FOK KB failed to load as it is invalid")
#KB = FOK.Load_KB()

# Use the Kernel's bootstrap() method to initialize the Kernel. The
# optional learnFiles argument is a file (or list of files) to load.
# The optional commands argument is a command (or list of commands)
# to run after the files are loaded.
# The optional brainFile argument specifies a brain file to load.
kern.bootstrap(learnFiles="mybot-basic.xml")
#######################################################
# Welcome user
#######################################################
print("Welcome to this chat bot. Please feel free to ask questions from me!")
def Load_QandACSV():
    with open(CSVFILEURI, mode= 'r',encoding='latin-1')  as f:
        _reader = csv.DictReader(f)
        dic = {}
        for row  in _reader:
           #print(row)
           row = row['Que'],row['Ans']
           dic[row[0]] = row[1] 
        #print(dic)
        return dic
csvQuestions = Load_QandACSV()


def cosine_sim_vectors(vec1, vec2):
    #Calculate the cosine similarity between two vectors
    vec1 = vec1.reshape(1, -1)
    vec2 = vec2.reshape(1, -1)
    return cosine_similarity(vec1, vec2)[0][0]
# https://towardsdatascience.com/calculating-string-similarity-in-python-276e18a7d33a
def cleanString(text):
    text = ''.join([word for word in text if word not in string.punctuation])
    text = text.lower()
    text = ' '.join([word for word in text.split() if word not in stopwords])
    return text
def SimilarityMatch(toMatch):
    tomatchquestions = list(csvQuestions.keys())
    tomatchquestions.insert(0,toMatch)
    cleaned = list(map(cleanString, tomatchquestions))
    #print(cleaned)
    vectorizer = CountVectorizer().fit_transform(cleaned)
    vectors = vectorizer.toarray()
    bestMatch = -1
    bestMatchItem = -1
    for x in range(len(csvQuestions)):
        similarity = cosine_sim_vectors(vectors[0],vectors[x + 1])
        if(similarity != 0 and similarity > bestMatch):
            bestMatch = similarity
            bestMatchItem = x
    return(bestMatchItem)

def get_url(string):
    match = re.search("(?P<url>https?://[^\s]+)", string)
    if match:
        return match.group("url")
    else:
        return None
def chat_output(text, alreadyTranslated=False):
    if not alreadyTranslated and LANGUAGE != 'en':
        text = vision.translate(text, 'en', LANGUAGE)
        
    if voiceRec:
        voice.textToVoice(text)
    else:
        print(text)
def chat_input(voiceRec):
    if voiceRec == False:
        try:
            userInput = input("> ")
        except:
            chat_output("Bye!")
    else: 
        try:
            userInput = voice.recognize_from_microphone()
        except (Exception) as e:
            chat_output("You didn't say anything or an error occured, resorting to text based")
            voiceRec = False
            userInputlng = 'en'
    userInputlng = vision.detectLanguage(userInput)
    if userInputlng != 'en':
        userInput = vision.translate(userInput, userInputlng, 'en')
        LANGUAGE = userInputlng
    return userInput
#######################################################
# Main loop
#######################################################
while True:
    #get user input
    userInput = chat_input(voiceRec)
    #pre-process user input and determine response agent (if needed)
    responseAgent = 'aiml'
    #activate selected response agent
    if responseAgent == 'aiml':
        answer = kern.respond(userInput)
    #post-process the answer for commands
    if answer[0] == '#':
        params = answer[1:].split('$')
        cmd = int(params[0])
        if cmd == 0:
            print(params[1])
            break
        elif cmd == 1:
            try:
                wSummary = wikipedia.summary(params[1], sentences=3,auto_suggest=False)
                chat_output(wSummary)
            except:
                chat_output("Sorry, I do not know that. Be more specific!")
        elif cmd == 3: # I know that x is y  
            if (params[1].find(" is ") != -1):
                obj, subj = params[1].split(" is ")
            chat_output(FOK.Add_To_Knowledgebase(obj, subj, KB))
        elif cmd == 4: # check that x is y 
            if (params[1].find(" is ") != -1):
                obj, subj = params[1].split(" is ")
            chat_output(FOK.confirmLogic(obj,subj, KB))
        elif cmd == 5: # check that x has y :
            if (params[1].find(" has ") != -1):
                obj, subj = params[1].split(" has ")
            chat_output(FOK.confirmLogic(obj,subj, KB))
        elif cmd == 5: # show all info in knowlage base
            FOK.fopl_to_readable(KB)
        elif cmd == 70:
            newlang = vision.get_language_code(params[1])
            if newlang != None:
                LANGUAGE = newlang
            chat_output("Language now set")
        elif cmd == 11:
            text = vision.findText(get_url(userInput))
            frmlng = vision.detectLanguage(text)
            tolng = vision.get_language_code(Utilities.get_last_word(userInput)) 
            if(tolng is None):
                chat_output(text) 
            else:
                chat_output(vision.translate(text,frmlng,tolng), True)
        elif cmd == 51:
            chat_output("This report was last reported in our system as: " +highways.getHighwayProblemByID(params[1]))
        elif cmd == 52:
            game.game(chat_output,chat_input,voiceRec)
        elif cmd == 53:
            chat_output("Please leave your comment now:")
            comment = chat_input(voiceRec)
            score = sentiment.calculate_sentiment(comment)
            chat_output(str(score))
            if(score > 0.5):
                chat_output('Thank you for your positive feedback! We will look at it soon')
            elif(score < -0.5):
                chat_output('We are sorry about your negative experance, please contact us, we will review the feedback soon')
            else:
                chat_output('Thank you for your feedback, we will review this soon')
            sentiment.store_comment(comment,score,COMMENTCSV)
        elif cmd == 99:
            if(params[1] in csvQuestions):
                chat_output(csvQuestions[params[1]])
            else:
                test = SimilarityMatch(params[1])
                if(test == -1):
                    chat_output("I did not get that, please try again.")
                else:
                    bestmatchQuestion = list(csvQuestions.values())[test]
                    chat_output(bestmatchQuestion)
            
    else:
        chat_output(answer)

    

