import pandas as pd
import pickle
import os
import re
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.layers import CuDNNLSTM, Conv1D, Embedding, Dense, Dropout, MaxPooling1D, Bidirectional
from keras.models import Model, Sequential, load_model
from keras.optimizers import Adam
from sklearn.model_selection import train_test_split
import keras
import tensorflow 
import tensorflow as tf

os.environ["CUDA_VISIBLE_DEVICES"]="0,1,2,3"

# Loads data from a .csv file
def load_data(inputDir):
	# Read and clean data
    trainingPath = os.path.join(inputDir, "train_data_shuffled.csv")
    df = pd.read_csv(trainingPath, index_col=0)
    data = df.dropna()
    data['Body'] = data['Body'].apply((lambda x: re.sub('[^a-zA-z0-9\s]','',str(x))))
    for idx,row in data.iterrows():
        row[0] = row[0].replace('rt',' ')    

    # Assign numerical values to words
    tokenizer = Tokenizer(nb_words = 10000, lower = True, split = ' ')
    tokenizer.fit_on_texts(data['Body'].values)

    # Save tokenizer for later use
    with open('tokenizer.pickle', 'wb') as handle:
        pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)
    with open('tokenizer.pickle', 'rb') as handle:
        loaded_tokenizer = pickle.load(handle)

    # Assemble trianing data and pad all to same length
    train_data = tokenizer.texts_to_sequences(data['Body'].values)
    train_data = pad_sequences(train_data, 6000)
    return train_data, data['Label'].values

# Builds LSTM model, uses CuDNNLSTM for GPU optimization
def build_model(train_data):
    model = Sequential()
    model.add(Embedding(10000, 128, input_length = 6000))
    model.add(Dropout(0.7))
    model.add(Bidirectional(CuDNNLSTM(100, input_shape=(10000, 128))))
    model.add(Dropout(0.7))
    model.add(Dense(1, activation = 'sigmoid'))
    return model

# Load and split training data
train_data, labels = load_data("./train_data/")
X_train, X_test, y_train, y_test = train_test_split(train_data, labels, test_size=0.10)

# Build and train model
model = build_model(train_data)
multi_model = keras.utils.multi_gpu_model(model, gpus = 4)
optimizer = Adam(.01, .5)
multi_model.compile(optimizer, loss = 'binary_crossentropy', metrics = ['accuracy'])
multi_model.fit(X_train, y_train, epochs = 4, batch_size = 256, validation_split=0.03)

# Test model and save: one for further training and one to assemble for use in non-GPU environment
print(multi_model.evaluate(X_test, y_test))
multi_model.save("sage.h5")
model.save_weights("weights.h5")





