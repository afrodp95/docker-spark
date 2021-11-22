import preprocessor as tweet_preprocesor
tweet_preprocesor.set_options(
    tweet_preprocesor.OPT.ESCAPE_CHAR,
    tweet_preprocesor.OPT.URL,
    tweet_preprocesor.OPT.URL)

import nltk
STOPWORDS = nltk.corpus.stopwords.words('english')

import emoji
import re


def clean_text(text,tokenize=False,demojize=True,only_nouns=False):
    data = tweet_preprocesor.clean(text)
    data = re.sub(r'[,!?;-]+', '.', text)
    data = nltk.word_tokenize(data)  # tokenize string to words
    data = [ ch.lower() for ch in data
             if ch.isalpha()
             or ch == '.'
             or emoji.get_emoji_regexp().search(ch)
           ]
    if demojize:
      data = [ emoji.demojize(ch) 
               if emoji.get_emoji_regexp().search(ch)
               else ch
               for ch in data
      ]
    if only_nouns:
      is_noun = lambda pos: pos[:2] in ('NN')
      data = [
              word for (word, post) in 
              nltk.pos_tag(data) if 
              is_noun(post) and
              word not in STOPWORDS
      ]
    if not tokenize:
      data = " ".join(data)
    return data