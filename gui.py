import tkinter as tk
from tkinter import messagebox
from main import *

class LibraryGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Library Management System")
        self.root.geometry("850x550")
        self.root.configure(bg="#f0f0f0")

        self.frames = {}
        for name in ["main", "addBook", "registerUser", "searchBook",
                     "borrowBook", "returnBook", "checkOverdues", "displayBooks"]:
            frame = tk.Frame(root, bg="#f0f0f0")
            frame.grid(row=0, column=0, sticky="nsew")
            self.frames[name] = frame

        self.setup_main()
        self.setup_add_book()
        self.setup_register_user()
        self.setup_search_book()
        self.setup_borrow_book()
        self.setup_return_book()
        self.setup_check_overdues()
        self.setup_display_books()

        self.show_frame("main")

    def show_frame(self, name):
        self.frames[name].tkraise()

    # ---------------- MAIN PAGE ----------------
    def setup_main(self):
        f = self.frames["main"]

        tk.Label(f, text="Library Management System",
                 font=("Arial", 24, "bold"), bg="#f0f0f0").grid(row=0, column=0, columnspan=3, pady=40)

        buttons = [
            ("Add Book", "addBook"),
            ("Register User", "registerUser"),
            ("Search Book", "searchBook"),
            ("Borrow Book", "borrowBook"),
            ("Return Book", "returnBook"),
            ("Check Overdues", "checkOverdues"),
            ("Display Books", "displayBooks"),
        ]

        row, col = 1, 0
        for text, frame_name in buttons:
            tk.Button(f, text=text, width=20, height=2, font=("Arial", 12),
                      command=lambda n=frame_name: self.show_frame(n)).grid(row=row, column=col, padx=47, pady=25)
            col += 1
            if col > 2:
                col = 0
                row += 1

        tk.Button(f, text="Exit", width=20, height=2,
                  command=self.root.destroy, bg="#cc4444", fg="white").grid(row=row + 1, column=1, pady=30)

    # ---------------- ADD BOOK ----------------
    def setup_add_book(self):
        f = self.frames["addBook"]
        tk.Label(f, text="Add Book", font=("Arial", 18, "bold")).pack(pady=20)
        entries = {}
        for field in ["Book ID", "Title", "Author", "Genre"]:
            tk.Label(f, text=field).pack()
            entries[field] = tk.Entry(f)
            entries[field].pack()

        def submit():
            try:
                book_id = entries["Book ID"].get().strip()
                title = entries["Title"].get().strip()
                author = entries["Author"].get().strip()
                genre = entries["Genre"].get().strip()

                if not all([book_id, title, author, genre]):
                    messagebox.showerror("Error", "All fields are required to add a book.")
                    return

                output = addBook(book_id, title, author, genre)
                messagebox.showinfo("Book Added Successfully!", output)
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(f, text="Add", command=submit).pack(pady=10)
        tk.Button(f, text="Back", command=lambda: self.show_frame("main")).pack(pady=10)


    # ---------------- REGISTER USER ----------------
    def setup_register_user(self):
        f = self.frames["registerUser"]
        tk.Label(f, text="Register User", font=("Arial", 18, "bold")).pack(pady=20)
        tk.Label(f, text="User ID").pack()
        uid = tk.Entry(f)
        uid.pack()
        tk.Label(f, text="Name").pack()
        uname = tk.Entry(f)
        uname.pack()
        tk.Label(f, text="Role (Student/Teacher)").pack()
        role = tk.Entry(f)
        role.pack()

        def submit():
            try:
                output = registerUser(uid.get(), uname.get(), role.get())
                messagebox.showinfo("Success", output)
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(f, text="Register", command=submit).pack(pady=10)
        tk.Button(f, text="Back", command=lambda: self.show_frame("main")).pack(pady=10)

    # ---------------- SEARCH BOOK ----------------
    def setup_search_book(self):
        f = self.frames["searchBook"]
        tk.Label(f, text="Search Book", font=("Arial", 18, "bold")).pack(pady=20)
        tk.Label(f, text="Title").pack()
        title = tk.Entry(f)
        title.pack()
        tk.Label(f, text="Author").pack()
        author = tk.Entry(f)
        author.pack()
        tk.Label(f, text="Genre").pack()
        genre = tk.Entry(f)
        genre.pack()
        results = tk.Text(f, width=80, height=12)
        results.pack(pady=10)

        def search():
            try:
                data = searchBook(title.get(), author.get(), genre.get())
                results.delete(1.0, tk.END)
                if not data:
                    results.insert(tk.END, "No results found.")
                else:
                    for book in data:
                        results.insert(tk.END,
                                       f"ID: {book.book_id}, Title: {book.title}, Author: {book.author}, Genre: {book.genre}, Available: {book.availability}\n")
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(f, text="Search", command=search).pack(pady=5)
        tk.Button(f, text="Back", command=lambda: self.show_frame("main")).pack(pady=10)

    # ---------------- BORROW BOOK ----------------
    def setup_borrow_book(self):
        f = self.frames["borrowBook"]
        tk.Label(f, text="Borrow Book", font=("Arial", 18, "bold")).pack(pady=20)
        tk.Label(f, text="User ID").pack()
        uid = tk.Entry(f)
        uid.pack()
        tk.Label(f, text="Book ID").pack()
        bid = tk.Entry(f)
        bid.pack()

        def submit():
            try:
                status, msg = borrowBook(uid.get(), bid.get())
                if status == "error":
                    messagebox.showerror("Error", msg)
                else:
                    messagebox.showinfo("Success", msg)
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(f, text="Borrow", command=submit).pack(pady=10)
        tk.Button(f, text="Back", command=lambda: self.show_frame("main")).pack(pady=10)

    # ---------------- RETURN BOOK ----------------
    def setup_return_book(self):
        f = self.frames["returnBook"]
        tk.Label(f, text="Return Book", font=("Arial", 18, "bold")).pack(pady=20)
        tk.Label(f, text="User ID").pack()
        uid = tk.Entry(f)
        uid.pack()
        tk.Label(f, text="Book ID").pack()
        bid = tk.Entry(f)
        bid.pack()

        def submit():
            try:
                status, msg = returnBook(uid.get(), bid.get())
                if status == "error":
                    messagebox.showerror("Error", msg)
                else:
                    messagebox.showinfo("Success", msg)
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(f, text="Return", command=submit).pack(pady=10)
        tk.Button(f, text="Back", command=lambda: self.show_frame("main")).pack(pady=10)

    # ---------------- CHECK OVERDUES ----------------
    def setup_check_overdues(self):
        f = self.frames["checkOverdues"]
        tk.Label(f, text="Check Overdues", font=("Arial", 18, "bold")).pack(pady=20)
        text = tk.Text(f, width=80, height=12)
        text.pack(pady=10)

        def check():
            try:
                data = checkOverdues()
                text.delete(1.0, tk.END)
                if not data:
                    text.insert(tk.END, "No overdue books.")
                else:
                    for d in data:
                        text.insert(tk.END, str(d) + "\n")
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(f, text="Check", command=check).pack(pady=5)
        tk.Button(f, text="Back", command=lambda: self.show_frame("main")).pack(pady=10)

    # ---------------- DISPLAY BOOKS ----------------
    def setup_display_books(self):
        f = self.frames["displayBooks"]
        tk.Label(f, text="Display Books", font=("Arial", 18, "bold")).pack(pady=20)
        text = tk.Text(f, width=80, height=15)
        text.pack(pady=10)

        def refresh():
            try:
                data = displayBooks()
                text.delete(1.0, tk.END)
                if not data:
                    text.insert(tk.END, "No books found.")
                else:
                    for book in data:
                        text.insert(tk.END,
                                    f"ID: {book.book_id}, Title: {book.title}, Author: {book.author}, Genre: {book.genre}, Available: {book.availability}\n")
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(f, text="Refresh", command=refresh).pack(pady=5)
        tk.Button(f, text="Back", command=lambda: self.show_frame("main")).pack(pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryGUI(root)
    root.mainloop()
