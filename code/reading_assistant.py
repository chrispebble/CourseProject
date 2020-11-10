import re
import os


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
        self.number_of_documents += 1
        print('Document ' + document.document_id + ' added to inverted index.')
        print('Current read document count: ' + str(self.number_of_documents))

    def remove_document(self,document_id):
        """
        Removes Document from inverted index given document id
        """
        for word in self.index.keys():
            if document_id in self.index[word].keys():
                del self.index[word][document_id]
        self.number_of_documents -= 1
        print('Document ' + document_id + ' removed from inverted index.')
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
        self.inv_idx.remove_document(doc_id)
        self.read_document_list = [d for d in self.read_document_list if d.document_id != doc_id]

    def load_documents(self):
        """
        Loads all read documents 
        Assumes document path is path to directory containing text files
        """ 
        for doc_path in os.listdir(self.read_documents_path):
            self.add_document(self.read_documents_path + doc_path)
    
    def score_document(self, document_path):
        """
        Scores new document against collection of already-read documents
        Returns list of most-similar and most different documents?
        """
        new_document = Document(document_path)
        new_document.load_document()
        new_document.preprocess_document()
        



def main():
    reading_assistant = ReadingAssistant('../documents/read/')
    reading_assistant.load_documents()
    print(reading_assistant.read_document_list)
    reading_assistant.remove_document('../documents/read/doc1.txt')
    print(reading_assistant.read_document_list)

if __name__ == '__main__':
    main()
