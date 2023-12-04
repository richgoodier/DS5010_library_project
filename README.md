# Book Management System

This Python package provides an extensive framework for managing a library of books. It leverages several libraries such as `isbnlib`, `nltk`, and `matplotlib` for various features like ISBN validation, text analysis, and data visualization.

## Features

- **Book and Library Classes**: Core components for representing books and their collection.
- **ISBN Validation**: Uses `isbnlib` to validate and fetch book details.
- **Text Analysis**: Employs `nltk` for stopwords removal, lemmatization, and tokenization.
- **Data Visualization**: Uses `matplotlib` to plot frequency of authors and genres.
- **CSV Export and Import**: Functionality to export library data to CSV and import from it.
- **Advanced Book Search**: Ability to search for books by titles or quotes within them.
- **Reading Progress Tracking**: Bookmark functionality to track reading progress.
- **Favorites Management**: Ability to mark books as favorites and list them.

## Installation

This package requires Python 3.x. Dependencies include `isbnlib`, `nltk`, `matplotlib`, and `csv`, all listed in the requirments.txt file. To install these dependencies, navigate to the folder containing requirements.txt and use the following command:

```bash
pip install -r requirements.txt
```

## Usage

### Initializing the Library

```python
from library_project import Library, Book
my_library = Library()
```

### Adding and Managing Books

```python
book = Book(isbn="9780590353427", genre="Fantasy", text=["Page 1 text", "Page 2 text"])
my_library.add_book(book)
my_library.list_titles()
my_library.remove_book(book)
```

### Searching and Sorting

```python
found_book = my_library.search_by_title("Book Title")
books_with_quote = my_library.search_by_quote("a specific quote")
my_library.sort_by_author()
```

### Visualization and CSV Operations

```python
my_library.freq_author()
my_library.freq_genre()
my_library.export_to_csv("library_data.csv")
```

### Bookmark and Favorites

```python
book.set_bookmark(100)
my_library.favorite_book("Book Title")
favorite_books = my_library.list_favorites()
```

### Additional Features

- **Word Count**: Each book instance calculates its word count.
- **Themes Extraction**: Identifies key themes in a book using word frequency.
- **CSV to Dictionary**: A separate function that converts a CSV file into a dictionary of books.

## Authors

 - Albert Yildirim
 - Teja Ramana Modukuru
 - Rich Goodier
 - Suchita Sharma

## License

This project was submitted as an assignment for DS 5010.  It is for educational purposes only.
