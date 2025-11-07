from abc import ABC, abstractmethod # Base class for User
import datetime

class Book:
    def __init__(self, book_id, title, author, genre):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.genre = genre
        self.__availability = "yes"  # use double underscore for private variable
        self.due_date = None

    @property       # function to get availability
    def availability(self):
        return self.__availability
 
    @availability.setter         # function to set availability
    def availability(self, value):
        self.__availability = value

    def markUnavailable(self):     # marks the availabilty of book to no
        self.availability = "no" 

    def markAvailable(self):      # marks the availabilty of book to yes 
        self.availability = "yes"

    def getStatus(self):     # returns the availability status of book
        return self.availability


class User(ABC):     # abstract user class
    def __init__(self,id,name,userType):
        self.id=id
        self.name=name
        self.userType=userType
        self._borrowedBooks=[]   # protected array to store borrowed books of the user

    @abstractmethod       # abstract method to request book
    def requestBook(self, book):
        pass 

    def returnBook(self, book):    # concrete method to return book
        if book in self._borrowedBooks:
            self._borrowedBooks.remove(book)

 

class Student(User):        # concrete student class inherits from user class
    def __init__(self, id, name):
        super().__init__(id, name, "Student")
        self._booklimit=3

    def getBorrowLimit(self):    # function to get borrow limit of student
        return self._booklimit

    def requestBook(self, book):     # overriden method to request book, takes a book object as a parameter
        if len(self._borrowedBooks)<self.getBorrowLimit():
            self._borrowedBooks.append(book)
            return True
        else:
            return False

class Teacher(User):     # concrete Teacher class inherits from user class
    def __init__(self, id, name):
        super().__init__(id, name, "Teacher")
        self._booklimit = 5

    def getBorrowLimit(self):    # function to get borrow limit of teacher
        return self._booklimit

    def requestBook(self, book):
        if len(self._borrowedBooks) < self.getBorrowLimit():
            self._borrowedBooks.append(book)
            return True
        else:
            return False

class BorrowRecord:         # class to represent a borrow record; stores user, book, borrow date, return date
    def __init__(self, record_id, user, book, borrow_date, return_date=None):
        self.record_id = record_id
        self.user = user
        self.book = book
        self.borrow_date = borrow_date
        self.return_date = return_date      # None if not returned yet (this is not due date)

    def markReturned(self, return_date):  # marks the return date of the book
        self.return_date = return_date

    def isOverdue(self):    # checks if the book is overdue
        if self.return_date is None:
            due_date = self.borrow_date + datetime.timedelta(days=14)     # assuming 14 days borrow period if not returned yet
            return datetime.date.today() > due_date
        return False

class FileManager:
    def __init__(self, transactionFile, bookfile, userfile):   # initializes file manager with file paths
        self.__transactionFile = transactionFile
        self.__bookfile = bookfile  
        self.__userfile = userfile

    def saveTransaction(self, record):      # saves a single borrow record to the transaction file
        # write ISO dates or 'None' so we can parse them reliably later
        borrow_iso = record.borrow_date.isoformat() if isinstance(record.borrow_date, datetime.date) else str(record.borrow_date)
        return_iso = record.return_date.isoformat() if isinstance(record.return_date, datetime.date) else 'None'
        due_iso = record.book.due_date.isoformat() if getattr(record.book, 'due_date', None) else 'None'
        with open(self.__transactionFile, 'a') as file:
            file.write(f"{record.record_id},{record.user.id},{record.book.book_id},{borrow_iso},{due_iso},{return_iso}\n")

    def loadTransactions(self, users=None, books=None):     # loads borrow records from the transaction file; optionally takes lists of users and books to restore object references 
        records = []
        try:
            with open(self.__transactionFile, 'r') as file:
                for line in file:
                    record_id, user_id, book_id, borrow_date_s, due_date_s, return_date_s = line.strip().split(',')
                    # find real objects if lists provided
                    user = next((u for u in users if str(u.id) == user_id), None) if users else None     # find user by id
                    book = next((b for b in books if str(b.book_id) == book_id), None) if books else None       # find book by id

                    # parse dates (ISO) into datetime.date
                    borrow_date = datetime.date.fromisoformat(borrow_date_s)
                    return_date = datetime.date.fromisoformat(return_date_s) if return_date_s != 'None' else None
                    due_date = datetime.date.fromisoformat(due_date_s) if due_date_s != 'None' else None

                    # create record with object references (user/book may be None if not found)
                    record = BorrowRecord(int(record_id), user, book, borrow_date, return_date)

                    # restore due_date onto the book object if available and book object exists
                    if book is not None and due_date is not None:
                        book.due_date = due_date

                    records.append(record)
        except FileNotFoundError:
            print(f"Transaction file {self.__transactionFile} not found.")
        return records            
            
    def saveBooks(self, books):     # saves the list of books to the book file
        with open(self.__bookfile, 'w') as file:
            for book in books:
                file.write(f"{book.book_id},{book.title},{book.author},{book.genre},{book.availability}\n")

    def saveUsers(self, users):     # saves the list of users to the user file
        with open(self.__userfile, 'a') as file:
            for user in users:
                file.write(f"{user.id},{user.name},{user.userType}\n")
    def loadBooks(self):        # loads the list of books from the book file
        books = []
        try:
            with open(self.__bookfile, 'r') as file:
                for line in file:
                    book_id, title, author, genre, availability = line.strip().split(',')
                    book = Book(book_id, title, author, genre)
                    book.availability = availability
                    books.append(book)
        except FileNotFoundError:
            print(f"Book file {self.__bookfile} not found.")
        return books

    def loadUsers(self):       # loads the list of users from the user file
        users = []
        try:
            with open(self.__userfile, 'r') as file:
                for line in file:
                    id, name, userType = line.strip().split(',')
                    if userType == "Student":
                        users.append(Student(id, name))
                    elif userType == "Teacher":
                        users.append(Teacher(id, name))
        except FileNotFoundError:
            print(f"User file {self.__userfile} not found.")
        return users
    
    def updateBookAvailability(self, book):
        lines = []
        with open("books.txt", "r") as f:
            for line in f:
                parts = line.strip().split(",")
                if parts[0] == str(book.book_id):
                    parts[4] = book.availability   # assuming 5th column is availability
                    line = ",".join(parts)
                lines.append(line.strip())
        with open("books.txt", "w") as f:
            for line in lines:
                f.write(line + "\n")

    
class Library:
    def __init__(self, filemanager):
        self.__filemanager = filemanager
        self.__books = filemanager.loadBooks()
        self.__users = filemanager.loadUsers()
        self.__records = filemanager.loadTransactions(self.__users, self.__books)
         

    def addBook(self, book):
        output = ""
        self.__books.append(book)
        self.__filemanager.saveBooks(self.__books)
        output += f"Book '{book.title}' added successfully."
        return output

    def registerUser(self, user):
        output = ""
        self.__users.append(user)
        self.__filemanager.saveUsers(self.__users)
        output += f"User {user.name} registered successfully."
        return output

    def searchBook(self, title=None, author=None, genre=None):      # searches books by title, author, or genre
        results = []
        for book in self.__books:
            if ((title and title.lower() in book.title.lower()) or
            (author and author.lower() in book.author.lower()) or
            (genre and genre.lower() in book.genre.lower())):
                results.append(book)
        return results
    
    def borrowBook(self, user_id, book_id):     # borrows a book for a user by their ids
        msg = ""
        try:
            user = next((u for u in self.__users if u.id == user_id), None)  # Find user by id
            if user is None:
                raise ValueError(f"User with id {user_id} not found")
            book = next((b for b in self.__books if b.book_id == book_id), None)   # Find book by id
            if book is None:
                raise ValueError(f"Book with id {book_id} not found")
            if book.availability != "yes":
                raise ValueError(f"Book '{getattr(book, 'title', book_id)}' is not available")
            
            due_date = datetime.date.today() + datetime.timedelta(days=14)
            book.due_date = due_date

            if user.requestBook(book):    # if user borrows book successfully..
                book.markUnavailable()
                self.__filemanager.updateBookAvailability(book)
                record = BorrowRecord(len(self.__records) + 1, user, book, datetime.date.today())
                self.__records.append(record)
                self.__filemanager.saveTransaction(record)
                msg += f"Book '{book.title.title()}' borrowed by user {user.name.title()}"
                return ("success", msg)
            else:
                msg += f"User {user.name.title()} has reached book limit ({user.getBorrowLimit()})"
                return ("error", msg)
        except ValueError as e:
            print(e)
            return ("error", e)

    def returnBook(self, user_id, book_id):
        msg = ""
        try:
            user = next((u for u in self.__users if u.id == user_id), None)  # Find user by id
            if user is None:
                raise ValueError(f"User with id {user_id} not found")
            book = next((b for b in self.__books if b.book_id == book_id), None)   # Find book by id
            if book is None:
                raise ValueError(f"Book with id {book_id} not found")
            user.returnBook(book)
            book.markAvailable()
            self.__filemanager.updateBookAvailability(book)
            record = next((r for r in self.__records if r.user == user and r.book == book and r.return_date is None), None)
            if record:
                record.markReturned(datetime.date.today())
                self.__filemanager.saveTransaction(record)
                msg += f"Book '{book.title}' returned by user {user.name}"
                return ("success", msg)
            else:
                raise ValueError(f"No active borrow record found for user {user_id} and book {book_id}")     
        
        except ValueError as e:
            print(e)
            return ("error", e)
            

    def checkOverdues(self):
        overdue_records = []
        for record in self.__records:
            if record.isOverdue():
                overdue_records.append(record)
        return overdue_records
    
    def displayBooks(self):
        return self.__books
               
        

        