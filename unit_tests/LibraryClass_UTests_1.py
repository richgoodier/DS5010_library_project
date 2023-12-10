import sys
import os
sys.path.append(os.path.abspath('../'))
import unittest
import tempfile
from unittest.mock import patch
from io import StringIO

from library_project import Library, Book, csv_to_dict

class TestLibraryFunctions(unittest.TestCase):
    #1
    def setUp(self):
        # Creating a library instance for testing
        self.library = Library()

        
        
        # Adding books to the library for testing
        book_data = [
            {"isbn": "9780061120084", "genre": "Classic Literature", "text":['The small town buzzed with the whispers of the old case, a tale known to all, yet understood by few.', 'Under the sprawling oak, memories of justice and injustice entwined like the branches above.', "Each passing day brought new eyes to old stories, and the towns history lived anew."]},
            {"isbn": "9780451524935", "genre": "Dystopian Fiction", "text": ['In the world of constant surveillance, the truth was a commodity few could afford.', 'Words became whispers in the night, a silent rebellion against the ever-watchful eyes.', 'The clock struck thirteen, marking another hour under the watchful presence of Big Brother.']}
        ]
        for book in book_data:
            book_obj = Book(book["isbn"], book["genre"], book["text"])
            self.library.add_book(book_obj)
    #2
    def test_search_by_title_existing(self):
        # Test search_by_title for an existing book
        found_book = self.library.search_by_title("To Kill a Mockingbird")
        self.assertIsNotNone(found_book)
        self.assertEqual(found_book.isbn, "9780061120084")
    #3
    def test_search_by_title_not_existing(self):
        # Test search_by_title for a non-existing book
        found_book = self.library.search_by_title("Animal Farm")
        self.assertIsNone(found_book)
    #4
    def test_search_by_quote(self):
        # Test search_by_quote
        found_books = self.library.search_by_quote("The small town buzzed with the whispers of the old case")
        self.assertEqual(len(found_books), 1)  # Both added books have "text" in their content
    #5
    def test_sort_by_author(self):
        # Test sort_by_author
        self.library.sort_by_author()
        self.assertEqual(self.library.list[0].isbn, "9780451524935")  # Non-Fiction book comes first
    #6
    def test_export_to_csv(self):
        # Create a temporary file to write the CSV content
        temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False)

        # Call the export_to_csv method with the temporary file path
        self.library.export_to_csv(temp_file.name)
        
        # Close the file before reading its content
        temp_file.close()

        # Read the CSV content from the temporary file
        with open(temp_file.name, 'r') as file:
            csv_content = file.read()

        # Expected CSV content based on the test data
        expected_csv_content = (
            "Title,Author,Genre,ISBN\n"
            "To Kill A Mockingbird,Harper Lee,Classic Literature,9780061120084\n"
            "Nineteen Eighty-Four - A Novel,George Orwell,Dystopian Fiction,9780451524935\n"
            # Add more rows based on the expected data
        )

        # Compare the generated CSV content with the expected content
        self.assertEqual(csv_content, expected_csv_content)
    
    # Add more test cases for other functions as needed..."""

if __name__ == '__main__':
    unittest.main()
