import nltk
import json
import Graph
import string
import requests
import en_core_web_sm
import KeyWordExtraction
from pathlib import Path
from jsondiff import diff
from pprint import pprint
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

nlp = en_core_web_sm.load()
lemmatizer = WordNetLemmatizer()


def preprocess(sent):
    sent = nltk.word_tokenize(sent)
    sent = nltk.pos_tag(sent)
    return sent


def parseSentence(data):
    data = nltk.word_tokenize(data)
    data = nltk.pos_tag(data)
    cp = nltk.RegexpParser('NP: {<DT>?<JJ>*<NN>}')
    return cp.parse(data)


def simplifyNLTKResult(data):
    result2 = []
    for x in data:
        if type(x) is tuple:
            result2.append(x)
        else:
            for y in x:
                result2.append(y)
    return [idx for idx in result2 if not any(punc in idx for punc in string.punctuation)]


def simplifyStandfordResult(data):
    pre_tuple_form = []
    result3 = []
    for x in range(len(data['parse_sentence'])):
        if data['parse_sentence'][x] == '(':
            newWord = ''
            is_in_parentheses = True
        else:
            is_in_parentheses = False
        while is_in_parentheses:
            newWord += data['parse_sentence'][x]
            x += 1
            if data['parse_sentence'][x] == ')':
                is_in_parentheses = False
                pre_tuple_form.append((newWord + ')').replace(' ', ','))
            elif data['parse_sentence'][x] == '(':
                is_in_parentheses = False
    for z in pre_tuple_form:
        word_and_POS = z.replace('(', '').replace(')', '').split(',')
        finalTuple = (word_and_POS[1], word_and_POS[0])
        result3.append(finalTuple)
    return [idx for idx in result3 if not any(punc in idx for punc in string.punctuation)]


def Diff(li1, li2):
    li_dif = [i for i in li1 + li2 if i not in li1 or i not in li2]
    return li_dif


def CompareSentences(sentenceData):
    postProcess = preprocess(sentenceData['sentence'])
    pattern = 'NP: {<DT>?<JJ>*<NN>}'
    cp = nltk.RegexpParser(pattern)
    result = cp.parse(postProcess)
    nltkResult = dict(simplifyNLTKResult(result))
    stanfordResult = dict(simplifyStandfordResult(sentenceData))
    resultDiff = [{k: v} for k, v in dict(diff(nltkResult, stanfordResult, syntax='symmetric')).items()]
    resultDiff = resultDiff[: len(resultDiff) - 2]
    return resultDiff


def SaveToFile(file, data):
    my_file = Path(file)
    if my_file.is_file():
        # This works so I won't touch it.
        with open(file, 'r') as f1:
            oldData = json.load(f1)
        with open(file, 'w') as f1:
            newData = oldData + data
            json.dump(newData, f1, indent=4)
    else:
        with open(file, 'w') as f1:
            json.dump(data, f1, indent=4)


def FilterSentence(sentenceData):
    stop_words = set(stopwords.words('english'))
    text = sentenceData['sentence']
    tokens = word_tokenize(text)
    tokens = [w.lower() for w in tokens]
    table = str.maketrans('', '', string.punctuation)
    stripped = [w.translate(table) for w in tokens]
    words = [word for word in stripped if word.isalpha()]
    words = [lemmatizer.lemmatize(w) for w in words if w not in stop_words]
    return words


if __name__ == '__main__':
    tr4w = KeyWordExtraction.TextRank4Keyword()

    with open('ArticleIds.json', 'r') as f:
        article_ids = json.load(f)
    for _id in article_ids:
        response = requests.get('http://149.165.156.117/api/article?doc_id=' + _id['_id'])
        articleData = response.json()['data']
        article_graph = Graph.Graph(2)
        articleText = []

        for rawSentence in articleData:
            fileName = f"{_id['_id']}.json"

            sentence_graph = Graph.Graph(2)
            filteredWords = FilterSentence(rawSentence)

            sentence_graph.CreateGraph(filteredWords)
            article_graph.MergeGraphs(sentence_graph)
            # print(filteredWords)
            # pprint(sentence_graph.GetGraph())
            '''
            Uncomment to find the differences of the standford corenlp and NLTK package on the sentences
            nlpDiff = CompareSentences(rawSentence)
            SaveToFile(fileName, nlpDiff)
            '''
            '''
            Uncomment to find the keywords in the sentence
            tr4w.analyze(rawSentence['sentence'], candidate_pos=['NOUN', 'PROPN'], window_size=4, lower=False)
            test = [{k: v} for k, v in dict(tr4w.get_keywords(10)).items()]
            SaveToFile(fileName, test)
            '''
        pprint(article_graph.GetGraph())
        break
