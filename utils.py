import ast
import json
import os
import re
import traceback
from argparse import ArgumentParser

import nltk
import pandas as pd
import requests
from sklearn import (feature_extraction, manifold, model_selection,
                     naive_bayes, pipeline, preprocessing)

import tensorflow as tf
from youtube_transcript_api import YouTubeTranscriptApi

ref = pd.read_csv('yt_label_ref.csv')
yt_label_ref = {k: v for k, v in zip(ref.loc[:, 'Index'], ref.loc[:, 'Vertical1'])}
lst_stopwords = nltk.corpus.stopwords.words("english")


def convert_label(labels):
    if isinstance(labels, str):
        labels = ast.literal_eval(labels)

    converted = list(map(lambda label: yt_label_ref[label], labels))
    return list(set(converted))


def convert_id(yt_8m_id):
    print(yt_8m_id)
    init = yt_8m_id[:2]
    url = f'http://data.yt8m.org/2/j/i/{init}/{yt_8m_id}.js'
    response = requests.get(url)
    print(url)
    if response.status_code != 200:
        return

    data = response.text
    startidx = data.find('(')
    endidx = data.rfind(')')
    y_id = data[startidx + 1:endidx].split(',')[1].replace('"', '')
    print(y_id)
    return y_id


def tfrecord_to_csv(dataset, category):
    count = 0
    temp = []
    csv_path = f'./data/yt8m_in_csv/{category}/{category}_data.csv'

    for data in dataset:
        example = tf.train.Example()
        example.ParseFromString(data.numpy())

        yt_8m_id = example.features.feature['id'].bytes_list.value[0].decode(encoding='UTF-8')
        labels = list(example.features.feature['labels'].int64_list.value)
        # mean_rgb = example.features.feature['mean_rgb'].float_list.value

        info = {
            "yt_8m_id": yt_8m_id,
            "labels": labels,
            # "mean_rgb": mean_rgb,
        }

        temp.append(info)
        count += 1
        print(count)

        if len(temp) % 100 == 0:
            df = pd.DataFrame(temp)
            df.to_csv(csv_path, mode='a', header=False, index=False)
            temp = []

    df = pd.DataFrame(temp)
    df.to_csv(csv_path, mode='a', header=False, index=False)


def get_yt_text(yt_id):
    try:
        return YouTubeTranscriptApi.get_transcript(yt_id, languages=['en'])
    except Exception as e:
        with open('log.txt', 'a') as f:
            f.write(f'{traceback.format_exc()}, {yt_id}\n')


def combine_text(texts):
    if isinstance(texts, str):
        texts = ast.literal_eval(texts)

    return ' '.join([text['text'] for text in texts])


def preprocess_text(text, flg_stemm=False, flg_lemm=True, lst_stopwords=lst_stopwords):
    # Tokenize
    lst_text = nltk.tokenize.word_tokenize(text)

    # Remove non-alphabetic words and transform to lower case
    lst_text = [word.lower().strip() for word in lst_text if word.isalpha()]

    # Remove stopwords
    if lst_stopwords is not None:
        lst_text = [word for word in lst_text if word not in
                    lst_stopwords]

    # Stemming (remove -ing, -ly, ...)
    if flg_stemm:
        ps = nltk.stem.porter.PorterStemmer()
        lst_text = [ps.stem(word) for word in lst_text]

    # Lemmatisation (convert the word into root word)
    if flg_lemm:
        lem = nltk.stem.wordnet.WordNetLemmatizer()
        lst_text = [lem.lemmatize(word) for word in lst_text]

    # back to string from list
    text = " ".join(lst_text)

    return text


def tfidf(corpus):
    vectorizer = feature_extraction.text.TfidfVectorizer(max_features=10000, ngram_range=(1, 2))
    vectorizer.fit(corpus)
    X_train = vectorizer.transform(corpus)
    dic_vocabulary = vectorizer.vocabulary