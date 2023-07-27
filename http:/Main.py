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
    username = input("Enter a username: ")
    password = getpass("Enter a password: ")

    if username and password:
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        print("User registration successful.")
    else:
        print("Please fill in all the fields.")

# Function to authenticate a user
def login_user():
    username = input("Enter your username: ")
    password = getpass("Enter your password: ")

    if username and password:
        cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        user = cursor.fetchone()

        if user:
            print("Login successful.")
            return user[0]  # Return the user ID
        else:
            print("Invalid username or password.")
            return None
    else:
        print("Please fill in all the fields.")
        return None

# Function to add a book to the database
def add_book():
    title = input("Enter the title of the book: ")
    author = input("Enter the author of the book: ")
    pub_date = input("Enter the publication date of the book: ")
    keywords = input("Enter keywords for the book (comma-separated): ")

    if title and author and pub_date and keywords:
        cursor.execute('INSERT INTO books (title, author, publication_date, keywords) VALUES (?, ?, ?, ?)',
                       (title, author, pub_date, keywords))
        conn.commit()
        print("Book added to the library.")
    else:
        print("Please fill in all the fields.")

# Function to search for books in the database
def search_books():
    search_term = input("Enter a search term (title, author, or keyword): ")

    if search_term:
        cursor.execute('SELECT * FROM books WHERE title LIKE ? OR author LIKE ? OR keywords LIKE ?',
                       ('%'+search_term+'%', '%'+search_term+'%', '%'+search_term+'%'))
        books = cursor.fetchall()
        if books:
            print("Search Results:")
            for book in books:
                print(f"{book[1]} by {book[2]} ({book[3]}) - Keywords: {book[4]}")
        else:
            print("No books found.")
    else:
        print("Please enter a search term.")

# Function to view book details
def view_book_details():
    book_id = input("Enter the book ID to view details: ")
    cursor.execute('SELECT * FROM books WHERE id = ?', (book_id,))
    book = cursor.fetchone()

    if book:
        print("Title:", book[1])
        print("Author:", book[2])
        print("Publication Date:", book[3])
        print("Keywords:", book[4])
    else:
        print("Book not found.")

# Function for book borrowing
def borrow_book(user_id):
    book_id = input("Enter the book ID to borrow: ")

    # Check if the book is available
    cursor.execute('SELECT * FROM books WHERE id = ?', (book_id,))
    book = cursor.fetchone()

    if book:
        cursor.execute('INSERT INTO book_loans (user_id, book_id, borrow_date) VALUES (?, ?, ?)',
                       (user_id, book_id, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        conn.commit()
        print("Book borrowed successfully.")
    else:
        print("Book not found.")

# Function for book returning
def return_book(user_id):
    book_id = input("Enter the book ID to return: ")

    # Check if the book is on loan by the user
    cursor.execute('SELECT * FROM book_loans WHERE user_id = ? AND book_id = ? AND return_date IS NULL',
                   (user_id, book_id))
    loan = cursor.fetchone()

    if loan:
        cursor.execute('UPDATE book_loans SET return_date = ? WHERE id = ?',
                       (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), loan[0]))
        conn.commit()
        print("Book returned successfully.")
    else:
        print("You haven't borrowed this book or it has already been returned.")

# Main program loop
def main():
    user_id = None

    while True:
        print("\n1. Register\n2. Login\n3. Add Book\n4. Search Books\n5. View Book Details")
        print("6. Borrow Book\n7. Return Book\n8. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            register_user()
        elif choice == "2":
            user_id = login_user()
        elif choice == "3":
            add_book()
        elif choice == "4":
            search_books()
        elif choice == "5":
            view_book_details()
        elif choice == "6":
            if user_id:
                borrow_book(user_id)
            else:
                print("Please log in to borrow a book.")
        elif choice == "7":
            if user_id:
                return_book(user_id)
            else:
                print("Please log in to return a book.")
        elif choice == "8":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

    conn.close()

if __name__ == "__main__":
    main()
