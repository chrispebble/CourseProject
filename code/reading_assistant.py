import re
import os
import math

class Document(object):
    """
    A document data structure broken down by whole document, paragraphs, and sentences
    """
    def __init__(self, document_path):
        """
        Initializes a document
        """
        self.document_path = document_path
        self.document_id = None
        self.unprocessed_text = None
        self.processed_text = []
        self.document_length = 0

    def load_document(self):
        """
        Loads a document given a document path to a text file
        """
        with open(self.document_path,'r') as f:
            self.unprocessed_text = f.read().split('\n')
            self.document_id = self.document_path.split("/")[-1]
        print('Document ' + self.document_id + " loaded.")
    def preprocess_document(self):
        """
        Preprocesses and stores a document
        Array indexed by paragraph, which are all indexed by sentences
        """
        text_by_sentence = " ".join(self.unprocessed_text).split('.')
        processed_sentences = []
        for sentence in text_by_sentence:
            if len(sentence) > 2:
                processed_sentence = re.sub("[^a-zA-Z -]+","",sentence.lower().strip())
                processed_sentence = [w for w in processed_sentence.split(" ") if len(w) > 0]
                self.document_length += len(processed_sentence)
                self.processed_text.append(processed_sentence)
        print('Document ' + self.document_id + ' processed.')
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

    def add_document(self,document):
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

    def remove_document(self,document):
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
    def __init__(self,read_documents_path):
        """
        Initialize the ReadingAssistant
        """
        self.read_documents_path = read_documents_path
        
        self.read_document_list = []
        self.inv_idx = InvertedIndex()

    def add_document(self,document_path):
        """
        Adds document to read collection, assumes path is to text file
        """
        doc = Document(document_path)
        doc.load_document()
        doc.preprocess_document()
        self.inv_idx.add_document(doc)
        self.read_document_list.append(doc)

    def remove_document(self,document_path):
        """
        Removes document from read collection, assumes path contains id
        """
        doc_id = document_path.split("/")[-1]
        removed_index = None
        for i,doc in enumerate(self.read_document_list):
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
        new_document = Document(document_path)
        new_document.load_document()
        new_document.preprocess_document()
        
        ranking = []
        for doc in self.read_document_list:
            doc_score = 0
            for sentence in new_document.processed_text:
                for word in sentence:
                    tf = self.TF_score_helper(word,doc.document_id)           
                    idf = self.IDF_score_helper(word)
                    numerator = tf * (k1 + 1)
                    denominator = tf + (k1 * (1 - b + (b * (doc.document_length / self.inv_idx.average_document_length))))
                    doc_score += idf * (numerator / denominator)
            ranking.append((doc.document_id, doc_score))
        return ranking


    def TF_score_helper(self,keyword,doc_id):
        """
        Given a keyword and doc_id, calculates the term frequency of keyword in document
        """
        tf = 0
        if keyword in self.inv_idx.index.keys():
            if doc_id in self.inv_idx.index[keyword].keys():
                tf = self.inv_idx.index[keyword][doc_id]
        return tf        


    def IDF_score_helper(self,keyword):
        """
        Given a keyword, calculates the inverse document frequency
        """ 
        N = self.inv_idx.number_of_documents
        docs_containing_keyword = 0
        if keyword in self.inv_idx.index.keys():
            docs_containing_keyword = len(self.inv_idx.index[keyword])
        numerator = N - docs_containing_keyword + 0.5
        denominator = docs_containing_keyword + 0.5
        return max(0,math.log((numerator/denominator) + 1))


def main():
    reading_assistant = ReadingAssistant('../documents/read/')
    reading_assistant.load_documents()
    print(reading_assistant.score_document('../documents/unread/basketball.txt'))
    reading_assistant.remove_document('../documents/read/baseball.txt')
    print(reading_assistant.score_document('../documents/unread/basketball.txt'))  



if __name__ == '__main__':
    main()
