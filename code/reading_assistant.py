import re
import os
import sys
import math
from gensimlsi import *

class Document(object):
    def __init__(self, document_id, processed_text):
        """
        Initializes a document
        """
        self.document_id = document_id
        self.processed_text = processed_text  # list of sentences
        self.document_length = sum([len(sentence) for sentence in self.processed_text])


class DocumentProcessor(object):
    """
    A DocumentProcessor broken down an article by whole document, paragraphs, and sentences
    """

    def __init__(self, document_path, level):
        """
        Initializes a document
        """
        self.document_path = document_path
        self.document_id = None
        self.unprocessed_text = None
        self.processed_text = []
        # self.document_length = 0
        self.level = level

        self.docs = []  # a list of Document objects
        self.load_document()
        self.preprocess_document()

    def load_document(self):
        """
        Loads a document given a document path to a text file
        """
        with open(self.document_path, 'r') as f:
            self.unprocessed_text = f.read().split('\n')
            self.document_id = self.document_path.split("/")[-1]
        print('Document ' + self.document_id + " loaded.")

    def preprocess_document(self):
        """
        Preprocesses and stores a document
        Array indexed by paragraph, which are all indexed by sentences
        """
        if self.level == 'document':
            text_by_sentence = " ".join(self.unprocessed_text).split(
                '.')  # <-- adding \n for each sentence is a null-op since you joined then again and split by periods
            processed_sentences = []
            for sentence in text_by_sentence:
                if len(sentence) > 2:
                    processed_sentence = re.sub("[^a-zA-Z -]+", "", sentence.lower().strip())
                    processed_sentence = [w for w in processed_sentence.split(" ") if len(w) > 0]
                    # self.document_length += len(processed_sentence)
                    self.processed_text.append(processed_sentence)
            print('Document ' + self.document_id + ' processed.')

            self.docs = [Document(self.document_id, self.processed_text)]

        elif self.level == 'paragraph':
            for idx, paragraph in enumerate(self.unprocessed_text):
                document_id = self.document_id + '_pg' + str(idx)

                text_by_sentence = paragraph.split('.')
                processed_paragraph = []
                for sentence in text_by_sentence:
                    if len(sentence) > 2:
                        processed_sentence = re.sub("[^a-zA-Z -]+", "", sentence.lower().strip())
                        processed_sentence = [w for w in processed_sentence.split(" ") if len(w) > 0]
                        processed_paragraph.append(processed_sentence)
                print('Paragraph ' + document_id + ' processed.')
                if processed_paragraph:
                    self.docs.append(Document(document_id, processed_paragraph))

    def get_docs(self):
        return self.docs


class InvertedIndex(object):
    """
    The inverted index for all seen documents
    """

    def __init__(self):
        """
        Initializes the inverted index
        """
        self.index = {}
        self.number_of_documents = 0
        self.average_document_length = 0

    def add_document(self, document):
        """
        Adds Document to inverted index
        """
        for sentence in document.processed_text:
            for word in sentence:
                if word in self.index.keys():
                    if document.document_id in self.index[word].keys():
                        self.index[word][document.document_id] += 1
                    else:
                        self.index[word][document.document_id] = 1
                else:
                    self.index[word] = {}
                    self.index[word][document.document_id] = 1
        new_total_length = (self.number_of_documents * self.average_document_length) + document.document_length
        self.number_of_documents += 1
        self.average_document_length = new_total_length / self.number_of_documents
        print('Document ' + document.document_id + ' added to inverted index.')
        print('Current read document count: ' + str(self.number_of_documents))

    def remove_document(self, document):
        """
        Removes Document from inverted index given document id
        """
        for word in self.index.keys():
            if document.document_id in self.index[word].keys():
                del self.index[word][document.document_id]

        new_total_length = (self.number_of_documents * self.average_document_length) - document.document_length
        self.number_of_documents -= 1
        self.average_document_length = new_total_length / self.number_of_documents
        print('Document ' + document.document_id + ' removed from inverted index.')
        print('Current read document count: ' + str(self.number_of_documents))


class ReadingAssistant(object):
    """
    An assistant that finds differences between what a user has and has not read
    """

    def __init__(self, read_documents_path, level):
        """
        Initialize the ReadingAssistant

        Depending on the 'level' parameter, a document could either be the whole wikipeida article,
        a paragraph of the wikipeida article, or a sentence in the wikipeida article 
        """
        self.read_documents_path = read_documents_path
        # list of read documents / paragraphs / sentences
        self.read_document_list = []
        # the inverted index is built based on analysis 'level'. i.e. document level, paragraph level, etc
        self.inv_idx = InvertedIndex()
        # the level at which the reading assistant does its analysis, choose from document|paragraph|sentence
        self.level = level

    def add_document(self, document_path):
        """
        Adds document to read collection, assumes path is to text file
        """
        # split article into documents based on level
        docs = DocumentProcessor(document_path, level=self.level).get_docs()

        for doc in docs:
            # doc.load_document()
            # doc.preprocess_document()
            self.inv_idx.add_document(doc)
            self.read_document_list.append(doc)

    def remove_document(self, document_path):
        """
        Removes document from read collection, assumes path contains id
        """
        doc_id = document_path.split("/")[-1]
        removed_index = None
        for i, doc in enumerate(self.read_document_list):
            if doc.document_id == doc_id:
                self.inv_idx.remove_document(doc)
                removed_index = i
                break
        if removed_index:
            del self.read_document_list[removed_index]

    def load_documents(self):
        """
        Loads all read documents 
        Assumes document path is path to directory containing text files
        """
        for doc_path in os.listdir(self.read_documents_path):
            self.add_document(self.read_documents_path + doc_path)

    def score_document(self, document_path, k1=1.2, b=0.75):
        """
        Scores new document against collection of already-read documents
        Returns list of most-similar and most different documents?
        """
        # new_document = Document(document_path)
        # new_document.load_document()
        # new_document.preprocess_document()
        new_docs = DocumentProcessor(document_path, level=self.level).get_docs()

        rankings = {}
        for new_document in new_docs:
            ranking = []
            for doc in self.read_document_list:
                doc_score = 0
                for sentence in new_document.processed_text:
                    for word in sentence:
                        tf = self.TF_score_helper(word, doc.document_id)
                        idf = self.IDF_score_helper(word)
                        numerator = tf * (k1 + 1)
                        denominator = tf + (
                                    k1 * (1 - b + (b * (doc.document_length / self.inv_idx.average_document_length))))
                        doc_score += idf * (numerator / denominator)
                ranking.append((doc.document_id, doc_score))
            rankings[new_document.document_id] = sorted(ranking, key=lambda x: x[1], reverse=True)

        # sort rankings
        return rankings

    def TF_score_helper(self, keyword, doc_id):
        """
        Given a keyword and doc_id, calculates the term frequency of keyword in document
        """
        tf = 0
        if keyword in self.inv_idx.index.keys():
            if doc_id in self.inv_idx.index[keyword].keys():
                tf = self.inv_idx.index[keyword][doc_id]
        return tf

    def IDF_score_helper(self, keyword):
        """
        Given a keyword, calculates the inverse document frequency
        """
        N = self.inv_idx.number_of_documents
        docs_containing_keyword = 0
        if keyword in self.inv_idx.index.keys():
            docs_containing_keyword = len(self.inv_idx.index[keyword])
        numerator = N - docs_containing_keyword + 0.5
        denominator = docs_containing_keyword + 0.5
        return max(0, math.log((numerator / denominator) + 1))


def print_rankings(method, level, rankings):
    for i in rankings.keys():
        print("---------------------\n")
        print(method, level, "ranking of", str(i))
        print(rankings[i])


def main(arg_level, arg_read_path, arg_unread_doc, arg_k1, arg_b):

    reading_assistant = ReadingAssistant(arg_read_path, level=arg_level)

    reading_assistant.load_documents()

    # BM25 rankings
    rankings = reading_assistant.score_document(arg_unread_doc, k1=arg_k1, b=arg_b)
    print_rankings("BM25", arg_level, rankings)

    # for i in rankings.keys():
    #     print("---------------------\n")
    #     print("[ BM25 ", arg_method, " ranking ] for ", str(i))
    #     print(rankings[i])

    # LSI, but  ranking is only set up for document-level ranking right now
    if arg_level == "document":
        lsi_rankings = gensim_lsi(arg_read_path, arg_unread_doc)
        print_rankings("LSI", arg_level, lsi_rankings)

        # for i in lsi_rankings.keys():
        #     print("---------------------\n")
        #     print("[ LSI ", arg_method, " ranking ] for ", str(i))
        #     print(lsi_rankings[i])


if __name__ == "__main__":
    """
    Run from the command line, specifying level of analysis and path to read and unread documents.
    """

    if len(sys.argv) < 4 or (not sys.argv[1].startswith(("paragraph","document","doc2vec"))):
        print("\nUsage: python reading_assistant.py analysis_method read_docs_path unread_doc_src [k1] [b] \n"
              "    ... analysis_level  : can be 'paragraph' or 'document'\n"
              "    ... read_docs_path  : path containing text files that have been read by the user\n"
              "    ... unread_doc_src  : file that is NOT YET read by the user\n"
              "    ... [k1]            : is the k1 value for BM25. Default: 1.2\n"
              "    ... [b] (optional)  : is the b value for BM25. Default: 0.75\n\n"
              )

    else:
        # tidy up some of the command line args

        # just add trailing "/" if necessary
        arg_read_docs_path = os.path.join(sys.argv[2], '')

        # and set default values for k1 and b
        arg_k1 = 1.2
        arg_b = 0.75
        if len(sys.argv) == 6:
            arg_k1 = sys.argv[4]
            arg_b = sys.argv[5]

        outstr = "\nReading Assistant\n" \
                 "  method: {}\n" \
                 "    read: {}\n" \
                 "  unread: {}\n".format(sys.argv[1], arg_read_docs_path, sys.argv[3])

        if sys.argv[1] == "document" or sys.argv[1] == "paragraph":
            outstr += "      k1: {}\n" \
                      "       b: {}\n".format(arg_k1, arg_b)

        outstr += "\n"

        print (outstr)

        # call main with command line args
        main(sys.argv[1], arg_read_docs_path, sys.argv[3], arg_k1, arg_b)
