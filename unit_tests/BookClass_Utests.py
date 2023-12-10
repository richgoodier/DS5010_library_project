import sys
import os
sys.path.append(os.path.abspath('../'))
import unittest
from library_project import Book

# book = Book('9780590353427', genre="Fantasy", text=['The young wizard stepped into a world unseen, where magic breathed life into the very stones.', 'Hidden corridors whispered secrets of ancient spells, the walls echoing with the magic of yore.', 'A dance of light and shadow played across the grand hall, casting enchantments of old.'])

class Test_Book(unittest.TestCase):
    #1
    def setUp(self):
        # Setup for the tests; executed before each test method
        self.valid_isbn = '9780590353427'  # Harry Potter ISBN
        self.invalid_isbn = 'invalid_isbn'
        self.book_harry_potter = Book(self.valid_isbn, genre="Fantasy", text=['The young wizard stepped into a world unseen, where magic breathed life into the very stones.', 'Hidden corridors whispered secrets of ancient spells, the walls echoing with the magic of yore.', 'A dance of light and shadow played across the grand hall, casting enchantments of old.'])
        self.sentence = 'The young wizards stepped into a world unseen.'
        self.tokenized = ['young', 'wizard', 'step', 'world', 'unseen']
        
    #2
    def test_initialization_with_no_isbn(self):
        with self.assertRaises(TypeError):
            Book(None)
    #3
    def test_initialization_with_invalid_isbn(self):
        with self.assertRaises(ValueError):
            Book(self.invalid_isbn)
    #4
    def test_successful_initialization(self):
        book = Book(self.valid_isbn)
        self.assertEqual(book.isbn, self.valid_isbn)
    
    #2
    def test_get_book_info(self):
        info = ("Harry Potter And The Sorcerer's Stone",['J. K. Rowling'],'Arthur A. Levine Books','1998')
        self.assertEqual(info, self.book_harry_potter.get_book_info())
       
        with self.assertRaises(TypeError):
            Book.get_book_info()

    #5
    def test_search_text(self):
        self.assertEqual([0],self.book_harry_potter.search_text("young wizard"))
        self.assertEqual([],self.book_harry_potter.search_text("old wizard"))

    #6
    def test_themes(self):
        self.assertEqual(['magic'],(self.book_harry_potter.themes(1)))

    #7
    def test_count_words(self):
        self.assertEqual(46,(self.book_harry_potter.count_words()))
        with self.assertRaises(TypeError):
            Book.count_words()

    #8
    def test_get_favorite(self):
        self.assertEqual(0,self.book_harry_potter.get_favorite())

    #9
    def test_set_favorite(self):
        self.book_harry_potter.set_favorite(1)
        self.assertEqual(1,self.book_harry_potter.get_favorite())
        self.book_harry_potter.set_favorite(0)
        self.assertEqual(0,self.book_harry_potter.get_favorite())

    #10
    def test_tally_words(self):
        self.book_harry_potter.tally_words()
        variable ="{'young': 1, 'wizard': 1, 'step': 1, 'world': 1, 'unseen': 1, 'magic': 2, 'breathe': 1, 'life': 1, 'stones': 1, 'hidden': 1, 'corridor': 1, 'whisper': 1, 'secret': 1, 'ancient': 1, 'spell': 1, 'wall': 1, 'echo': 1, 'yore': 1, 'dance': 1, 'light': 1, 'shadow': 1, 'play': 1, 'across': 1, 'grand': 1, 'hall': 1, 'cast': 1, 'enchantment': 1, 'old': 1}"
        self.assertEqual(variable,str(self.book_harry_potter.tally_words()))

    #11   
    def test_get_bookmark(self):
        self.assertEqual(0, self.book_harry_potter.get_bookmark())
    
    #12
    def test_set_bookmark(self):
        self.book_harry_potter.set_bookmark(2)
        self.assertEqual(2, self.book_harry_potter.get_bookmark())

    #13
    def test_reset_bookmark(self):
        self.book_harry_potter.set_bookmark(2)
        self.book_harry_potter.reset_bookmark()
        self.assertEqual(0, self.book_harry_potter.get_bookmark())

    #14
    def test_get_wordnet_pos(self):
        self.assertEqual(Book.get_wordnet_pos("V"), "v")
        self.assertEqual(Book.get_wordnet_pos("R"), "r")
        self.assertEqual(Book.get_wordnet_pos("J"), "a")
        self.assertEqual(Book.get_wordnet_pos("default"), "n")
        with self.assertRaises(TypeError):
            Book.get_wordnet_pos()

    #15
    def test_tokenize(self):
        self.assertEqual(self.book_harry_potter.tokenize(self.sentence), self.tokenized)
        with self.assertRaises(TypeError):
            self.book_harry_potter.tokenize()

if __name__ == '__main__':
    unittest.main()
