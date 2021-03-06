#!/usr/bin/env python

import sys
import os
from string import punctuation
from typing import Dict, Any, Union

import nltk
import pandas as pd
import pyarrow.parquet as pq

from nltk import word_tokenize
from nltk import TweetTokenizer  # utilizamos el tweet tokenizer.
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

# Decidimos sacar estos caracteres para quedarnos solamente con palabras
chars_to_remove = [',', '.', '!', '(', ')', '/', '^', ':', '...'
    , " ", ",", "*", ". ", "..", "<", "|", ">", "/", "?"
    , '"', "+", "-", ":", "_"
    , "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"
                   ]


def sanitize(tweet):
    a


clean_tweet = remove_stopwords(tweet)
clean_tweet = remove_punctuation(clean_tweet)
clean_tweet = remove_websites(clean_tweet)
return clean_tweet


def stemming(tweet):
    clean_tweet = []
    stemmer = SnowballStemmer("english")
    for word in tweet:
        stemmed = stemmer.stem(word)
        stemmed = stemmed.lstrip("#")
        stemmed = ''.join([c for c in stemmed if c not in set(chars_to_remove)])

        clean_tweet.append(stemmed)
    return clean_tweet


def remove_stopwords(tweet):
    stop_words = stopwords.words('english')
    clean_tweet = [word for word in tweet if word not in stop_words]

    return clean_tweet


def remove_websites(tweet):
    clean_tweet = [word for word in tweet if word[0:4] != "http" and word != ""]
    return clean_tweet


def remove_punctuation(tweet):
    clean_tweet = [word for word in tweet if word not in chars_to_remove]
    return clean_tweet


# noinspection PyUnreachableCode
if __name__ == '__main__':
    # nltk.download('stopwords') SOLO SE NECESITA LA PRIMERA VEZ; por eso lo dejo comentado
    # nltk.download('punkt') SOLO SE NECESITA LA PRIMERA VEZ; por eso lo dejo comentado

    words = {}
    output = sys.argv[2]
    outputfile = open(output, 'w', encoding='utf8')
    brand = 'control'
    file = 'tweets_{0}.parquet'.format(str(sys.argv[1]))
    clean_words = []
    tweet_token = []
    if len(sys.argv) == 4:
        brand = sys.argv[3]
        # for inputfile in os.listdir(sys.argv[1]):
    df = pq.read_pandas(file).to_pandas()
    df = df.reset_index()

    for i in range(1, df.last_valid_index()):
        # print(df['text'][i])
        tTokenizer = TweetTokenizer(preserve_case=False, reduce_len=True, strip_handles=True)
        tweet = tTokenizer.tokenize(df['text'][i])

        clean_words = sanitize(tweet)  # envío a la función sanitize para sacar stop words y puntuación
        stemmed_words = stemming(clean_words)
        print(stemmed_words)

        for word in stemmed_words:
            if word not in words:
                words[word] = 1
            else:
                words[word] = words[word] + 1
    # store relevant info in words map

    for key, count in words.items():
        outputfile.write(key + "\t" + brand + "\t" + str(count) + "\n")
    outputfile.close()
