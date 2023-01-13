import tensorflow as tf
import string
import pandas as pd
import requests
import flask
# In[ ]:


# In[28]:


textdata = open(r"C:\Users\shash\Downloads\poemdata.txt", "r")
data = textdata.readlines()

# In[ ]:


# In[30]:


len(data)

# In[31]:


len(" ".join(data))

# In[32]:


import numpy as np
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Embedding
from tensorflow.keras.preprocessing.sequence import pad_sequences

# In[33]:


token = Tokenizer()
token.fit_on_texts(data)

# In[34]:


encoded = token.texts_to_sequences(data)

# In[35]:


datalist = []
for d in encoded:
    if len(d) > 1:
        for i in range(2, len(d)):
            datalist.append(d[:i])

# In[36]:


max_length = 20
sequences = pad_sequences(datalist, maxlen=max_length, padding='pre')

# In[37]:


x = sequences[:, :-1]

# In[38]:


y = sequences[:, -1]

# In[39]:


y

# In[40]:


vocab_size = len(token.word_counts) + 1

# In[41]:


y = to_categorical(y, num_classes=vocab_size)

# In[42]:


seq_length = x.shape[1]

# In[43]:


model = Sequential()
model.add(Embedding(vocab_size, 50, input_length=seq_length))
model.add(LSTM(100, return_sequences=True))
model.add(LSTM(100))
model.add(Dense(100, activation='relu'))
model.add(Dense(vocab_size, activation='softmax'))

# In[44]:


model.summary()

# In[48]:


model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
model.fit(x, y, epochs=1)

# In[49]:
poetry_length = 10
ftext = []
def poetry(seed_text):
    no_of_lines=10
    for i in range(no_of_lines):
        text = []
        for _ in range(poetry_length):
            enco = token.texts_to_sequences([seed_text])
            enco = pad_sequences(enco, maxlen=seq_length, padding='pre')
            y_pred = np.argmax(model.predict(enco), axis=-1)

            predicted_word = ""
            for word, index in token.word_index.items():
                if (index == y_pred):
                    predicted_word = word
                    break
            seed_text = seed_text + ' ' + predicted_word
            text.append(predicted_word)
        seed_text = text[-1]
        text = ' '.join(text)
        ftext.append(text)
    return ftext
k=str(" \n".join(poetry("happy sad sorrow")))
def iny():
    #f=" \n".join(k)
    return 0
from flask import Flask, render_template, request
app = Flask(__name__,template_folder=r'C:\Users\shash\PycharmProjects\pythonProject1')
@app.route('/')
def index():
   return render_template('index.html')

@app.route('/',methods=['POST'])
def getvalue():
    seed_text=request.form['poem']
    no_of_lines=10
    for i in range(no_of_lines):
        text = []
        for _ in range(poetry_length):
            enco = token.texts_to_sequences([seed_text])
            enco = pad_sequences(enco, maxlen=seq_length, padding='pre')
            y_pred = np.argmax(model.predict(enco), axis=-1)

            predicted_word = ""
            for word, index in token.word_index.items():
                if (index == y_pred):
                    predicted_word = word
                    break
            seed_text = seed_text + ' ' + predicted_word
            text.append(predicted_word)
        seed_text = text[-1]
        text = ' '.join(text)
        ftext.append(text)
    j=" \n".join(ftext)
    return render_template('index.html' , list=k)






if __name__=='__main__':
    app.run(debug=True)