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
        """
        Prints the titles of all books loaded.
        """
        for book in self.list:
            print(book.title)

    def add_book(self, book):
        """
        Adds book to self.list for our library
        param book: the book data provided to the function
        return none
        """
        self.list.append(book)

    def remove_book(self, title):
        """
        Removes book from the list of the library
        parm title: the user inputs title of the book that they want to remove
        return: none
        value error: if book is not found with the title provided, we return No book found
        """
        
        book = self.search_by_title(title)
        print(book)
        if book is None:
            return ValueError("No book found")
        else:
            #removes the book from list
            self.list.remove(book)

    def search_by_title(self, title):
        """
        Search for a book by its title.

        Args:
        - title (str): The title of the book to search for. Case-insensitive.

        Returns:
        - Book or None: If a book with the specified title is found, the function returns
                       the Book object. If not found, returns None.
        """
        # Search for a book by title
        for book in self.list:
            if book.title.lower() == title.lower():
                return book
        return None

    def search_by_quote(self, quote):
        """
        Search for books containing a specific quote within their text.

        Args:
        - quote (str): The quote to search for within the book texts. Case-insensitive.

        Returns:
        - list: A list containing titles of books that contain the specified quote in their text.
        """

        # Search for a book by a quote
        found_books = []
        for book in self.list:
          for page in book.text:
              if quote.lower() in page.lower():
                  found_books.append(book.title)
        return found_books

    def sort_by_author(self):
        """
        Sorts the books in the library by the primary author's name.

        This method sorts the list of books in the library based on the primary author's name.
        It uses the first author's name for sorting purposes (assuming authors[0] represents the primary author).
        """
        # Sorts the books in the library by author
        self.list.sort(key=lambda book: book.authors[0])

    def export_to_csv(self, filename):
        """
        Exports the library content to a CSV file.

        Args:
        - filename (str): The name of the file to which the library content will be exported.

        The function exports the library content, including book titles, authors, genres, and ISBNs,
        into a CSV file with the specified filename. Each row in the CSV represents a book,
        with columns for 'Title', 'Author', 'Genre', and 'ISBN'.
        """
        # Exports the library to a CSV file
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Title', 'Author', 'Genre', 'ISBN'])
            for book in self.list:
                writer.writerow([book.title, ', '.join(book.authors), book.genre, book.isbn])


    def freq_author(self):
        """
        Tracks the times an author exists within the library and creates a
        visualization of it (bar chart)

        param self

        return author_freq: The dictionary used for the visualization

        """
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

        return author_freq


    def freq_genre(self):
        """
        Tracks the times a genre exists within the library and creates a
        visualization of it (bar chart)

        param self

        return genre_freq: The dictionary used for the visualization

        """

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

        return genre_freq

    def progress_check(self):
        """
        Checks the progress of each book and creates a dictionary of the books,
        with the key being the title of the book and the value being the progress
        (Not started, Completed, and reading in progress)

        param self:

        return page_check_dict: the dictionary with the title and progress of book
        """

        #Creating a dictionary to record our values
        page_check_dict = {}

            #for loop for all books in self.list
        for book in self.list:
            #grabbing values for bookmark and title
            bookmark = book.get_bookmark()
            title = book.title

            #checking if statement for books if they have not started, currently reading, or completed
            if bookmark == 0:
                page_check_dict[title] = 'Not Started'

            #if bookmark is equal to the pagecount of the book, then that would mean it is completed
            elif bookmark == book.page_count - 1:
                page_check_dict[title] = 'Completed'

            #if the bookmark is greater then 0 then that means that the book is currently in progress of being read
            elif bookmark > 0:
                page_check_dict[title] = 'Reading in Progress'

        return page_check_dict

    def favorite_book(self, title):
        """
        sets the recieved book as a favorite, sets the favorite value to 1

        param title: the title of the book

        return none
        """
        #Sets book to 1 to indicate that it is a favorite book
        book = self.search_by_title(title)
        if book is None:
            return ValueError("No book found")
        else:
            book.set_favorite(1)

    def unfavorite_book(self, title):
        """
        sets the recieved book as not a favorite (or unfavorites the book), sets the favorite value to 0

        param title: the title of the book

        return none
        """
        #Unfavorite book, set the favorite value to 0 to indicate that it is not a favorite
        book = self.search_by_title(title)
        if book is None:
            return ValueError("No book found")
        else:
            book.set_favorite(0)

    def list_favorites(self):
        """
        checks through all books in list and only grabs the favorited books (favorite value == 1)
        to create a list of all favorite books

        param self

        return favorite_books: list of all favorite books
        """
        favorite_books = []
        for book in self.list:
            if book.get_favorite() == 1:
                favorite_books.append(book.title)
        return favorite_books

class Book():
    '''
    Represents a book with attributes like ISBN, genre, text, and more.
    It provides functionalities such as fetching book information using ISBN,
    managing reading progress, and analyzing the text for themes and word frequencies.
    '''
    stopword_list = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()

    def __init__(self, isbn,  genre = None, text = None):
        '''
        Initializes a new instance of the Book class.

        Args:
            isbn (str): The ISBN number of the book.
            genre (str, optional): The genre of the book.
            text (list of str, optional): The text content of the book, split into a list of pages.

        Raises:
            TypeError: If the ISBN is not provided.
            ValueError: If provided ISBN is invalid.
        '''
        if isbn is None:
          raise TypeError("ISBN number is required before proceeding.")
        else:
          self.isbn = isbn
        self.genre = genre
        self.text = text if text is not None else []
        book_info = self.get_book_info()
        if book_info == 'Invalid ISBN':
            raise ValueError(book_info)
        else:
            self.title, self.authors, self.publisher, self.year = book_info
        self._bookmark = 0
        self._favorite = 0
        self.page_count = len(self.text)
        self.word_count = self.count_words()
        self.word_dict = self.tally_words()

    def __str__(self):
        '''
        Returns a string representation of the book, including title, author, and genre.

        Returns:
            str: A string representation of the book.
        '''
        return f"Title: {self.title} Author: {self.authors[0]} Genre: {self.genre}"

    def __len__(self):
        '''
        Returns the total number of pages in the book.

        Returns:
            int: The total number of pages.
        '''
        return len(self.text)

    def get_book_info(self):
        '''
        Fetches and returns detailed information about the book using its ISBN.

        Returns:
            tuple: A tuple containing the title, authors, publisher, and year of the book.
            str: 'Invalid ISBN' if the ISBN is not valid.

        Raises:
            isbnlib._exceptions.NotValidISBNError: If the ISBN is not valid.
        '''
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
        '''
        Retrieves the current bookmark page number.

        Returns:
            int: The page number where the bookmark is set.
        '''
        return self._bookmark

    def set_bookmark(self, page):
        '''
        Sets the bookmark to a specified page number.

        Args:
            page (int): The page number to set the bookmark.

        Returns:
            IndexError: If the specified page number is beyond the book's length.
        '''
        if page < self.page_count:
          self._bookmark = page
        else:
          raise IndexError(f"Page {page} is out of bounds. The book's pages go from 0 to {self.page_count - 1}.")

    def reset_bookmark(self):
        '''Resets the bookmark to the beginning of the book'''
        self._bookmark = 0

    def get_favorite(self):
        '''
        Checks whether the book is marked as favorite.

        Returns:
            int: The favorite status (0 for not favorite, 1 for favorite).
        '''
        return self._favorite

    def set_favorite(self, number):
        '''
        Sets the favorite status of the book to favorite (1) or not favorite (0).

        Args:
            number (int): The value to set the favorite status (0 or 1).
        '''
        self._favorite = number

    def search_text(self, quotation):
        '''
        Searches for a given quotation in the book's text.

        Args:
            quotation (str): The quotation to search for.

        Returns:
            list of int: A list of page numbers where the quotation is found, or None if not found.
        '''
        pages_found = []
        for i in range(len(self.text)):
            if quotation in self.text[i]:
                pages_found.append(i)
        return pages_found

    @staticmethod
    def get_wordnet_pos(treebank_tag):
        '''
        Maps a POS (Part-Of-Speech) tag from the Penn Treebank project to a format recognized by the WordNetLemmatizer.

        This method simplifies the conversion of tags like 'NN', 'VB', 'JJ', and 'RB' to their corresponding
        simple WordNet POS tags: NOUN, VERB, ADJ, and ADV respectively.

        Args:
            treebank_tag (str): A POS tag from the Penn Treebank tagset.

        Returns:
            str: A simplified POS tag compatible with the WordNetLemmatizer.
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
        Tokenizes the given text page into words, excluding stopwords.

        Args:
            page (str): The text of the page to tokenize.

        Returns:
            list of str: A list of tokenized words.
        '''
        words = page.split()

        '''
        The following step is necessary to prevent the lemmatizer from making mistakes
        like considering 'was' a noun and removing the 's' in order to singularize it.
        '''
        tokens_with_pos = nltk.pos_tag(words)

        y = []
        for word, pos in tokens_with_pos:
            new_word = "".join([char.lower() for char in word if char.isalnum()])
            lemmatized_word = self.lemmatizer.lemmatize(new_word, pos=Book.get_wordnet_pos(pos))
            if lemmatized_word not in self.stopword_list:
                y.append(lemmatized_word)
        return y

    def tally_words(self):
        '''
        Counts the frequency of each word in the book's text.

        Returns:
            dict: A dictionary mapping words to their frequency counts.
        '''
        words = []
        for page in self.text:
            words.extend(self.tokenize(page))

        word_tally = {}
        for word in words:
            if word in word_tally:
                word_tally[word] += 1
            else:
                word_tally[word] = 1

        return word_tally

    def count_words(self):
      '''
      Counts the total number of words in the text of the book.

      This method iterates through each page in the book's text, splitting the page into words based on spaces,
      and then sums up the count of words across all pages.

      Returns:
          int: The total number of words in the book's text.
      '''
      word_count = 0
      for page in self.text:
        words = page.split()
        word_count += len(words)
      return word_count

    def themes(self, theme_count = 5):
        '''
        Identifies the most frequent themes (words) in the book.

        Args:
            theme_count (int, optional): The number of themes to identify. Defaults to 5.

        Returns:
            list of str: A list of the most frequent words in the book.
        '''
        sorted_words = sorted(self.word_dict.items(), key=lambda item: item[1], reverse=True)
        theme_words = []
        for word in sorted_words:
            theme_words.append(word[0])
            theme_count -= 1
            if theme_count == 0:
                return theme_words

def csv_to_dict(csv_file):
    '''
    Converts a CSV file into a list of dictionaries, each representing a book.

    This function reads a CSV file where each row represents a book. It expects each row to have 
    at least three fields: ISBN, genre, and text. The 'text' field should be a string representation
    of a list, which is converted back into a list using `ast.literal_eval`.

    Args:
        csv_file (str): The path to the CSV file to be read.

    Returns:
        list of dict: A list where each dictionary contains the details of a book. Each dictionary 
                      has keys 'isbn', 'genre', and 'text', corresponding to the values in each row of the CSV file.

    Raises:
        FileNotFoundError: If the specified CSV file does not exist.
        ValueError: If the 'text' field in a row cannot be converted to a list.
        IndexError: If a row in the CSV file does not contain the expected number of fields.
    '''
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


if __name__ == '__main__':
    my_library = Library()

    books = csv_to_dict('../sample_books.csv')
    for book in books:
        book_data = Book(book["isbn"], book["genre"], book["text"])
        print(book_data)
        print(book_data.themes(10))
        print(f"pages: {book_data.page_count} words: {book_data.word_count}")
        my_library.add_book(book_data)



    print(my_library.search_by_title("The Great Gatsby").get_favorite())
    my_library.favorite_book("The Great Gatsby")
    print(my_library.search_by_title("The Great Gatsby").get_favorite())
    my_library.unfavorite_book("The Great Gatsby")
    print(my_library.search_by_title("The Great Gatsby").get_favorite())

    my_library.freq_genre()