import re

import nltk
from nltk.corpus import stopwords
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

from pymystem3 import Mystem

import gensim

from .models import PostModel


m = Mystem()
nltk.download('stopwords')


def lemmatize(words: list) -> list:
    words_string = ''.join(m.lemmatize(' FGMK '.join(words)))
    words = re.sub(r'[^\w\s]+|[\d]+', '', words_string)
    return [i.strip() for i in set(words.strip().split('FGMK'))]

def get_popular_words(text: str, n=5):
    stop = stopwords.words("russian") + ['это', 'или', "в", 'либо'] + stopwords.words("english") 
    tf = TfidfVectorizer(analyzer='word' , stop_words=stop)
    token_text = tf.fit_transform([text])
    feature_array = np.array(tf.get_feature_names())
    tfidf_sorting = np.argsort(token_text.toarray()).flatten()[::-1]
    return feature_array[tfidf_sorting][:n]

def summarize(text: str, sentences: int) -> str:
    gensim_summary = gensim.summarization.summarize(text)
    return '. '.join(gensim_summary.split('.')[:sentences]) + '.'

def lemmatize_db():
    obs = PostModel.objects.all()
    for ob in obs:
        ob.tags = [i for i in lemmatize(ob.tags) if i]
        print(ob.tags)
        ob.save()