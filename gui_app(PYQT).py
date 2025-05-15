import sys
import PyQt6.QtWidgets as QtWidgets
from PyQt6.QtGui import QDoubleValidator
from book_library import Book, EBook, Library, BookNotAvailableError

class LibraryApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.library = Library()
        self.setWindowTitle("Library Management System")
        self.setGeometry(100, 100, 600, 500)
        self.init_ui()

    def init_ui(self):
        layout = QtWidgets.QVBoxLayout()

        layout.addWidget(QtWidgets.QLabel("Title:"))
        self.title_input = QtWidgets.QLineEdit()
        layout.addWidget(self.title_input)

       
        layout.addWidget(QtWidgets.QLabel("Author:"))
        self.author_input = QtWidgets.QLineEdit()
        layout.addWidget(self.author_input)
       
        layout.addWidget(QtWidgets.QLabel("ISBN:"))
        self.isbn_input = QtWidgets.QLineEdit()
        layout.addWidget(self.isbn_input)

        self.ebook_check = QtWidgets.QCheckBox("Is eBook?")
        self.ebook_check.stateChanged.connect(self.toggle_ebook_fields)
        layout.addWidget(self.ebook_check)

   
        layout.addWidget(QtWidgets.QLabel("Download Size (MB):"))
        self.size_input = QtWidgets.QLineEdit()
        self.size_input.setEnabled(False)
        self.size_input.setValidator(QDoubleValidator(0.0, 10000.0, 2))
        layout.addWidget(self.size_input)

      
        layout.addWidget(self.create_button("Add Book", self.add_book))
        layout.addWidget(self.create_button("Lend Book", self.lend_book))
        layout.addWidget(self.create_button("Return Book", self.return_book))
        layout.addWidget(self.create_button("Remove Book", self.remove_book))
        layout.addWidget(self.create_button("View Books by Author", self.view_books_by_author))

        layout.addWidget(QtWidgets.QLabel("Library Inventory:"))
        self.book_list = QtWidgets.QListWidget()
        layout.addWidget(self.book_list)

        self.setLayout(layout)
        self.update_book_list()

    def create_button(self, text, slot):
        button1 = QtWidgets.QPushButton(text)
        button1.clicked.connect(slot)
        return button1

    def toggle_ebook_fields(self):
        is_checked = self.ebook_check.isChecked()
        self.size_input.setEnabled(is_checked)
        if not is_checked:
            self.size_input.clear()

    def add_book(self):
        title = self.title_input.text()
        author = self.author_input.text()
        isbn = self.isbn_input.text()
        is_ebook = self.ebook_check.isChecked()
        size = self.size_input.text()

        if not title or not author or not isbn:
            QtWidgets.QMessageBox.warning(self, "Error", "Title, Author, and ISBN are required.")
            return

        if is_ebook:
            if not size:
                QtWidgets.QMessageBox.warning(self, "Error", "Download size is required for eBooks.")
                return
            try:
                size = float(size)
            except ValueError:
                QtWidgets.QMessageBox.warning(self, "Error", "Download size must be a number.")
                return
            book = EBook(title, author, isbn, size)
        else:
            book = Book(title, author, isbn)

        self.library.add_book(book)
        QtWidgets.QMessageBox.information(self, "Success", f"Book '{title}' added to the library.")
        self.clear_inputs()
        self.update_book_list()

    def lend_book(self):
        isbn, ok = QtWidgets.QInputDialog.getText(self, "Lend Book", "Enter ISBN to lend:")
        if ok and isbn:
            try:
                self.library.lend_book(isbn)
                QtWidgets.QMessageBox.information(self, "Success", "Book lent successfully.")
                self.update_book_list()
            except BookNotAvailableError as error:
                QtWidgets.QMessageBox.warning(self, "Error", str(error))

    def return_book(self):
        isbn, ok = QtWidgets.QInputDialog.getText(self, "Return Book", "Enter ISBN to return:")
        if ok and isbn:
            try:
                self.library.return_book(isbn)
                QtWidgets.QMessageBox.information(self, "Success", "Book returned successfully.")
                self.update_book_list()
            except BookNotAvailableError as e:
                QtWidgets.QMessageBox.warning(self, "Error", str(e))

    def remove_book(self):
        isbn, ok = QtWidgets.QInputDialog.getText(self, "Remove Book", "Enter ISBN to remove:")
        if ok and isbn:
            self.library.remove_book(isbn)
            QtWidgets.QMessageBox.information(self, "Success", "Book removed successfully.")
            self.update_book_list()

    def view_books_by_author(self):
        author, ok = QtWidgets.QInputDialog.getText(self, "Search by Author", "Enter author's name:")
        if ok and author:
            books = list(self.library.books_by_author(author))
            self.book_list.clear()
            if books:
                self.book_list.addItem(f"Books by {author}:")
                for book in books:
                    self.book_list.addItem(str(book))
            else:
                QtWidgets.QMessageBox.information(self, "Not Found", "No books by this author.")

    def update_book_list(self):
        self.book_list.clear()
        self.book_list.addItem("Available Books:")
        for book in self.library:
            self.book_list.addItem(str(book))

    def clear_inputs(self):
        self.title_input.clear()
        self.author_input.clear()
        self.isbn_input.clear()
        self.ebook_checkbox.setChecked(False)
        self.size_input.clear()
        self.size_input.setEnabled(False)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = LibraryApp()
    win.show()
    sys.exit(app.exec())
