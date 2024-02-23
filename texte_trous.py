import random
import spacy
import pandas as pd
import re
from fugashi import Tagger
"""
générer des cartes anki texte à trou
- v 2.0 tokenization avec fugashi pour éviter erreur comme 「ところ」au lieu de　「ころ」 
"""
# variables
deck = {}
nlp = spacy.load('ja_core_news_sm',disable=['ner','tagger'])
particles = {'なんて','なんか'}
max_length = 16383
tagger = Tagger()

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
with open ('ikebukuro.txt', encoding='utf-8') as f:
    livre = f.read()

chunks = [livre[i:i+max_length] for i in range(0,len(livre),max_length)]
doc = nlp(random.choice(chunks))
phrases = [sent.text for sent in doc.sents]
phrases = [phrase for phrase in phrases if any(particle in [word.surface for word in tagger(phrase)] for particle in particles)]

try:
    dix_phrases = random.sample(phrases,10)
    make_quizz(dix_phrases)
except:
    if phrases == []:
        print("Il n'y a pas de phrases contenant cette sous-chaîne de caractères")
    else:
        make_quizz(phrases) # s'il y a moins de dix phrases contenant la sous-chaîne
