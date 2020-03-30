# on définit la fonction qu'on appellera dans le chatbot : elle renvoie 
# la phrase la plus proche de celle posée par l'utilisateur
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import re
import random
import json
import numpy as np


def bot_reponse(message, phrases_tf, sent_tokens, user, tfidf):
    bonjour = r"salut.*|bonjour.*|coucou.*|cc.*|hello.*"
    reponse_bonjour_bot = ["Bonjour à toi", "Hello", "Salut", "Hi"]
    message = message.lower()
    # on a besoin d epasser la chaîne de caractère dans une liste :
    phrase_user = [message]
    # On calcule les valuers TF-IDF pour la phrase de l'utilisateur
    user_tf = tfidf.transform(phrase_user)
    # on calcule la similarité entre la question posée par l'utilisateur
    # et l'ensemble des phrases de la page wiki
    similarity = cosine_similarity(user_tf, phrases_tf).flatten()
    # on sort l'index de la phrase étant la plus similaire
    index_max_sim = np.argmax(similarity)
    # Si la similarité max ets égale à 0 == pas de correspondance trouvée
    if(similarity[index_max_sim] == 0):
        if (re.fullmatch(bonjour, message)):
            robo_response = f"{random.choice(reponse_bonjour_bot)} {user}"
        elif (re.search("au revoir", message)):
            robo_response = f"au revoir {user}, n'oublie pas: Reste chez toi! "
        else:
            robo_response = f"J'ai pas compris {user}, soit plus claire stp. "
    # Sinon, on sort la phrase correspondant le plus : 
    else:
        robo_response = sent_tokens[index_max_sim]
    return robo_response