import requests as requests
from scrapy.selector import Selector
import regex as re
import numpy as np
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from textblob import Word
from sklearn.feature_extraction.text import TfidfVectorizer
import time
from sklearn.metrics.pairwise import cosine_similarity

def get_planet(planet):
    """Takes in a name (string format) of a planet in our solar system, scrape the website with facts about it,
    clean text such that it contains only meaningful words and returns a list with the facts about selected planet"""
    response = requests.get("https://theplanets.org/"+planet+"/").content
    xpath = '//div[@class="entry-content"]/ul/li'
    sel = Selector(text = response)
    l = sel.xpath(xpath).extract()
    rgx = r"<(.+?)>"
    k = [re.sub(rgx,"",i) for i in l]
    return k

def NLP(doc_list):
    """Takes in the list of string documents, process the text such that it contains only
    key words in basic form and returns a TF-IDF matrix of the processed text"""
    splited = [word_tokenize(i) for i in doc_list]
    alphabetic = [[i for i in j if i.isalpha()] for j in splited]
    lower = [[i.lower() for i in j] for j in alphabetic]
    nosw = [[i for i in j if i not in stopwords.words('english')] for j in lower]
    lemm = [[Word(i).lemmatize() for i in j] for j in nosw]
    final = [" ".join(i) for i in lemm]
    tfidf = TfidfVectorizer()
    vectorized = tfidf.fit_transform(final)
    vectors = vectorized.A
    return vectors

def similarity(matrix):
    """Takes in the TF-IDF matrix and returns the index and value of the highest cosine similarity
    between last vector and other vectors"""
    similarities = cosine_similarity(matrix[-1].reshape(1, -1),matrix)
    similarities = similarities[0][:(matrix.shape[0]-1)]
    index = np.argmax(similarities)
    return [index,similarities[index]]

bot = 0
# create list of invitational greets
greets = ["Hi! My name is bot. I can speak with you about planets. In which planet are you interested in?",
            "Hello, I am bot. I can tell you something interesting about planets. About which planet would you like to talk?",
            "Hi, here is bot. I am an expert on planets. which planet would you like to explore?"]
# create list of final greets
end_greets = ["Good bye!","Have a nice day!","Bye bye!"]
planets = ["mercury","venus","earth","mars","jupiter","saturn","uranus","neptune","pluto"]
# create four lists with bot´s answers for situations when the ML algorithm cannot be used
bot_response_1 = ["So you do not want to speak about planets?","Just tell me, which planet would you like to explore...","Maybe we can talk later?"]
bot_response_2 = ["Great! what would you like to know about ","Cool! what are you interested in about ", "Nice! What can I tell you about "]
bot_response_3 = ["Choose only one planet please!", "Let´s talk about one planet only.","Better to speak only about one planet."]
bot_response_4 = ["I do not understand... try to ask question different way please.","Sorry, I cannot answer on this question...",
                  "I am not enough clever to answer this... Could you maybe ask something different? "]
user_planet = 0

# create an infinite loop
while True:
    # if there was not any sentence written before, bot will start by randomly choosing one of the invitational greets and take an input of user
    if bot == 0:
        greet = np.random.choice(greets)
        print(greet)
        bot += 1
        response = input()
    else:
        # if there was a response from user, the response will be splitted on spaces and all of the words will be turned to lowercase
        splited = response.split()
        splited = [i.lower() for i in splited]
        # if there was word "bye" in the user response, bot will randomly choose one of the final greets and the program will finish
        if "bye" in splited:
            print(np.random.choice(end_greets))
            time.sleep(2)
            exit()
        else:
            selection = [i for i in splited if i in planets]#check if user specify planet
            if len(selection)==0 and user_planet==0:
                print(np.random.choice(bot_response_1))#if user does not specify planet, random response is generated
                response = input()
            elif len(selection)== 1 and user_planet==0:
                user_planet=selection[0]
                print(np.random.choice(bot_response_2)+selection[0]+"?")#if planet is specified, bot will ask, what user would like to know
                response = input()
                documents = get_planet(selection[0])#select documents about specified planet
                documents.append(response)
            elif len(selection) > 1 and user_planet == 0:
                print(np.random.choice(bot_response_3))#if user specifies more planets, bot will ask user to choose only one planet
                response = input()
            elif len(selection) == 1 and user_planet != 0:
                if selection[0] != user_planet:
                    user_planet = selection[0]
                    print(np.random.choice(bot_response_2) + selection[0] + "?")#if user specifies only one planet, bot will ask, what user wants to know
                    response = input()
                    documents = get_planet(selection[0])#bot will choose documents related to specified planet
                    documents.append(response)#user´s response will append to documents
                else:
                    tfidf = NLP(documents)#get TFIDF matrix from documents
                    l = similarity(tfidf)#get similarities
                    if l[1] == 0.0:
                        print(np.random.choice(bot_response_4))#if similarity is zero, print answer that bot does not understand
                        response = input()
                        documents[-1] = response
                    else:
                        print(documents[l[0]])#print sentence which had the highest cosine similarity with question
                        response = input()
                        documents[-1] = response
            else:

                tfidf = NLP(documents) #if there was not name of planet in user´s response, following branch will be executed
                l = similarity(tfidf)
                if l[1] == 0.0:
                    print(np.random.choice(bot_response_4))
                    response = input()
                    documents[-1] = response
                else:
                    print(documents[l[0]])
                    response = input()
                    documents[-1] = response














