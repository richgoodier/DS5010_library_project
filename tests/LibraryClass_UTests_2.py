import sys
import os
sys.path.append(os.path.abspath('../modules'))
import unittest
from library_project import Library 
from library_project import Book 

class TestLibrary(unittest.TestCase):
    
    
    def setUp(self):
        # Creating a library instance for testing
        self.library = Library()

        
        
        # Adding books to the library for testing
        book_data = [
            {"isbn": "9780061120084", "genre": "Classic Literature", "text":['The small town buzzed with the whispers of the old case, a tale known to all, yet understood by few.', 'Under the sprawling oak, memories of justice and injustice entwined like the branches above.', "Each passing day brought new eyes to old stories, and the towns history lived anew."]},
            {"isbn": "9780451524935", "genre": "Dystopian Fiction", "text": ['In the world of constant surveillance, the truth was a commodity few could afford.', 'Words became whispers in the night, a silent rebellion against the ever-watchful eyes.', 'The clock struck thirteen, marking another hour under the watchful presence of Big Brother.']},
            {'isbn': '9780062315007', 'genre': 'Philosophical Fiction', 'text': ['In the journey of the soul, every step was a lesson, every path a different story.', 'The desert spoke in silence, teaching the language of the world, heard by those who listened.', "Dreams and reality merged under the sun's gaze, as the alchemist sought the truth within."]}
        ]
        for book in book_data:
            book_obj = Book(book["isbn"], book["genre"], book["text"])
            self.library.add_book(book_obj)
                      
    def test_add(self):
        #Checks if the list of library is 3 (we added 3 books)
        #add was done through setUp method
        self.assertEqual(len(self.library.list), 3) #list should have 3 books

    def test_favorite_book(self):
        #sets To kill a mockingbird as a favorite
        self.library.favorite_book('To Kill A Mockingbird')
        #check the favorite list after setting To Kill a Mockingbird as a favorite
        self.assertEqual(len(self.library.list_favorites()), 1) #the list should only have 1 book
        
    def test_unfavorite_book(self):
        #Unfavorite the favorited book
        self.library.unfavorite_book('To Kill A Mockingbird')
        #checks that the list is empty since we removed it from our favorites
        self.assertEqual(len(self.library.list_favorites()), 0) #the list should have no books
        
    def test_progress_check(self):
        #Set bookmark of first book to 0
        self.library.list[0].set_bookmark(0) 
        #Set bookmark of second book to 1
        self.library.list[1].set_bookmark(1)
        #set bookmark of last book to 2
        self.library.list[2].set_bookmark(2)
        
        #checks if the progress check matches the list given
        self.assertEqual(self.library.progress_check(), {'To Kill A Mockingbird': 'Not Started', 'Nineteen Eighty-Four - A Novel': 'Reading in Progress', 'The Alchemist': 'Completed'})
    
    def test_freq_author(self):
        #We test to see if the return of freq_author dictionary is correct
        self.assertEqual(self.library.freq_author(), {'Harper Lee': 1, 'George Orwell': 1, 'Paulo Coelho': 1}) #a dictionary with a key of authors and a value of 1 for each author (frequnecy 1)

    def test_freq_genre(self):
        #We test to see if the return of freq_genre dictionary is correct
        self.assertEqual(self.library.freq_genre(), {'Classic Literature': 1, 'Dystopian Fiction': 1, 'Philosophical Fiction': 1}) #a dictionary with a key of genres and a value of 1 for each genre (frequency 1) 
    
    def test_remove_book(self):
        self.library.remove_book('To Kill A Mockingbird')
        self.assertEqual(len(self.library.list), 2)
 


if __name__ == '__main__':
    unittest.main()