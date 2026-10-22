import sqlite3
from datetime import date


DB_PATH = "mini_loans.db"


#!-------------CONNECT------------------------

def connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


#!---------------INIT_DB-----------------------

def init_db(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            is_available INTEGER NOT NULL DEFAULT 1
        );

        CREATE TABLE IF NOT EXISTS loans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_id INTEGER NOT NULL UNIQUE,
            borrower TEXT NOT NULL,
            loan_date TEXT NOT NULL,
            FOREIGN KEY(item_id) REFERENCES items(id) ON DELETE CASCADE)
        """
    )
    conn.commit()

#!-----------------GET_ITEMS---------------------

def get_items(conn):
    return conn.execute(
        "SELECT id, name, is_available FROM items ORDER BY id;"
    ).fetchall()


#!-----------------ADD_ITEMS----------------------

def add_item(conn):
    print(" ")
    name = input("Podaj nazwe samochodu do dodania: ").strip()

    if not name:
        print("Nazwa przedmiotu nie może być pusta!")
        return
    
    conn.execute("INSERT INTO items(name) VALUES(?)", (name,))
    conn.commit()

    print("Przedmiot dodany.")


#!-----------------LIST_ITEMS------------------------


def list_items(conn):
    print(" ")
    #Wyswietla recordy z bazy danych
    rows = conn.execute(
        "SELECT id, name, is_available FROM items ORDER BY id;"
    ).fetchall()

    # print(rows)

    for row in rows:
            avail = "TAK" if row["is_available"] == 1 else "NIE"
            print(f"{row['id']}. {row['name']} - {avail}")
    
    if not rows:
        print("Brak rekordów w bazie")
        return


#!-------------------LOAN_ITEM-----------------------


def loan_item(conn):
    print(" ")
    rows = get_items(conn)
    
    for row in rows:
        if row["is_available"] == 1:
            print(f"{row['id']}. {row['name']}")


    try:
        item_id = int(input("Podaj ID samochodu do wypożyczenia: "))
    except ValueError:
        print("Podaj ID")
        return

    item = conn.execute(
        "SELECT id, name, is_available FROM items WHERE id = ?", (item_id,)
    ).fetchone()

    if not item:
        print("Nie ma takiego samochodu:(")
        return
    
    if item["is_available"] == 0:
        print("Samochód wypożyczony")
        return

    borrower = input("Kto wypożycza? (Imie i Nazwisko): ").strip().title()

    if not borrower:
        print("Puste dane wypożyczającego!")
        return

    try:
        with conn:
            conn.execute("UPDATE items SET is_available = 0 WHERE id = ?", (item_id,))
            conn.execute(
                "INSERT INTO loans(item_id, borrower, loan_date) VALUES (?, ?, ?)",
                (item_id, borrower, date.today().isoformat())
            )
        print("WYPOŻYCZONO!")
    except sqlite3.IntegrityError:
        print("Coś poszło nie tak...")


#!-----------------RETURN_ITEMS----------------


def return_items(conn):
    print(" ")

    rows = [row for row in get_items(conn) if row["is_available"] == 0]

    if not rows:
        print("NIE WYPOŻYCZONO ŻADNEGO SAMOCHODU!")
        return

    for row in rows:
        print(f"{row['id']}. {row['name']}")
    # rows = get_items(conn)
    # if not loan:
    #     print("NIE WYPOŻYCZONO ŻDANEGO SAMOCHODU!")
    #     return
    # else:
    #     for row in rows:
    #         if row["is_available"] == 0:
    #             print(f"{row['id']}. {row['name']}")

    try:
        item_id = int(input("Podaj ID samochodu do zwrotu: "))
    except ValueError:
        print("Podaj ID")
        return

    loan = conn.execute(
        "SELECT id, borrower, loan_date FROM loans WHERE item_id = ?", (item_id,)
    ).fetchone()

    if not loan:
        print("Nie ma takiego samochodu:(")
        return

    try:
        with conn:
            conn.execute("DELETE FROM loans WHERE item_id = ?", (item_id,))
            conn.execute("UPDATE items SET is_available = 1 WHERE id = ?", (item_id,))
        print("ZWRÓCONO!")
    except sqlite3.IntegrityError:
        print("Coś poszło nie tak...")


#!-----------------LIST_LOANS-------------------
    
def list_loans(conn):
    print(" ")
    rows = conn.execute(
        """
            SELECT l.item_id, i.name, l.borrower, l.loan_date
            FROM loans AS l
            INNER JOIN items AS i ON i.id = l.item_id
            ORDER BY l.loan_date DESC
        """
    ).fetchall()


    if not rows:
        print("Brak danych.")
        return

    for row in rows:
        print(f"{row['item_id']}. {row['name']} - {row['borrower']} ({row['loan_date']})")


#!-------------------MENU------------------------

def menu():
    print("\n****** WYPOŻYCIALNIA SAMOCHODÓW ******")
    print("1. Dodaj samochód do bazy")
    print("2. Lista samochodów w bazie danych")
    print("3. Wypożycz samochód")
    print("4. Zwróć samochód")
    print("5. Lista wypożyczonych samochodów")
    print("0. Wyjśćie z programu")


#!-------------------MAIN-------------------------

def main():
    conn = connect()
    # print(conn)
    init_db(conn)

    while True:
        menu()
        print(" ")
        choise = input("Podaj numer opcji: ").strip()

        if choise == "1":
            add_item(conn)

        elif choise == "2":
            list_items(conn)

        elif choise == "3":
            loan_item(conn)

        elif choise == "4":
            return_items(conn)

        elif choise == "5":
            list_loans(conn)

        elif choise == "0":
            print("Zakończono działanie programu.")
            pass
            break

        else:
            print("Nie ma takiej opcji")

    conn.close()





if __name__ == "__main__":
    main()