# import des librairies
import nltk
import numpy as np
import random
import string # to process standard python strings
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from stop_words import get_stop_words


def tokens():
    # import du texte & nettoyages
    f=open('./static/infos_corona.txt','r',errors = 'ignore', encoding = "utf8")
    raw=f.read()
    #raw=raw.lower()# not necessare
    # quelques modifications : 
    raw = re.sub(r"n.c.a.", "", raw)

    # Création d'une liste de phrases (= tokenization)
    sent_tokens = nltk.sent_tokenize(raw, language="french")

    # on a beaucoup de questions ici : on les enlève
    for i in sorted(range(len(sent_tokens)), reverse = True):
        if re.search(r"\?", sent_tokens[i]):
            del sent_tokens[i]
    # on enlève les doublons
    sent_tokens = list(set(sent_tokens)) 

    return sent_tokens

# On crée une liste nettoyée mais qui ne sera pas celle dans laquelle
# on ira chercher les réponses, simplement pour la création de la
# matrice TF-IDF
def nettoyage(texte):
    # on remplace covid-19 par coronavirus
    
    texte = re.sub('covid-19| virus|covid 19 |sars-cov', 'coronavirus', texte)
    # on remplace les "coronavirus coronavirus" par coronavirus
    texte = re.sub('coronavirus coronavirus', 'coronavirus', texte)
    texte = re.sub(f"[{string.punctuation}]", " ", texte)
    texte = re.sub('[éèê]', 'e', texte)
    texte = re.sub('[àâ]', 'a', texte)
    texte = re.sub('[ô]', 'o', texte)
    #texte = re.sub('mort(\w){0,3}|deces|deced(\w){1,5}', 'deces', texte)
    #texte = re.sub('medec(\w){1,5}|medic{1,5}', 'medical', texte)
    return texte



def tokens_net():
# import du texte & nettoyages
    f=open('./static/infos_corona.txt','r',errors = 'ignore', encoding = "utf8")
    raw=f.read()

    # quelques modifications : 
    raw = re.sub(r"n.c.a.", "", raw)

    # Création d'une liste de phrases (= tokenization)
    sent_tokens = nltk.sent_tokenize(raw, language="french")

    # on a beaucoup de questions ici : on les enlève
    for i in sorted(range(len(sent_tokens)), reverse = True):
        if re.search(r"\?", sent_tokens[i]):
            del sent_tokens[i]
    # on enlève les doublons
    sent_tokens = list(set(sent_tokens)) 
    phrases_nettoyees = []
    for i in range(len(sent_tokens)):
        phrases_nettoyees.append(nettoyage(sent_tokens[i]))
    return phrases_nettoyees

def matrix_tfidf_fit(phrases_nettoyees):
# Entraînement d'une matrice TF-IDF
    french_stop_words = get_stop_words('french')
    TfidfVec = TfidfVectorizer(stop_words = french_stop_words)
    tfidf = TfidfVec.fit(phrases_nettoyees)

    return tfidf

def matrix_tfidf_trans(tfidf, phrases_nettoyees):

    # on crée la matrice TF-IDF sur le texte de la page wiki
    phrases_tf = tfidf.transform(phrases_nettoyees)
    return phrases_tf