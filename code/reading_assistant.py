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
        self.processed_text = None

    def load_document(self):
        """
        Loads a document given a document path to a text file
        Assumes first line is unique ID, rest of lines are document
        """
        pass

    def preprocess_document(self):
        """
        Preprocesses and stores a document
        Array indexed by paragraph, which are all indexed by sentences
        """
        pass

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
        pass
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
    #run the program
    pass

if __name__ == '__main__':
    main()
