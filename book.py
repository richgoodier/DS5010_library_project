import isbnlib
import nltk
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer
import csv
import ast

nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')

class Library():
    def __init__(self):
        self.list = []
    
    def list_titles(self):
        for book in self.list:
            print(book.title)
    
    def add_book(self, book):
        self.list.append(book)


class Book():
    '''
    Defines a book
    '''
    stopword_list = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()

    def __init__(self, isbn = None,  genre = None, text = None, bookmark = 0):
        '''Initializes a book'''
        self.isbn = isbn
        self.genre = genre
        self.text = text if text is not None else []
        self.bookmark = bookmark
        self.word_count = self.count_words()
        book_info = self.get_book_info()
        if book_info == 'Invalid ISBN':
            raise ValueError(book_info)
        else:
            self.title, self.authors, self.publisher, self.year = book_info    

    def __str__(self):
        '''Returns basic info of the book.'''
        return f"Title: {self.title} Author: {self.authors[0]} Genre: {self.genre}"
    
    def __len__(self):
        '''Returns the number of pages'''
        return len(self.text)
    
    def get_book_info(self):
        try:
            #Get book information
            book = isbnlib.meta(self.isbn)
            
            # Extract title from book information
            title = book.get('Title', 'Title not found')
            authors = book.get('Authors', 'Author not found')
            publisher = book.get('Publisher', 'Publisher not found')
            year = book.get('Year', 'Year not found')
            return (title, authors, publisher, year)
        except isbnlib._exceptions.NotValidISBNError:
            return 'Invalid ISBN'
    
    def get_bookmark(self):
        '''Returns the page number of the bookmark'''
        return self.bookmark
    
    def set_bookmark(self, page):
        '''Sets the bookmark to a page'''
        self.bookmark = page
    
    def reset_bookmark(self):
        '''Resets the bookmark to the beginning of the book'''
        self.bookmark = 0

    def search_text(self, quotation):
        pages_found = []
        for i in range(len(self.text)):
            if quotation in self.text[i]:
                pages_found.append(i)
        if pages_found == []:
            return None
        else:
            return pages_found
        
    @staticmethod
    def get_wordnet_pos(treebank_tag):
        '''
        Map treebank POS tag to first character used by WordNetLemmatizer
        '''
        tag = {
            'J': wordnet.ADJ,
            'V': wordnet.VERB,
            'N': wordnet.NOUN,
            'R': wordnet.ADV
        }.get(treebank_tag[0], wordnet.NOUN)  # Default to noun

        return tag
    
    def tokenize(self, page):
        '''
        Creates a list of tokens from a string
        param page: a string to calculate tokens
        returns: a list y of all tokens contained in string page
        '''
        words = page.split()

        tokens_with_pos = nltk.pos_tag(words)

        y = []
        for word, pos in tokens_with_pos:
            new_word = "".join([char.lower() for char in word if char.isalnum()])
            lemmatized_word = self.lemmatizer.lemmatize(new_word, pos=Book.get_wordnet_pos(pos))
            if lemmatized_word == "wa": # debugging
                print(word + ":" + new_word)
            if lemmatized_word not in self.stopword_list:
                y.append(lemmatized_word)
        return y

    def count_words(self):
        '''
        Creates a dictionary  with keys from the tokens of a string and values representing the count for that token
        param s: a string to calculate tokens
        returns: a dictionary word_count of tokens and their counts
        '''
        words = []
        for page in self.text:
            words.extend(self.tokenize(page))
        
        word_count = {}
        for word in words:
            if word in word_count:
                word_count[word] += 1
            else:
                word_count[word] = 1
        
        return word_count
    
    def themes(self, theme_count = 5):
        sorted_words = sorted(self.word_count.items(), key=lambda item: item[1], reverse=True)
        theme_words = []
        for word in sorted_words:
            theme_words.append(word[0])
            theme_count -= 1
            if theme_count == 0:
                return theme_words


def csv_to_dict(csv_file):
    books_dict = []
    with open(csv_file, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            book = {
                "isbn": row[0],
                "genre": row[1],
                "text": ast.literal_eval(row[2])
            }
            books_dict.append(book)
    return books_dict


my_libary = Library()

books = csv_to_dict('sample_books.csv')
for book in books:
    book_data = Book(book["isbn"], book["genre"], book["text"])
    print(book_data)
    print(book_data.themes(10))
    my_libary.add_book(book_data)

my_libary.list_titles()
