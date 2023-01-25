import sqlite3
from tabulate import tabulate

db = sqlite3.connect('ebookstore')
cursor = db.cursor()

def add_new():
# Function to add new ro to TABLE books 
    new_title = input("Title:  ")
    new_author = input("Author:  ")
    try:
        new_qty = int(input("Quantity:  "))
    except ValueError:
        new_qty = 0
        print("Incorrect entry. Quantity equals 0")
    new_book = [new_title, new_author, new_qty]
    db.execute('''INSERT INTO books (Title, Author, Qty) VALUES(?,?,?)''', new_book)
    db.commit()
    cursor.execute("""SELECT * FROM books WHERE id = (SELECT max(id) FROM books)""")
    for row in cursor:
        row_print(row)
    print("Book has been successfully added.")

def update(id):
# Function to update information for book with id as a parameter
    cursor.execute("""SELECT * FROM books WHERE id = ?""", (id, ))
    for row in cursor:
        row_print(row)

    title_update = input("Enter new Title or -1 to skip: ")
    if title_update == "-1":
        pass
    else:
        cursor.execute("""UPDATE books SET Title = ? WHERE id = ?""", (title_update, id))
        db.commit()

    author_update = input("Enter new Author or -1 to skip: ")
    if author_update == "-1":
        pass
    else:
        cursor.execute("""UPDATE books SET Author = ? WHERE id = ?""", (author_update, id))
        db.commit()

    qty_update = input("Enter new Qty or -1 to skip: ")
    if qty_update == "-1":
        pass
    else:
        cursor.execute("""UPDATE books SET Qty = ? WHERE id = ?""", (qty_update, id))
        db.commit()

def delete(id_delete_book):
    cursor.execute("""SELECT id, Title, Author FROM books WHERE id = ?""", (id_delete_book, ))
    for row in cursor:
        sure = input(f"""Do you want to delete this book:
    {'{0} : {1} : {2}'.format(row[0], row[1], row[2])}
y or any to exit: """)
        if sure == "y":
            print(f"""Book {row[1]} by {row[2]} has been successfully deleted""")            
            db.execute("""DELETE FROM books WHERE id = ?""", (id_delete_book, ))
            db.commit()
        else:
            print("Back to main menu")

def search():
    while True:
        menu_search = input("""Search books by:
        1 - id
        2 - title
        3 - author
        e - exit
        : """)

        if menu_search == '1':
            id_search = int(input("Enter book's id: "))
            cursor.execute("""SELECT * FROM books WHERE id = ? """, (id_search, ))
            row = cursor.fetchone()
            if row is None:
                print(f"No book with id {id_search}")
            else: 
                row_print(row)
                menu(id_search)

        elif menu_search == '2':
            title_search = input("Enter title: ")
            rows = cursor.execute("""SELECT * FROM books WHERE Title LIKE ? """, ('%'+title_search+'%', ))
            for row in rows:
                row_print(row)
            rows = cursor.execute("""SELECT * FROM books WHERE Title LIKE ? """, ('%'+title_search+'%', ))
            row = rows.fetchone()
            if row is None:
                print(f"No book this title {title_search}")
            else:
                try:
                    id = int(input("""
        Enter id to update or delete 
        OR 0 to exit: """))
                    if id == "0":
                        break
                    else:
                        menu(id)
                except ValueError:
                    print("Incorrect entry")

        elif menu_search == '3':
            author_search = input("Enter author: ")
            rows = cursor.execute("""SELECT * FROM books WHERE Author LIKE ? """, ('%'+author_search+'%', ))
            for row in rows:
                row_print(row)
            rows = cursor.execute("""SELECT * FROM books WHERE Author LIKE ? """, ('%'+author_search+'%', ))
            row = rows.fetchone()
            if row is None:
                print(f"No book this author {author_search}")
            else:
                id = int(input("""
        Enter id to update or delete 
        OR 0 to exit: """))
                menu(id)
        
        elif menu_search == 'e':
            break
        else:
            print("Wrong enter. Try again please.")

def menu(id):
    while True:
        menu = input("""
            Choose:
            1 - to update
            2 - to delete
            3 - to view
            e - exit
                : """)
        if menu == '1':
            update(id)
        elif menu == '2':
            delete(id)
        elif menu == '3':
            cursor.execute("""SELECT * FROM books WHERE id = ?""", (id, ))
            for row in cursor:
                row_print(row)
        elif menu == 'e':
            break
        else:
            print("Wrong enter. Try again please.")

def row_print(row):
    print(f'''=================================================================
    id:       {row[0]} 
    Title:    {row[1]} 
    Autor:    {row[2]} 
    Quantity: {row[3]}''')

def view_all():
    list_for_table = []
    cursor.execute('PRAGMA table_info("books")')
    column_names = [i[1] for i in cursor.fetchall()]

    cursor.execute('SELECT * FROM books')
    for row in cursor:
        row_list = []
        for i in range(len(row)):
            row_list.append(row[i])
        list_for_table.append(row_list)

    print(tabulate(list_for_table, headers= column_names))

cursor.execute('''
CREATE TABLE IF NOT EXISTS books(id INTEGER PRIMARY KEY AUTOINCREMENT, Title TEXT NOT NULL, Author TEXT NUT NULL, Qty INT DEFAULT 0)''')
cursor.execute("""SELECT * FROM books""")
row = cursor.fetchone()
if row is None:
    books = [(3001, "A Tale of Two Cities", "Charles Dickens", 30), 
            (3002, "Harry Potter and the Philosopher's Stone", "J.K. Rowling", 40), 
            (3003, "The Lion, the Witch and the Wardrobe", "C.S. Lewis", 25), 
            (3004, "The Lord of the Rings", "J.R.R Tolkien", 37), 
            (3005, "Alice in Wonderland", "Lewis Carroll", 12)]

    cursor.executemany(''' INSERT INTO books(id, Title, Author, Qty) VALUES(?,?,?,?)''', books)
db.commit()


while True:
    main_menu = input("""\nMain menu:
    1 - Enter book
    2 - Search books (to update or delete)
    3 - View all books
    0 - Exit
    :  """)

    if main_menu == "1":
        add_new()

    elif main_menu == "2":
        search()

    elif main_menu == "3":
        view_all()

    elif main_menu == "0":
        break

    else:
        print("Wrong enter. Try again please.")

print("Thank you for using BOOK Database")

db.close()
