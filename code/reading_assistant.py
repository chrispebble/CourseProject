import re

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
        Assumes first line is unique ID, rest of lines are document
        """
        with open(self.document_path,'r') as f:
            lines = f.read().split('\n')
            self.document_id = lines[0]
            self.unprocessed_text = lines[1:]

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

class InvertedIndex(object):
    """
    The inverted index for all seen documents
    """
    def __init__(self):
        """
        Initializes the inverted index
        """
        self.index = {}

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

    def remove_document(self,document_id):
        """
        Removes Document from inverted index given document id
        """
        pass

class ReadingAssistant(object):
    """
    An assistant that finds differences between what a user has and has not read
    """
    def __init__(self,read_document_path):
        """
        Initialize the ReadingAssistant
        """
        self.read_documents_path = read_documents_path
        
        self.read_documents = []

    def add_document(self,document_path):
        """
        Adds document to read collection, assumes path is to text file
        """
        pass
    def load_documents(self):
        """
        Loads all read documents 
        Assumes document path is path to directory containing text files
        """ 

        pass
    
    def score_document(self):
        pass



def main():
    d1 = Document("../documents/read/doc1.txt")
    d2 = Document("../documents/read/doc2.txt")
    d3 = Document("../documents/read/doc3.txt")
    inv_idx = InvertedIndex()
    
    for d in [d1,d2,d3]:
        d.load_document()
        d.preprocess_document()
        inv_idx.add_document(d)

    
    print(inv_idx.index)

if __name__ == '__main__':
    main()
