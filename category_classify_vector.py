import nltk
import json
import numpy as np
import gensim
import tensorflow as tf 
from gensim.models import Word2Vec
from keras.preprocessing import sequence
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
#nltk.download('punkt')
#nltk.download('averaged_perceptron_tagger')


def One_hot(data):
    index_dict = {value:index for index,value in enumerate(set(data))}
    encodings = []
    for value in data:
        one_hot = np.zeros(len(index_dict))
        index = index_dict[value]
        one_hot[index] = 1
        encodings.append(one_hot)
    return np.array(encodings)


#Proccessing
file = open('bbc-text.csv.(1)_restored.csv', 'r', encoding='ISO-8859-1')
data = csv.reader(file)
category_list = {'tech' : 0, 'business' : 1, 'sport' : 2, 'entertainment' : 3, 'politics' : 4}


token =[]
embeddingmodel = []


#토큰화
for i in data:
    headline = i[1]
    sentence = nltk.word_tokenize(headline)
    temp = []
    temp_embedding = []
    all_temp = []
    for k in range(len(sentence)):
        temp_embedding.append(sentence[k])
        temp.append(sentence[k])
    all_temp.append(temp)
    category = i[0] 
    all_temp.append(category_list.get(category))
    token.append(all_temp)



# 벡터화
embeddingmodel = []
for i in range(len(token)):
    temp_embeddingmodel = []
    for k in range(len(token[i][0])):
        temp_embeddingmodel.append(token[i][0][k])
    embeddingmodel.append(temp_embeddingmodel)

embedding = Word2Vec(embeddingmodel, size=300, window=5, min_count=10, iter=5, sg=1, max_vocab_size=360000000)
embedding.save('post.embedding')


model = Word2Vec.load('post.embedding')
model.wv.most_similar('lie')
model.wv['good']




