import sqlite3
from tabulate import tabulate


def init_db():
    """Initialise the database.

    Creates the books table in the ebookstore.db database if it doesn't already exists.
    """
    con = sqlite3.connect("ebookstore.db")
    cur = con.cursor()
    res = cur.execute("SELECT name FROM sqlite_master")
    table = res.fetchone()

    # Will only create a table if it's not there
    if table is None:
        cur.execute(
            "CREATE TABLE books(id INTEGER PRIMARY KEY, Title VARCHAR, Author VARCHAR, Qty INTEGER)")
        con.commit()
        con.close()


def populate_table(books):
    """ Populate the books table with data.

    Args: 
    books (list): List of tuples, where each tuple contains books data (id, title, author, quantity).
    """
    con = sqlite3.connect("ebookstore.db")
    cur = con.cursor()
    cur.executemany(
        """INSERT INTO books (id, Title, Author, Qty) VALUES(?,?,?,?)""", books)

    con.commit()
    con.close()


def enter_book():
    """Add a book to the database.

    Prompts the user to enter book information and adds it to the books table in the 
    ebookstore.db database. 
    """
    con = sqlite3.connect("ebookstore.db")
    cur = con.cursor()

    while True:
        try:
            _id = int(input("Enter the id: "))
            title = input("Enter the title of the book: ")
            author = input("Enter the name of the author: ")
            quantity = int(input("Enter the quantiy: "))
            cur.execute(
                f"""INSERT INTO books VALUES("{_id}", "{title}", "{author}", "{quantity}")""")
            con.commit()
            con.close()
        except ValueError:
            print("Please enter a valid input.")

        return


def update_book():
    """Update an existing book in the database

    Prompts the user to enter the id of the book to be updated and the updated information,
    then updates the relevant book in the books table in the ebookstore.db database.
    """
    con = sqlite3.connect("ebookstore.db")
    cur = con.cursor()

    while True:
        try:
            _id = int(input("Enter the id of the book you want to update: "))
            title = input("Enter the title of the book: ")
            author = input("Enter the name of the author: ")
            quantity = int(input("Enter the quantiy: "))
            cur.execute(
                f"""UPDATE books SET Title ="{title}", Author ="{author}", Qty="{quantity}" WHERE id="{_id}";""")
            con.commit()
            con.close()
        except ValueError:
            print("Please enter a valid input.")

        return


def delete_book():
    """Delete a book from the database.

    Prompts the user to enter the id of the book to be deleted and confirms the deletion
    before removing the book from the books table in the ebookstore.db database.
    """
    con = sqlite3.connect("ebookstore.db")
    cur = con.cursor()

    while True:
        try:
            _id = int(input("Enter the id of the book you want to delete: "))
            res = cur.execute(f"""SELECT * FROM books WHERE id="{_id}";""")
            delete_following_book = res.fetchone()
            print("\nYou've selected to delete:\n")
            print(tabulate([delete_following_book], headers=[
                  'id', 'Title', 'Author', 'Qty']))
            confirm_delete = input(
                "\nPlease confirm you want to delete this book from the database (y/n): ")
            if confirm_delete == "y":
                cur.execute(
                    f"DELETE FROM books WHERE id='{_id}'")
                con.commit()
                con.close()
            print("You have successfully deleted the book.")
            return
        except ValueError:
            print("Please enter a valid input.")

        return


def search_books():
    """Search for books in the database.

    Prompts the user to enter a search query and returns books in the books table in the 
    ebookstore.db database that match the query based on either title or author.
    """
    con = sqlite3.connect("ebookstore.db")
    cur = con.cursor()
    print("You can search by title or author")
    search_query = input(
        "Enter your search ")
    res = cur.execute(
        f"""SELECT * FROM books WHERE title LIKE "%{search_query}%" OR author LIKE "%{search_query}%";""")
    print(res.fetchall())


# Secret function option to allow for testing the program
def print_books():
    """Print all books in the database.

    Prints all books in the books table in the ebookstore.db database.
    """
    con = sqlite3.connect("ebookstore.db")
    cur = con.cursor()
    res = cur.execute("SELECT * FROM books")
    books = res.fetchall()
    print(tabulate(books, headers=['id', 'Title', 'Author', 'Qty']))


def user_menu():
    """Display the user menu

    Displays the options for the user to interact with the books table in the ebookstore.db database.
    """

    while True:
        print("""\nBookstore Menu:

1. Enter book
2. Update book
3. Delete book
4. Search books
0. Exit
    """)
        try:
            choice = int(input("Enter the number for the task: "))
            if choice == 1:
                enter_book()
            if choice == 2:
                update_book()
            if choice == 3:
                delete_book()
            if choice == 4:
                search_books()
            if choice == 5:
                print_books()
            if choice == 0:
                exit()
        except ValueError:
            print("Please select a valid number from menu.")


def main():
    """Initialise the program.
    """
    init_db()
    books = [(3001, "A Tale of Two Cities", "Charles Dickens", 30),
             (3002, "Harry Potter and the Philosopher's Stone", "J.K. Rowling", 40),
             (3003, "The Lion, the Witch and the Wardrobe", "C.S. Lewis", 25),
             (3004, "The Lord of the Rings", "J.R.R Tolkien", 37),
             (3005, "Alice in Wonderland", "Lewis Carrol", 12)]
    populate_table(books)
    user_menu()


main()
