from datasets import load_dataset
import random
import spacy
import torch
nlp = spacy.load('ja_core_news_sm')

substring = 'わけがないでしょ'

def extract_sentences(texte):
    try:
        doc = nlp(texte)
        phrases = [sent.text for sent in doc.sents if substring in sent.text]
        return phrases
    except:
        return

dataset = load_dataset("oscar-corpus/OSCAR-2201",
                        token="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", # required
                        language="ja", 
                        streaming=True, # optional
                        split="train",
                       trust_remote_code=True) # optional, but the dataset only has a train split

#print(dataset.features)
dataset = dataset.shuffle(buffer_size=100)
filtered_ds = dataset.filter(lambda x: substring in x['text'])
count = 0
for example in filtered_ds:
    print(extract_sentences(example['text']))
    count+=1
    if count >=5:
        break

