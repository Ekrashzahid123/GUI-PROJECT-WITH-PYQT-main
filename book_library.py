# book_library.py

# Custom exception for unavailable book lending
class BookNotAvailableError(Exception):
    pass

# Book class with basic attributes
class Book:
    def __init__(self, title, author, isbn):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.is_lent = False  # Track if the book is currently lent out

    def __str__(self):
        return f"{self.title} by {self.author} (ISBN: {self.isbn})"

# Library class to manage books
class Library:
    def __init__(self):
        self.books = []  # Store all books

    def add_book(self, book):
        self.books.append(book)

    def remove_book(self, isbn):
        self.books = [book for book in self.books if book.isbn != isbn]

    def lend_book(self, isbn):
        for book in self.books:
            if book.isbn == isbn and not book.is_lent:
                book.is_lent = True
                return book
        raise BookNotAvailableError("Book is either not available or already lent.")

    def return_book(self, isbn):
        for book in self.books:
            if book.isbn == isbn and book.is_lent:
                book.is_lent = False
                return
        raise BookNotAvailableError("This book was not lent out.")

    def __iter__(self):
        # Custom iterator to yield only available books
        return (book for book in self.books if not book.is_lent)

    def books_by_author(self, author):
        # Generator function to yield books by specific author
        return (book for book in self.books if book.author.lower() == author.lower())

# Subclass for digital libraries with download size
class EBook(Book):
    def __init__(self, title, author, isbn, download_size):
        super().__init__(title, author, isbn)
        self.download_size = download_size  # in MB

    def __str__(self):
        return f"{self.title} by {self.author} (eBook, {self.download_size}MB)"
    