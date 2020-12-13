import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.chunk import conlltags2tree, tree2conlltags
from pprint import pprint
import re
import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm
import requests
import json

nlp = en_core_web_sm.load()


def preprocess(sent):
    sent = nltk.word_tokenize(sent)
    sent = nltk.pos_tag(sent)
    return sent


if __name__ == '__main__':
    # with open('text.txt', 'r', encoding='utf8') as f:
    #     text = f.read().replace('\n', '').split('.')
    #
    # print(text)
    #

    #         doc = nlp(sentence)
    #         pprint([(x.text, x.label_) for x in doc.ents])

    with open('ArticleIds.json', 'r') as f:
        ids = json.load(f)
    i = 0
    for _id in ids:
        response = requests.get('http://eventdata.utdallas.edu/api/article?doc_id=' + _id['_id'])
        test = response.json()['data']
        for sentence in test:
            sentence = preprocess(sentence['sentence'])
            pattern = 'NP: {<DT>?<JJ>*<NN>}'
            cp = nltk.RegexpParser(pattern)
            result = cp.parse(sentence)
            print(result)

            # iob_tagged = tree2conlltags(cs)
            # pprint(iob_tagged)

