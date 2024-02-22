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
particles = {'わけがない','はずがない'}
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
#main
with open ('ikebukuro.txt', encoding='utf-8') as f:
    livre = f.read()

chunks = [livre[i:i+max_length] for i in range(0,len(livre),max_length)]
doc = nlp(random.choice(chunks))
# phrases = [sent.text for sent in doc.sents if any(particle in sent.text for particle in particles)]
phrases = []
sentences = list(doc.sents)
for i, sent in enumerate(sentences):
    phrase = ""
    if any(particle in sent.text for particle in particles):
        if i > 0:
            phrase += doc.sents[i-1].text
        phrase += sent.text
        phrases.append(phrase)
print(phrases)
"""
dix_phrases = random.sample(phrases,10)
deck['question'] = [question(phrase, particles) for phrase in dix_phrases]
deck['answer'] = [answer(phrase, particles) for phrase in dix_phrases]

df = pd.DataFrame.from_dict(deck)
df.to_csv('quizz_jp.csv', index=False, header=False,sep='\t')
"""
