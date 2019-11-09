import pandas as pd
import pickle
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Model, load_model
import keras
import tensorflow
import sys
if sys.version_info[0] < 3: 
    from StringIO import StringIO
else:
    from io import StringIO

model = load_model("sage.h5")
with open('tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)
TESTDATA = StringIO("STRING HERE")
data = pd.read_table(TESTDATA, names=('X'))
data['X'] = data['X'].apply((lambda x: re.sub('[^a-zA-z0-9\s]','',x)))
for idx,row in data.iterrows():
    row[0] = row[0].replace('rt',' ')    
data = data.append(data)
tokenizer.fit_on_texts(data['X'].values)
test = tokenizer.texts_to_sequences(data['X'].values)
test = pad_sequences(test, 5014)
print(model.predict(test, batch_size = 2))