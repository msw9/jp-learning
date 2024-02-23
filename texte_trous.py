import random
import spacy
import pandas as pd
import re
"""
générer des cartes anki texte à trou
version alt pour mongues expressions et contexte
"""
# variables
deck = {}
nlp = spacy.load('ja_core_news_sm',disable=['ner','tagger'])
particles = {'でしょうか','のですか','んです'}
max_length = 16383

#fonctions
def question(texte, particles):
    for particle in particles:
        texte = re.sub(particle, "<font color=\"#0000ff\">(???)</font>", texte)
    return texte

def answer(texte, particles):
    for particle in particles:
        texte = re.sub(particle, f"<font color=\"#0000ff\">{particle}</font>", texte)
    return texte

def make_quizz(phrases): #list
    deck = {}
    deck['question'] = [question(phrase, particles) for phrase in phrases]
    deck['answer'] = [answer(phrase, particles) for phrase in phrases]
    df = pd.DataFrame.from_dict(deck)
    df.to_csv('quizz_jp.csv', index=False, header=False,sep='\t')
    
#main
with open ('pride.txt', encoding='utf-8') as f:
    livre = f.read()

chunks = [livre[i:i+max_length] for i in range(0,len(livre),max_length)]
doc = nlp(random.choice(chunks))
phrases = []
sentences = list(doc.sents)
sentences = [sent.text for sent in sentences]
for i, sent in enumerate(sentences):
    phrase = ""
    if any(particle in sent for particle in particles):
        if i > 0:
            phrase += sentences[i-1]
        phrase += sent
        phrases.append(phrase)
try:
    dix_phrases = random.sample(phrases,10)
    make_quizz(dix_phrases)
except:
    if phrases == []:
        print("Il n'y a pas de phrases contenant cette sous-chaîne de caractères")
    else:
        make_quizz(phrases) # s'il y a moins de dix phrases contenant la sous-chaîne
