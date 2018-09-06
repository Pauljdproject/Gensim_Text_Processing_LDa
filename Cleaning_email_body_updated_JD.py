# -*- coding: utf-8 -*-
"""
Created on Mon Jul 16 19:44:47 2018

@author: jkdadhich
"""
import re
Count = 0
from bs4 import BeautifulSoup
try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

from validate_email_address import validate_email

def remove_urls(vTEXT):
    Body_  =[el for el in vTEXT if not urlparse(el).scheme]
    Body_ ="".join(Body_)
    return(Body_)


def Cleaning_email_pandas(Body_):
    Body_ = str(Body_).lower()
    
    Body_ = re.sub(r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))''', " ", Body_)
    Body_ = re.sub(r'''(?i)\b((?:http?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))''', " ", Body_)
    
    Body_ = [ x for x in Body_ if validate_email(x) != True]
    Body_ = "".join(Body_)
    
    URLS  = re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', Body_)
    Body_ = [ x for x in Body_ if x not in URLS]
    Body_ = "".join(Body_)
    
    
    Body_ = remove_text_inside_brackets(Body_,brackets="<>[]")


#        Body_ = re.sub(r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]
#          +[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))
#          +(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))
#          ''', " ", Body_)
#        
    for j in range(1,5):
        try:

            New_Text = find_and_replace(Body_)
            Body_     = New_Text
        except ValueError:
            pass

    Body_ = re.sub(r"@|--|/hou/|cc:|to:|subject:|sent:|/corp/|/lon/|re:|","",Body_)
    Body_ = re.sub(r"enron@enron|/na/|enronenron|original message|from:","",Body_)
    
    Body_ = Remove_text_htm_end(Body_)
    Body_ = re.sub(r"--","",Body_)
    
    
    print (Body_)


    return Body_




def remove_text_inside_brackets(text, brackets):
#https://stackoverflow.com/questions/14596884/remove-text-between-and-in-python
    count = [0] * (len(brackets) // 2) # count open/close brackets
    saved_chars = [] # save the result to return
    for character in text:
        for i, b in enumerate(brackets):
            if character == b: # found bracket
                kind, is_close = divmod(i, 2)
                count[kind] += (-1)**is_close # `+1`: open, `-1`: close
                if count[kind] < 0: # unbalanced bracket
                    count[kind] = 0  # keep it
                else:  # found bracket to remove
                    break
        else: # character is not a [balanced] bracket
            if not any(count): # outside brackets
                saved_chars.append(character)
    return ''.join(saved_chars)

def Remove_text_htm_end(text):
    text_body =  str(text).split(" ")
    text_list = []
    for text in text_body:

        if str(text).endswith(".htm"):
            text_list.append(" ")
        elif str(text).endswith(".com"):
            text_list.append(" ")
        
        elif str(text).endswith(".html"):
            text_list.append(" ")

            
        else:
            text_list.append(text)

    return str(" ".join(text_list))



def find_and_replace(text,Start_Value="to:",End_value ="subject:"):
    index_ = text.index(Start_Value)
    End_   = text.index(End_value)+8
    New_text = text[index_:End_]
    Final_text = text.replace(New_text,"")
    del index_
    del End_
    return Final_text

import gensim
import nltk
from nltk.stem.wordnet import  WordNetLemmatizer
lemmatization_word = WordNetLemmatizer()
def Lemmatiztion_Process_(text):
    try:
        
        unicode_from_string = text.encode(encoding='utf-8')
        text                = unicode_from_string.decode('unicode-escape')
    except UnicodeDecodeError:
        text = str(text)
        
    tokens = [word.lower() for sent in nltk.sent_tokenize(text)for word in nltk.word_tokenize(sent)]
    # finding the lemma or root word which we ealier tokenized
        
    lemmas = [lemmatization_word.lemmatize(t.strip())for t in tokens]
        
        

    return lemmas

# =============================================================================
# Gensim Preprocess
# =============================================================================
def Gensim_preprocess(text):
    
    token_gensim = [token for token in gensim.utils.simple_preprocess(text) if token not in gensim.parsing.preprocessing.STOPWORDS]
    return  token_gensim

# =============================================================================

# =============================================================================


def Next_Level_Word_Clean(text):
    noise_words_list = ["iii","www","jpg","http","jpg",'th',
                        "msn",'com','iso','pm','am','a','ll','mw',
                        'yahoo','ena',"eb","xls","st","pdf","outlook",
                        "doc","hrweb","et","asp",".ect","xx","eol",
                        "nbsp","txt","ve","el","bg","tx","ut","kt","se",
                        "sw","nw","tw","ngx","da","usc","ed","ld","ng",
                        "wsj","sb","loveect","fw","for","a","of","and",
                        "to","in","ndas","ss","ab","plea","ma",'ke',
                        "ch","jr","mr",'eml','lme','xom',"bn","td","nda"]
    noise_re = [" ".join([w for w in t.split() if not w in noise_words_list]) for t in text]
   
    
    return noise_re

    


#from New_Text_Preprocess_Cleaning_part import Print_format
from File_Location_path_details import System_location_folders
File_path_detail_log = System_location_folders()
from gensim import corpora, models
def Dic_TFIDF_Corpus(texts,Dic_percentage):
    #File_path_detail_log.Gensim_Results()
    dictionary = corpora.Dictionary(texts) # Creating Dictionary
    # Dictionry Purning
#    Value_Of_ = int(round((len(dictionary)/100)*Dic_percentage,0))

    dictionary.filter_extremes(no_below=2)
    dictionary.compactify()
    dictionary.save('dict_1.dict')
    print (dictionary)
    # Creating Verctors
    corpus = [dictionary.doc2bow(text) for text in texts]
    # Wrapper of TFIDF Model
    corpus_tfidf = models.TfidfModel(corpus)
    # bulid TFIDF Corpus
    print ("Creating TF~iDF")
    corpus_tfidf_Value = corpus_tfidf[corpus]
    corpora.MmCorpus.save_corpus("corpus_tfidf_Value.mm",corpus_tfidf_Value)
    return corpus_tfidf_Value

Score_of_Model = {}
from gensim.models import CoherenceModel

def lsi_Best_Topic_Model_(corpus_tfidf_Value,chunksize,
                          dictionary,texts,
                          Start_range,End_range):
    global Score_of_Model
    for j in range(Start_range,End_range):
        
        value_topic_number =int(j+1)
        print ("Processing Topic :",value_topic_number)
        # Performing LSI MODEL
        lsi = models.LsiModel(corpus = corpus_tfidf_Value,
                              num_topics=value_topic_number,
                              id2word=dictionary,
                              chunksize=chunksize,onepass=True,
                              power_iters=5,extra_samples=1
                                  )

        # Calulating The Coherence Value for Best Number of Topic's
        cm = CoherenceModel(model=lsi, texts=texts,
                            dictionary=dictionary, coherence='c_v')

        Score_of_Model[j+1] = (cm.get_coherence())

        del  cm
        del  lsi
        
    return Score_of_Model