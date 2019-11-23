#import Word2Vec as Word2Vec
import time
import csv
import nltk
import json
import numpy as np
import gensim
import tensorflow as tf 
from gensim.models import Word2Vec
import Bi_LSTM as Bi_LSTM
#nltk.download('punkt')
#nltk.download('averaged_perceptron_tagger')

def Zero_padding(train_batch_X, Batch_size, Maxseq_length, Vector_size):
    zero_pad = np.zeros((Batch_size, Maxseq_length, Vector_size))
    for i in range(Batch_size):
        zero_pad[i,:np.shape(train_batch_X[i])[0],:np.shape(train_batch_X[i])[1]] = train_batch_X[i]
    return zero_pad




def One_hot(data):
    index_dict = {value:index for index,value in enumerate(set(data))}
    encodings = []
    for value in data:
        one_hot = np.zeros(len(index_dict))
        index = index_dict[value]
        one_hot[index] = 1
        encodings.append(one_hot)
    return np.array(encodings)

def Convert2Vec(model_name, doc):
    word_vec = []
    model = Word2Vec.load(model_name)
    for sent in doc:
        sub = []
        for word in sent:
            if word in model.wv.vocab:
                sub.append(model.wv[word]) # Word Vector Input
            else:
                #Conficient
                sub.append(np.random.uniform(-0.25,0.25,300)) # used for OOV words
        word_vec.append(sub)
    return word_vec

#Proccessing
file = open('bbc-text.csv.(1)_restored.csv', 'r', encoding='ISO-8859-1')
data = csv.reader(file)


category_list = {'tech' : 0, 'business' : 1, 'sport' : 2, 'entertainment' : 3, 'politics' : 4}
token =[]
embeddingmodel = []


for i in data:
    headline = i[1]
    rawdata = nltk.word_tokenize(headline)
    sentence = nltk.pos_tag(rawdata)
    temp = []
    temp_embedding = []
    all_temp = []
    for k in range(len(sentence)):
        temp_embedding.append(sentence[k][0])
        temp.append(sentence[k][0] + '/' + sentence[k][1])
    all_temp.append(temp)
    #embeddingmodel.append(temp_embedding)
    category = i[0] 
    all_temp.append(category_list.get(category))
    token.append(all_temp)

print("토큰 처리 완료")

embeddingmodel = []
for i in range(len(token)):
    temp_embeddingmodel = []
    for k in range(len(token[i][0])):
        temp_embeddingmodel.append(token[i][0][k])
    embeddingmodel.append(temp_embeddingmodel)

embedding = Word2Vec(embeddingmodel, size=300, window=5, min_count=10, iter=5, sg=1, max_vocab_size=360000000)
embedding.save('post.embedding')


tokens = np.array(token)
print("token 처리 완료")
print("train_data 최신 버전인지 확인")
train_X = tokens[:, 0]
train_Y = tokens[:, 1]

--------------------------------------------------------------------------------------------------


train_Y_ = One_hot(train_Y)
#train_X_ = W2V.Convert2Vec("Data\\post.embedding",train_X)
train_X_ = Convert2Vec('post.embedding',train_X)



Batch_size = 32
Total_size = len(train_X)
Vector_size = 300
seq_length = [len(x) for x in train_X]
Maxseq_length = max(seq_length)
learning_rate = 0.001
lstm_units = 128
num_class = 5
training_epochs = 5
keep_prob = 0.75


X = tf.placeholder(tf.float32, shape = [None, Maxseq_length, Vector_size], name = 'X')
Y = tf.placeholder(tf.float32, shape = [None, num_class], name = 'Y')
seq_len = tf.placeholder(tf.int32, shape = [None])

-------------------------------------------------------------------
CNN : convolution -> pooling 
BiLSTM = Bi_LSTM.Bi_LSTM(lstm_units, num_class, keep_prob) => RNN CNN으로
**CNN은 단어 등장순서/문맥 정보를 보존한다.(텍스트의 지역적인 정보 보존)
RNN은 단어 입력값을 순서대로 처리함으로써, CNN은 문장의 지역 정보를 보존함으로써 단어/표현의 등장순서를 학습에 반영하는 아키텍처.
즉 자연언어처리를 위해 CNN 사용 max-pooling 과정을 거쳐 클래스 개수(결과값 5개 : sport ~~등등) 
import tensorflow as tf
import random
import matplotlib.pyplot as plt
from tensorflow.examples.tutorials.mnist import input_data
%matplotlib inline
tf.set_random_seed(777)


------------여기부터 다시 하면 됨. 위에까지는 성공했음. 
with tf.nn.conv2d(self.embedded_chars_expanded,
			W,
			strides=[1,1,1,1], // 배치데이터 하나씩, 단어 하나씩 슬라이딩 하면서 보라는 의미 => strides 값 [batch_size, input_height, input_width, input_channels] 순서임. 
			padding="VALID",
			name="conv")
h = tf.nn.relu(tf.nn.bias_add(conv,b), name="relu") // bias -8 시범 조정
// 코드 설명 - 이렇게 conv를 적용한 뒤의 텐서 차원수는 [batch_size, sequence_length-filter_size+1,1,num_filters] 가 된다. 이후 ReLU 를 써서 non-linearity 확보한다. 
//------------------
//max-pooling 코드
Pooled = tf.nn.max_pool(h,
			Ksize=[1, sequence_length ? filter_size + 1, 1, 1],
			Strides=[1,1,1,1],
			Padding=’VALID’,
			Name=”pool”)
// 이후 MAS-pooling 한 결과물을 합치고 FC(Full-connected layer) 를 통과시켜 각 클래스에 해당하는 스코어를 낸 뒤 크로스엔트로피 오차를 구한 후 backpropagation 수행해서 필터의 weight 등 파라미터 값들을 업데이트하는 과정을 거친다. 여기서 특이점은 단어벡터의 모음인 lookup 테이블도 학습과정에서 같이 업데이트 한다.

이때, word2vec 에서 시쿼나이즈 부분에 문제가 생겨서 이 부분을 해결하기 위해 노력하고 있는 중이다. (CNN과 word2vec 를 접목시키는 과정에서 문제가 발생)
TF-IDF vs Word2VEC 중에서 무엇을 선택할지 고민중이다. 랜덤포레스트를 이용하면 결과가 더 잘 나올 것 같다고 생각해서 이쪽으로 구현을 생각중이다. 


			
    logits = BiLSTM.logits(X, BiLSTM.W, BiLSTM.b, seq_len)
    loss, optimizer = BiLSTM.model_build(logits, Y, learning_rate)

prediction = tf.nn.softmax(logits)
correct_pred = tf.equal(tf.argmax(prediction, 1), tf.argmax(Y, 1))
accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))

init = tf.global_variables_initializer()

total_batch = int(Total_size / Batch_size)

print("Start training!")

modelName = "BiLSTM.model"
saver = tf.train.Saver()

with tf.Session() as sess:
    start_time = time.time()
    sess.run(init)
    train_writer = tf.summary.FileWriter('Bidirectional_LSTM', sess.graph)
    i = 0
    for epoch in range(training_epochs):

        avg_acc, avg_loss = 0. , 0.
        for step in range(total_batch):

            train_batch_X = train_X_[step*Batch_size : step*Batch_size+Batch_size]
            train_batch_Y = train_Y_[step*Batch_size : step*Batch_size+Batch_size]
            batch_seq_length = seq_length[step*Batch_size : step*Batch_size+Batch_size]
            
            train_batch_X = Zero_padding(train_batch_X, Batch_size, Maxseq_length, Vector_size)
            print(train_batch_Y)
            
            sess.run(optimizer, feed_dict={X: train_batch_X, Y: train_batch_Y, seq_len: batch_seq_length})
            # Compute average loss
            loss_ = sess.run(loss, feed_dict={X: train_batch_X, Y: train_batch_Y, seq_len: batch_seq_length})
            avg_loss += loss_ / total_batch
            
            acc = sess.run(accuracy , feed_dict={X: train_batch_X, Y: train_batch_Y, seq_len: batch_seq_length})
            avg_acc += acc / total_batch
            print("epoch : {:02d} step : {:04d} loss = {:.6f} accuracy= {:.6f}".format(epoch+1, step+1, loss_, acc))

        summary = sess.run(BiLSTM.graph_build(avg_loss, avg_acc))       
        train_writer.add_summary(summary, i)
        i += 1

    duration = time.time() - start_time
    minute = int(duration / 60)
    second = int(duration) % 60
    print("%dminutes %dseconds" % (minute,second))
    save_path = saver.save(sess, os.getcwd())

    train_writer.close()
    print('save_path',save_path)


