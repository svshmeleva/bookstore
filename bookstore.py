import sqlite3

db = sqlite3.connect('ebookstore')
cursor = db.cursor()

def row_print(row):
    print('{0} : {1} : {2} : {3}'.format(row[0], row[1], row[2], row[3]))

def add_new():
    new_title = input("Title:  ")
    new_author = input("Author:  ")
    new_qty = int(input("Quantity:  "))

    while True:
        new_id = int(input("Enter id:  "))
        try:
            new_book = [new_id, new_title, new_author, new_qty]
            db.execute('''INSERT INTO books VALUES(?,?,?,?)''', new_book)
            db.commit()
            break
        except sqlite3.IntegrityError:
            print("this id already is in database. Enter new id:")
            continue

def update():
    id = int(input("Enter id book's you want to update: "))
    cursor.execute("""SELECT * FROM books WHERE id = ?""", (id, ))
    for row in cursor:
        row_print(row)

    id_update = int(input("Enter new id or -1 to skip: "))
    if id_update == -1:
        id_update = id

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
    if qty_update == -1:
        pass
    else:
        cursor.execute("""UPDATE books SET Qty = ? WHERE id = ?""", (qty_update, id))
        db.commit()

    cursor.execute("""UPDATE books SET id = ? WHERE id = ?""", (id_update, id))
    db.commit()

def delete():
    view_all()
    id_delete_book = int(input("Enter id book's you want to delete: "))
    cursor.execute("""SELECT id, Title, Author FROM books WHERE id = ?""", (id_delete_book, ))
    for row in cursor:
        sure = input(f"""Do you want to delete this book:
    {'{0} : {1} : {2}'.format(row[0], row[1], row[2])}
y or n: """)
        if sure == "y":
            print(f"""Book:
    {'{0} : {1} : {2}'.format(row[0], row[1], row[2])}
has been successfully deleted""")            
            db.execute("""DELETE FROM books WHERE id = ?""", (id_delete_book, ))
            db.commit()
        else:
            print("Back to main menu")

def search():
    menu_search = input("""How would you search the book.
    Enter the search parameters separated by commas:
    1 - id
    2 - title
    3 - author
    e - exit
    : """)
    search_parameters = menu_search.split(',')

    if "1" in search_parameters:
        id_search = int(input("Enter book's id: "))
        cursor.execute("""SELECT * FROM books WHERE id = ? """, (id_search, ))
        for row in cursor:
            row_print(row)

    if "2" in search_parameters:
        title_search = input("Enter title: ")
        cursor.execute("""SELECT * FROM books WHERE Title LIKE '%?%' """, (title_search, ))
        for row in cursor:
            row_print(row)

    if "3" in search_parameters:
        author_search = input("Enter author: ")
        cursor.execute("""SELECT * FROM books WHERE Author = ? """, (author_search, ))
        for row in cursor:
            row_print(row)


def view_all():
    cursor.execute('''SELECT * FROM books''')
    for row in cursor:
        row_print(row)


cursor.execute('''
CREATE TABLE IF NOT EXISTS books(id INTEGER PRIMARY KEY, Title TEXT NOT NULL, Author TEXT NUT NULL, Qty INT DEFAULT 0)''')
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
    2 - Update book
    3 - Delete book
    4 - Search books
    5 - View all books
    0 - Exit
    :  """)

    if main_menu == "1":
        add_new()

    elif main_menu == "2":
        update()

    elif main_menu == "3":
        delete()

    elif main_menu == "4":
        search()

    elif main_menu == "5":
        view_all()

    elif main_menu == "0":
        break

    else:
        print("Wrong enter. Try again please.")

print("Thank you for using BOOK Database")

db.close()