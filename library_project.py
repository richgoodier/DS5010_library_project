import isbnlib
import nltk
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer
import csv
import ast
import matplotlib.pyplot as plt

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
      #Adds book to library
      self.list.append(book)

    def remove_book(self, book):
      #removes book from library
      self.list.remove(book)

    def search_by_title(self, title):
        # Search for a book by title
        for book in self.list:
            if book.title.lower() == title.lower():
                return book
        return None

    def search_by_quote(self, quote):
        # Search for a book by a quote
        found_books = []
        for book in self.list:
          for page in book.text:
              if quote.lower() in page.lower():
                  found_books.append(book.title)
        return found_books

    def sort_by_author(self):
        # Sorts the books in the library by author
        self.list.sort(key=lambda x: x.authors)

    def export_to_csv(self, filename):
        # Exports the library to a CSV file
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Title', 'Author', 'Genre', 'ISBN'])
            for book in self.list:
                writer.writerow([book.title, ', '.join(book.authors), book.genre, book.isbn])


    def freq_author(self):
      #initializing frequency dictionary
      author_freq = {}

      #for loop that checks each other for each book in library
      for book in self.list:
        author_list = book.authors
        #the book.authors returns authors as indivudal lists, we can fist that by doing another for loop to rechieve the values within those lists
        for writer in author_list:
          author = writer

        #if the author exists in the dictionary then we add 1 to value of freq
          if author in author_freq:
            author_freq[author] += 1
          else:
          #if author does not exists in dictionary (else), then we set the author as 1
            author_freq[author] = 1

      authorname = list(author_freq.keys())
      freq = list(author_freq.values())

      #creating a bar plot
      plt.bar(authorname, freq, color='red')
      plt.xlabel('Author')
      plt.xticks(rotation = 80)
      plt.ylabel('Frequency')
      plt.title('My Library Author Count')
      plt.show()

      #return dictionary
      return author_freq


    def freq_genre(self):

      #initialzie genre frequency dictionary
      genre_freq = {}
      for book in self.list:
        #rechieving value necesary
        genre = book.genre

        #Checking if genre already exists in dictionary, if so add 1
        if genre in genre_freq:
          genre_freq[genre] += 1
        #else is that the genre does not exist in dictionary so we add genre with value of 1
        else:
          genre_freq[genre] = 1

      #retreiving the values in dictionary to use in our visualization
      genre_name = list(genre_freq.keys())
      freq = list(genre_freq.values())

      #creating a bar plot
      plt.bar(genre_name, freq, color='blue')
      plt.xlabel('Genre')
      plt.xticks(rotation = 45, ha='right')
      plt.ylabel('Frequency')
      plt.title('My Library Genre Count')
      plt.show()

    def page_check(self):

      #Creating a dictionary to record our values
      page_check_dict = {}

        #for loop for all books in self.list
      for book in self.list:
        #grabbing values for bookmark and title
        bookmark = book.bookmark
        title = book.title

        #checking if statement for books if they have not started, currently reading, or completed
        if bookmark == 0:
              page_check_dict[title] = 'Not Started'

        #This does not accuratly check read progress due to no page count currently in code
        elif bookmark > 0:
              page_check_dict[title] = 'Reading in Progress'

        #This does not accuratly check completed due to no page count currently in code
        elif bookmark < 0:
              page_check_dict[title] = 'Completed'

      return page_check_dict

    def favorite_book(self, title):
      #Need further discussion on how we want to do this, 0 and 1 for favorite True or False check, in book data?
      book = self.search_by_title(title)
      if book is None:
        return ValueError("No book found")
      else:
        book.set_favorite(1)

    def unfavorite_book(self, title):
      #Need further discussion on how we want to do this, 0 and 1 for favorite True or False check, in book data?
      book = self.search_by_title(title)
      if book is None:
        return ValueError("No book found")
      else:
        book.set_favorite(0)

    def list_favorites(self):
      favorite_books = []
      for book in self.list:
        if book.get_favorite() == 1:
          favorite_books.append(book.title)
      return favorite_books

class Book():
    '''
    Defines a book
    '''
    stopword_list = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()

    def __init__(self, isbn = None,  genre = None, text = None):
        '''Initializes a book'''
        self.isbn = isbn
        self.genre = genre
        self.text = text if text is not None else []
        self.bookmark = 0
        self.favorite = 0
        self.page_count = len(self.text)
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
        if page < self.page_count:
          self.bookmark = page
        else:
          return IndexError("No page found")

    def reset_bookmark(self):
        '''Resets the bookmark to the beginning of the book'''
        self.bookmark = 0

    def get_favorite(self):
        '''Returns the page number of the bookmark'''
        return self.favorite

    def set_favorite(self, number):
        '''Sets the bookmark to a page'''
        self.favorite = number

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

my_library = Library()

books = csv_to_dict('sample_books.csv')
for book in books:
    book_data = Book(book["isbn"], book["genre"], book["text"])
    print(book_data)
    print(book_data.themes(10))
    print(book_data.page_count)
    my_library.add_book(book_data)

print(my_library.search_by_title("The Great Gatsby").get_favorite())
my_library.favorite_book("The Great Gatsby")
print(my_library.search_by_title("The Great Gatsby").get_favorite())

my_library.freq_genre()