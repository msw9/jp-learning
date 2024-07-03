import pandas as pd
import numpy as np
from collections import Counter
from fugashi import Tagger
"""
Classification de texte
1) Naive Bayes
2) Bernouilli
"""
def nbr_of_c(data,c): # YES
    return len(list(filter(lambda x:x[1]==c,data)))

def p_t_c(phrase,c,data,tagger,v): #YES
    total = {}
    data = list(filter(lambda x:x[1]==c,data))
    for entry in data:
        total.update(dict(Counter([word.surface for word in tagger(entry[0])])))
    for word in tagger(phrase):
        if word.surface in total:
            yield (total[word.surface] + 1) / (sum(total.values()) + v)
        else:
            yield  1 / (sum(total.values()) + v)

def vocabulary(tagger,data): # YES
    memo = []
    for entry in data:
        for word in tagger(entry[0]):
            if word.surface not in memo:
                memo.append(word.surface)
    return len(memo)
def p_t_c_bernouilli():
    yield ()/(+ v)
def main_naive_bayes(corpus):#df
    tagger = Tagger()
    train_df = corpus.sample(frac=0.8,random_state=200)
    test_df = corpus.drop(train_df.index)
    # TRAIN
    train = train_df.values.tolist()
    n = len(train)
    v = vocabulary(tagger,train)
    """
    p_n1 = nbr_of_c(train,1)/n
    p_n2 = nbr_of_c(train,2)/n
    p_n3 = nbr_of_c(train,3)/n
    p_n4 = nbr_of_c(train,4)/n
    p_n5 = nbr_of_c(train,5)/n
    """
     # TEST 
    test = test_df.values.tolist()
    phrase = "オスマンの大規模開発事業を抗議した。"
    liste = [(nbr_of_c(train,i)/n) * np.prod(list(p_t_c(phrase,i,train,tagger,v))) for i in range(1,6)]
    index = 0
    max_element = liste[0]
    for i in range(1,len(liste)):
        if liste[i] > max_element:
            max_element = liste[i]
            index = i
    print(liste)
    print(max_element, index + 1)
    
def main_bernouilli(corpus):
    tagger = Tagger()
    train_df = corpus.sample(frac=0.8,random_state=200)
    test_df = corpus.drop(train_df.index)
    #TRAIN
    train = train_df.values.tolist()
    n = len(train)
    v = 5 # car 5 niveaux JLPT
    
if __name__=='__main__':
    df = pd.read_csv('corpus.csv')
    main_naive_bayes(df)
    main_bernouilli(data)
