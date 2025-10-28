class Book:
    def __init__(self, book_id, title, author, genre ):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.genre = genre
       

        self._availability = "yes"  # use underscore for internal variable

    @property
    def availability(self):
        return self._availability

    @availability.setter
    def availability(self, value):
        self._availability = value

    def borrow(self):
        self.availability = "no" 

    def returnBook(self):
        self.availability = "yes"

    def getStatus(self):
        return self.availability


# Create an instance
book1 = Book(1, "Python 101", "John Doe", "Programming" )

print(book1.getStatus())  # should print "yes"
book1.borrow()
print(book1.getStatus())  # should print "no"
book1.returnBook()
print(book1.getStatus())  # should print "yes"


class User:
    def __init__(self,id,name,userType):
        self.Id=id
        self.Name=name
        self.userType=userType

    def viewBorrowedBooks():
        pass
    def requestBook():
        pass   

class Student(User):
    def __init__(self, id, name, userType):
        super().__init__(id, name, userType)
        self.booklimit=3

    def requestBook(self,book):
     if len(self.borrowedBooks)<self.booklimit:
        self.borrowedBooks.append(book)
        print(f"Book'{Book.title}'borrowed by Student{self.name}")
     else:
         print(f"student{self.name} has reached book limit({self.booklimit})")

class Teacher(User):
    def __init__(self, id, name, userType):
        super().__init__(id, name, userType, "Teacher")
        self.booklimit = 5

    def requestBook(self, book):
        if len(self.borrowedBooks) < self.booklimit:
            self.borrowedBooks.append(book)
            print(f"Book '{book.title}' borrowed by teacher {self.name}")
        else:
            print(f"Teacher {self.name} has reached book limit ({self.booklimit})")
