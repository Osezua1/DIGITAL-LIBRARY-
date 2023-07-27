import tkinter as tk
from tkinter import messagebox
import sqlite3
from getpass import getpass
from datetime import datetime

# Database initialization
conn = sqlite3.connect('library.db')
cursor = conn.cursor()

# Create tables if they don't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        publication_date TEXT NOT NULL,
        keywords TEXT NOT NULL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS book_loans (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        book_id INTEGER NOT NULL,
        borrow_date TEXT NOT NULL,
        return_date TEXT,
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (book_id) REFERENCES books(id)
    )
''')
conn.commit()

# Function to add a user to the database
def register_user():
    username = entry_username.get()
    password = entry_password.get()

    if username and password:
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        messagebox.showinfo("Success", "User registration successful.")
    else:
        messagebox.showerror("Error", "Please fill in all the fields.")

# Function to authenticate a user
def login_user():
    username = entry_username.get()
    password = entry_password.get()

    if username and password:
        cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        user = cursor.fetchone()

        if user:
            messagebox.showinfo("Success", "Login successful.")
            return user[0]  # Return the user ID
        else:
            messagebox.showerror("Error", "Invalid username or password.")
            return None
    else:
        messagebox.showerror("Error", "Please fill in all the fields.")
        return None

# Function to add a book to the database
def add_book():
    title = entry_title.get()
    author = entry_author.get()
    pub_date = entry_pub_date.get()
    keywords = entry_keywords.get()

    if title and author and pub_date and keywords:
        cursor.execute('INSERT INTO books (title, author, publication_date, keywords) VALUES (?, ?, ?, ?)',
                       (title, author, pub_date, keywords))
        conn.commit()
        messagebox.showinfo("Success", "Book added to the library.")
    else:
        messagebox.showerror("Error", "Please fill in all the fields.")

# Function to search for books in the database
def search_books():
    search_term = entry_search.get()

    if search_term:
        cursor.execute('SELECT * FROM books WHERE title LIKE ? OR author LIKE ? OR keywords LIKE ?',
                       ('%'+search_term+'%', '%'+search_term+'%', '%'+search_term+'%'))
        books = cursor.fetchall()
        display_search_results(books)
    else:
        messagebox.showerror("Error", "Please enter a search term.")

# Function to display search results in a new window
def display_search_results(books):
    results_window = tk.Toplevel(root)
    results_window.title("Search Results")
    results_window.geometry("600x400")

    result_listbox = tk.Listbox(results_window, width=70, height=20)
    result_listbox.pack()

    for book in books:
        result_listbox.insert(tk.END, f"{book[1]} by {book[2]} ({book[3]}) - Keywords: {book[4]}")

# Function to view book details
def view_book_details():
    book_id = entry_book_id.get()
    cursor.execute('SELECT * FROM books WHERE id = ?', (book_id,))
    book = cursor.fetchone()

    if book:
        details_window = tk.Toplevel(root)
        details_window.title("Book Details")
        details_window.geometry("400x200")

        label_title = tk.Label(details_window, text="Title:")
        label_title.pack()
        label_title_value = tk.Label(details_window, text=book[1])
        label_title_value.pack()

        label_author = tk.Label(details_window, text="Author:")
        label_author.pack()
        label_author_value = tk.Label(details_window, text=book[2])
        label_author_value.pack()

        label_pub_date = tk.Label(details_window, text="Publication Date:")
        label_pub_date.pack()
        label_pub_date_value = tk.Label(details_window, text=book[3])
        label_pub_date_value.pack()

        label_keywords = tk.Label(details_window, text="Keywords:")
        label_keywords.pack()
        label_keywords_value = tk.Label(details_window, text=book[4])
        label_keywords_value.pack()

    else:
        messagebox.showerror("Error", "Book not found.")

# Function for book borrowing
def borrow_book(user_id):
    book_id = entry_borrow.get()

    # Check if the book is available
    cursor.execute('SELECT * FROM books WHERE id = ?', (book_id,))
    book = cursor.fetchone()

    if book:
        cursor.execute('INSERT INTO book_loans (user_id, book_id, borrow_date) VALUES (?, ?, ?)',
                       (user_id, book_id, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        conn.commit()
        messagebox.showinfo("Success", "Book borrowed successfully.")
    else:
        messagebox.showerror("Error", "Book not found.")

# Function for book returning
def return_book(user_id):
    book_id = entry_return.get()

    # Check if the book is on loan by the user
    cursor.execute('SELECT * FROM book_loans WHERE user_id = ? AND book_id = ? AND return_date IS NULL',
                   (user_id, book_id))
    loan = cursor.fetchone()

    if loan:
        cursor.execute('UPDATE book_loans SET return_date = ? WHERE id = ?',
                       (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), loan[0]))
        conn.commit()
        messagebox.showinfo("Success", "Book returned successfully.")
    else:
        messagebox.showerror("Error", "You haven't borrowed this book or it has already been returned.")

# Main program loop
def main():
    user_id = None

    root = tk.Tk()
    root.title("Digital Library")
    root.geometry("400x600")

    # User Authentication GUI
    label_username = tk.Label(root, text="Username:")
    label_username.pack()
    entry_username = tk.Entry(root)
    entry_username.pack()

    label_password = tk.Label(root, text="Password:")
    label_password.pack()
    entry_password = tk.Entry(root, show="*")
    entry_password.pack()

    btn_register = tk.Button(root, text="Register", command=register_user)
    btn_register.pack()

    btn_login = tk.Button(root, text="Login", command=lambda: login_user())
    btn_login.pack()

    # Book Management GUI
    label_title = tk.Label(root, text="Title:")
    label_title.pack()
    entry_title = tk.Entry(root)
    entry_title
