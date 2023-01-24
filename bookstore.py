import sqlite3

db = sqlite3.connect('ebookstore')
cursor = db.cursor()

def enter():
    new_title = input("Title:  ")
    new_author = input("Author:  ")
    new_qty = input("Quantity:  ")

    while True:
        new_id = input("Enter id:  ")
        try:
            new_book = [new_id, new_title, new_author, new_qty]
            db.execute('''INSERT INTO books VALUES(?,?,?,?)''', new_book)
            db.commit()
            break
        except sqlite3.IntegrityError:
            print("this id already is in database. Enter new id:")
            continue


"""def update():
    menu = input(What do you want to update: 
                 1 - id
                 2 - title
                 3 - author 
                 4 - quantity)
    view_all()
    id_update = int(input("Enter the book's id you want to update: "))
    title_update = input("Enter new title: ")
"""       

def delete():
    view_all()
    id_delete_book = int(input("Enter id book's you want to delete: "))
    cursor.execute("""SELECT id, Title, Author FROM bookshop WHERE id = ?""", (id_delete_book, ))
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
            print('{0} : {1} : {2} : {3}'.format(row[0], row[1], row[2], row[3]))

    if "2" in search_parameters:
        title_search = input("Enter title: ")
        cursor.execute("""SELECT * FROM books WHERE Title LIKE '%?%' """, (title_search, ))
        for row in cursor:
            print('{0} : {1} : {2} : {3}'.format(row[0], row[1], row[2], row[3]))

    if "3" in search_parameters:
        author_search = input("Enter author: ")
        cursor.execute("""SELECT * FROM books WHERE Author = ? """, (author_search, ))
        for row in cursor:
            print('{0} : {1} : {2} : {3}'.format(row[0], row[1], row[2], row[3]))


def view_all():
    cursor.execute('''SELECT * FROM books''')
    for row in cursor:
        print('{0} : {1} : {2} : {3}'.format(row[0], row[1], row[2], row[3]))


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
    menu = input("""\nWhat do you intend to do:
    1 - Enter book
    2 - Update book
    3 - Delete book
    4 - Search books
    5 - View all books
    0 - Exit
    :  """)

    if menu == "1":
        enter()

    elif menu == "2":
        print("2 Update")

    elif menu == "3":
        delete()

    elif menu == "4":
        search()

    elif menu == "5":
        view_all()

    elif menu == "0":
        break

    else:
        print("Wrong enter. Try again please.")

print("Thank you for using BOOK Database")

db.close()