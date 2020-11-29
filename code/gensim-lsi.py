import os
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import remove_stopwords
from smart_open import smart_open
from gensim import corpora
from collections import defaultdict
from gensim import models
from gensim import similarities

import logging
# logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

class ListOfWords(object):
    def __init__(self, path):
        self.filepath = path
        self.doc = smart_open(self.filepath, encoding='latin')
        self.id = int(self.doc.readline().strip())
        self.list = []
        for line in self.doc:
            if (len(line.strip())==0):
                continue                                                                    # skip blank lines
            self.list = self.list + simple_preprocess(remove_stopwords(line), deacc=True)

class ReadTxtFiles(object):
    def __init__(self, dirname):
        self.dirname = dirname

    def __iter__(self):
        for fname in os.listdir(self.dirname):
            yield ListOfWords(os.path.join(self.dirname, fname))

path_to_text_directory = "../documents/read"
list_of_list_of_words = ReadTxtFiles(path_to_text_directory)

texts = []
for doc in list_of_list_of_words:
    # print ("-"*70)
    # print(doc.id)
    # print(doc.list)
    texts.append(doc.list)

# remove words that appear only once
frequency = defaultdict(int) #defaultdict never raises keyError
for text in texts:
    for token in text:
        frequency[token] += 1
texts = [
    [token for token in text if frequency[token] > 1]
    for text in texts
]

# print("="*70)
# print(texts)

dictionary = corpora.Dictionary(texts)
corpus = [dictionary.doc2bow(text) for text in texts]

tfidf = models.TfidfModel(corpus)  # initialize a model

corpus_tfidf = tfidf[corpus]  # use the model to transform vectors

lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=200)  # initialize an LSI transformation

index = similarities.MatrixSimilarity(lsi[corpus])  # transform corpus to LSI space and index it

### Now we have the model.  We need to query it with the unread documents.

class ListOfUnreadWords(object):
    def __init__(self, path):
        self.filepath = path
        self.doc = smart_open(self.filepath, encoding='latin')
        self.word_list = []
        for line in self.doc:
            if (len(line.strip()) == 0):
                continue  # skip blank lines
            self.word_list = self.word_list + simple_preprocess(remove_stopwords(line), deacc=True)
        self.name = self.word_list[0]

class ReadUnreadTxtFiles(object):
    def __init__(self, dirname):
        self.dirname = dirname

    def __iter__(self):
        for fname in os.listdir(self.dirname):
            yield ListOfUnreadWords(os.path.join(self.dirname, fname))


path_to_text_directory = "../documents/unread"
list_of_list_of_unread_docs = ReadUnreadTxtFiles(path_to_text_directory)


print("Creating unread document vectors")

unread_doc_v = []

for doc in list_of_list_of_unread_docs:
    print("=-==-" * 14)
    print("[", doc.name.upper(), "]")

    vec_bow = dictionary.doc2bow(doc.word_list)
    vec_lsi = lsi[vec_bow]  # convert the query to LSI space

    # print ("VEC LSI")
    # print(vec_lsi)  # an empy vec_lsi means the words have no overlap!

    sims = index[vec_lsi]  # perform a similarity query against the corpus

    # print("SIMS")
    # print(list(enumerate(sims)))  # print (document_number, document_similarity) 2-tuples

    sims = sorted(enumerate(sims), key=lambda item: -item[1])
    for doc_position, doc_score in sims:
        print(doc_score, texts[doc_position])