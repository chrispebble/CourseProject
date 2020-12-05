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

# contains the names of the read files, for reference later.
read_files = []

class ListOfWords(object):
    def __init__(self, path):
        self.doc = smart_open(path, encoding='latin')
        self.list = []
        for line in self.doc:
            if (len(line.strip()) == 0):
                continue  # skip blank lines
            self.list = self.list + simple_preprocess(remove_stopwords(line), deacc=True)

class ReadTxtFiles(object):
    def __init__(self, dirname):
        self.dirname = dirname

    def __iter__(self):
        for fname in os.listdir(self.dirname):
            read_files.append(fname)
            yield ListOfWords(os.path.join(self.dirname, fname))

class ListOfUnreadWords(object):
    def __init__(self, path):
        self.doc = smart_open(path, encoding='latin')
        self.word_list = []
        for line in self.doc:
            if (len(line.strip()) == 0):
                continue  # skip blank lines
            self.word_list = self.word_list + simple_preprocess(remove_stopwords(line), deacc=True)
        self.name = path.split("/")[-1]

class ReadUnreadTxtFiles(object):
    def __init__(self, fname):
        self.fname = fname

    def __iter__(self):
        # iterator isn't really needed, left over from when this pointed to a directory rather than a file
        # for fname in os.listdir(self.dirname):
        yield ListOfUnreadWords(self.fname)

def gensim_lsi(arg_read_path, arg_unread_file):

    list_of_list_of_words = ReadTxtFiles(arg_read_path)
    list_of_list_of_unread_docs = ReadUnreadTxtFiles(arg_unread_file)

    texts = []
    for doc in list_of_list_of_words:
        texts.append(doc.list)

    # remove words that appear only once
    frequency = defaultdict(int) # defaultdict never raises keyError
    for text in texts:
        for token in text:
            frequency[token] += 1
    texts = [
        [token for token in text if frequency[token] > 1]
        for text in texts
    ]

    dictionary = corpora.Dictionary(texts) # create gensim dictionary structure from words

    corpus = [dictionary.doc2bow(text) for text in texts] # turn all words into the general corpus

    tfidf = models.TfidfModel(corpus)  # initialize a model

    corpus_tfidf = tfidf[corpus]  # use the model to transform vectors

    lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=200)  # initialize an LSI transformation

    index = similarities.MatrixSimilarity(lsi[corpus])  # transform corpus to LSI space and index it

    ### Now we have the model.  We need to query it with the unread documents.

    # this iterates, but for our purposes, this is always just one document...
    for doc in list_of_list_of_unread_docs:
        print("unread document = ", doc.name.upper())

        # create the vectors for the bag of words from all the words in the document
        vec_bow = dictionary.doc2bow(doc.word_list)

        # convert the query to LSI space
        vec_lsi = lsi[vec_bow]

        # perform a similarity query against the corpus
        sims = index[vec_lsi]

        # sort the most similar documents to the top
        sims = sorted(enumerate(sims), key=lambda item: -item[1])

        # create the ranking array
        ranking = []
        for i, doc_score in sims:
            ranking.append((read_files[i], doc_score))

        rankings = {}
        rankings[doc.name] = ranking
        return rankings
