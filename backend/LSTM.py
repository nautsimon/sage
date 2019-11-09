import pandas as pd
import os
import collections
import re
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.layers import LSTM, Conv2D, Embedding, Dense
from keras.models import Model, Sequential
from keras.optimizers import Adam

def load_data(inputDir):
	trainingPath = os.path.join(inputDir, "train.csv")
	df = pd.read_csv(trainingPath)
	data = df.dropna()
	data['Body'] = data['Body'].apply((lambda x: re.sub('[^a-zA-z0-9\s]','',x)))
	labels = data['Label']
	
	tokenizer = Tokenizer(nb_words = 50000, lower = True, split = ' ')
	tokenizer.fit_on_texts(data['Body'].values)
	train_data = tokenizer.texts_to_sequences(data['Body'])
	train_data = pad_sequences(train_data)
	return train_data, labels

def build_model(train_data):
	model = Sequential()
	model.add(Embedding(50000, 128, input_length = train_data.shape[1]))
	model.add(LSTM(100, dropout=0.2))
	model.add(Dense(1, activation = 'sigmoid'))
	return model

train_data, labels = load_data("./train_data/")
print(labels)
model = build_model(train_data)
optimizer = Adam(.01, .5)
model.compile(optimizer, loss = 'binary_crossentropy', metrics = ['accuracy'])
model.fit(train_data, labels, batch_size = 32, epochs = 10)