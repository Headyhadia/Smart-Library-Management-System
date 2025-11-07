from classes import *

# 1. Create filemanager and Library instance
file_manager = FileManager("transactions.txt", "books.txt", "users.txt")
library = Library(file_manager)

# Functions for GUI to call

# addBook
def addBook(book_id, title, author, genre):
    book = Book(book_id, title, author, genre)      # creating the book object with given parameters
    output = library.addBook(book) 
    return output


# registerUser
def registerUser(user_id, name, role):
    if role.lower() == "student":
        user = Student(user_id, name)
    elif role.lower() == "teacher":
        user = Teacher(user_id, name)
    else:
        raise ValueError("Role must be either 'student' or 'teacher'.")
    output = library.registerUser(user)
    return output


# searchBook
def searchBook(title, author=None, genre=None):
    return library.searchBook(title, author, genre)


# borrowBook
def borrowBook(user_id, book_id):
    status, result = library.borrowBook(user_id, book_id)
    return (status, result)


# returnBook
def returnBook(user_id, book_id):
    status, result = library.returnBook(user_id, book_id)
    return (status, result)


# checkOverdues
def checkOverdues():
    return library.checkOverdues()


# displayBooks
def displayBooks():
    return library.displayBooks()



