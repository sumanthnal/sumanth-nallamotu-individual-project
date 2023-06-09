# -*- coding: utf-8 -*-
"""Zero_Shot.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/158aJ-7gTQzswuNY7z9qLZsONPZlnXB6B
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
from nltk.corpus import wordnet
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from xgboost import XGBClassifier
from keras.models import Sequential
from keras.layers import Dense, LSTM, Embedding, Bidirectional
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score
import tensorflow as tf
!pip install transformers
from transformers import BertTokenizer, TFBertForSequenceClassification
from keras.optimizers import Adam
from keras.losses import BinaryCrossentropy
from keras.metrics import BinaryAccuracy
from keras.callbacks import EarlyStopping

target_encoder = LabelEncoder()

train = pd.read_csv("train_set.csv", index_col=0)
x_train = train.iloc[:,:-1]
y_train = target_encoder.fit_transform(train['type'])

# Load the test data
test = pd.read_csv("test_set.csv", index_col=0)
x_test = test.iloc[:,:-1]
y_test = target_encoder.fit_transform(test['type'])

# Load the val data
val = pd.read_csv("val_set.csv", index_col=0)
x_val = val.iloc[:,:-1]
y_val = target_encoder.fit_transform(val['type'])

from transformers import pipeline
classifier = pipeline("zero-shot-classification")

data = pd.read_csv("mbti_1.csv")

# print(classifier("This is a course about the Transformers library",
#                  candidate_labels=["education", "politics", "business"],))

# classifier("This session is about the machine learning and artifical inteligence",
#            candidate_labels=["education", "politics", "business", "data science"],)

import re
import string
# Preprocess
# Remove URL's
data['posts'] = data['posts'].apply(lambda s: ' '.join(re.sub(r'http\S+', '', s).split()))
# # Remove HTML tags
data['posts'] = data['posts'].apply(lambda s: ' '.join(re.sub(r'<[^>]+>', '', s).split()))

# # Remove punctuations and convert text to lowercase
data['posts'] = data['posts'].apply(lambda s: s.translate(str.maketrans('', '', string.punctuation)).lower())

# # Remove digits
data['posts'] = data['posts'].apply(lambda s: ' '.join(re.sub(r'\d+', '', s).split()))

# # Remove special characters and symbols
data['posts'] = data['posts'].apply(lambda s: ' '.join(re.sub(r'[^\w\s]', '', s).split()))

posts = data['posts']

sample = posts[0]

print(sample)

labels = list(set(data['type'].values))
print(labels)

print(classifier(sample,
                 candidate_labels=labels,))

print(data['type'][0])

response = {'sequence': 'i am speaking gibberish',
            'labels': ['A', 'B', 'C']}

response['labels']

def get_prediction(text):
    response = classifier(text, candidate_labels=labels)
    prediction = response['labels'][0]
    print(prediction)
    return prediction

data['prediction'] = data.apply(lambda row: get_prediction(row.posts), axis=1)

print(data)