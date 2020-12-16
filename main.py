import nltk
import en_core_web_sm
import requests
import json
from jsondiff import diff
import string

nlp = en_core_web_sm.load()


def preprocess(sent):
    sent = nltk.word_tokenize(sent)
    sent = nltk.pos_tag(sent)
    return sent


def Diff(li1, li2):
    li_dif = [i for i in li1 + li2 if i not in li1 or i not in li2]
    return li_dif


if __name__ == '__main__':
    with open('ArticleIds.json', 'r') as f:
        article_ids = json.load(f)
    for _id in article_ids:
        response = requests.get('http://eventdata.utdallas.edu/api/article?doc_id=' + _id['_id'])
        data = response.json()['data']
        nltkResult = []
        stanfordResult = []

        for sentence in data:
            pre_tuple_form = []
            sentence2 = preprocess(sentence['sentence'])
            pattern = 'NP: {<DT>?<JJ>*<NN>}'
            cp = nltk.RegexpParser(pattern)
            result = cp.parse(sentence2)

            for x in result:
                if type(x) is tuple:
                    stanfordResult.append(x)
                else:
                    for y in x:
                        stanfordResult.append(y)

            # The data from the stanford corenlp is in string so I have to convert it into a tuple.
            for x in range(len(sentence['parse_sentence'])):
                if sentence['parse_sentence'][x] == '(':
                    newWord = ''
                    is_in_parentheses = True
                else:
                    is_in_parentheses = False
                while is_in_parentheses:
                    newWord += sentence['parse_sentence'][x]
                    x += 1
                    if sentence['parse_sentence'][x] == ')':
                        is_in_parentheses = False
                        pre_tuple_form.append((newWord + ')').replace(' ', ','))
                    elif sentence['parse_sentence'][x] == '(':
                        is_in_parentheses = False
            for z in pre_tuple_form:
                word_and_POS = z.replace('(', '').replace(')', '').split(',')
                finalTuple = (word_and_POS[1], word_and_POS[0])
                nltkResult.append(finalTuple)

            stanfordResult = [idx for idx in stanfordResult if not any(punc in idx for punc in string.punctuation)]
            nltkResult = [idx for idx in nltkResult if not any(punc in idx for punc in string.punctuation)]
            with open(f"{_id['_id']}.json", 'w') as f1:
                newFile = False
                try:
                    oldData = json.load(f1)
                except:
                    newFile = True
                parsed1 = dict(stanfordResult)
                parsed2 = dict(nltkResult)
                nlpDiff = [{k: v} for k, v in dict(diff(parsed1, parsed2, syntax='symmetric')).items()]
                nlpDiff = nlpDiff[: len(nlpDiff) - 2]
                if newFile:
                    json.dump(nlpDiff, f1, indent=4)
                else:
                    oldData.update(nlpDiff)
                    json.dump(oldData, f1, indent=4)
