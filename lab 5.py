import sqlite3

# Часть 1: Создание базы данных библиотеки

def create_library_database():
    """Создает базу данных и таблицу books"""
    try:
        with sqlite3.connect('library.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS books (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    author TEXT NOT NULL,
                    year INTEGER,
                    isbn TEXT UNIQUE,
                    available INTEGER DEFAULT 1
                )
            ''')
            conn.commit()
            print("База данных успешно создана!")
    except sqlite3.Error as e:
        print(f"Ошибка при создании базы данных: {e}")


def add_book(title, author, year, isbn):
    """Добавляет одну книгу в базу данных"""
    try:
        with sqlite3.connect('library.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO books (title, author, year, isbn)
                VALUES (?, ?, ?, ?)
            ''', (title, author, year, isbn))
            conn.commit()
            print(f"Книга '{title}' успешно добавлена!")
    except sqlite3.IntegrityError:
        print(f"Ошибка: Книга с ISBN {isbn} уже существует в базе!")
    except sqlite3.Error as e:
        print(f"Ошибка при добавлении книги: {e}")


def add_multiple_books(books_data):
    """Добавляет несколько книг одновременно"""
    try:
        with sqlite3.connect('library.db') as conn:
            cursor = conn.cursor()
            cursor.executemany('''
                INSERT INTO books (title, author, year, isbn)
                VALUES (?, ?, ?, ?)
            ''', books_data)
            conn.commit()
            print(f"Успешно добавлено {len(books_data)} книг!")
    except sqlite3.IntegrityError:
        print("Ошибка: Одна из книг уже существует в базе!")
    except sqlite3.Error as e:
        print(f"Ошибка при добавлении книг: {e}")


# Часть 2: Функции для работы с данными

def show_all_books():
    """Выводит список всех книг"""
    try:
        with sqlite3.connect('library.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM books')
            books = cursor.fetchall()
            
            if not books:
                print("В библиотеке пока нет книг.")
                return
            
            print("\n=== Список всех книг ===")
            for book in books:
                available_status = "Да" if book[5] == 1 else "Нет"
                print(f'ID: {book[0]} | Название: "{book[1]}" | Автор: {book[2]} | Год: {book[3]} | Доступна: {available_status}')
            print()
    except sqlite3.Error as e:
        print(f"Ошибка при получении списка книг: {e}")


def find_books_by_author(author_name):
    """Находит все книги конкретного автора"""
    try:
        with sqlite3.connect('library.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM books WHERE author LIKE ?', (f'%{author_name}%',))
            books = cursor.fetchall()
            
            if not books:
                print(f"Книги автора '{author_name}' не найдены.")
                return
            
            print(f"\n=== Книги автора '{author_name}' ===")
            for book in books:
                available_status = "Да" if book[5] == 1 else "Нет"
                print(f'ID: {book[0]} | Название: "{book[1]}" | Год: {book[3]} | Доступна: {available_status}')
            print()
    except sqlite3.Error as e:
        print(f"Ошибка при поиске книг: {e}")


def find_books_by_year_range(start_year, end_year):
    """Находит книги, изданные в указанном диапазоне лет"""
    try:
        with sqlite3.connect('library.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM books WHERE year BETWEEN ? AND ?', (start_year, end_year))
            books = cursor.fetchall()
            
            if not books:
                print(f"Книги за период {start_year}-{end_year} не найдены.")
                return
            
            print(f"\n=== Книги {start_year}-{end_year} годов ===")
            for book in books:
                available_status = "Да" if book[5] == 1 else "Нет"
                print(f'ID: {book[0]} | Название: "{book[1]}" | Автор: {book[2]} | Год: {book[3]} | Доступна: {available_status}')
            print()
    except sqlite3.Error as e:
        print(f"Ошибка при поиске книг: {e}")


def borrow_book(book_id):
    """Отмечает книгу как выданную"""
    try:
        with sqlite3.connect('library.db') as conn:
            cursor = conn.cursor()
            
            # Проверяем существование книги
            cursor.execute('SELECT available FROM books WHERE id = ?', (book_id,))
            result = cursor.fetchone()
            
            if result is None:
                print(f"Ошибка: Книга с ID {book_id} не найдена!")
                return
            
            if result[0] == 0:
                print("Книга уже выдана!")
                return
            
            # Обновляем статус
            cursor.execute('UPDATE books SET available = 0 WHERE id = ?', (book_id,))
            conn.commit()
            print(f"Книга с ID {book_id} успешно выдана!")
    except sqlite3.Error as e:
        print(f"Ошибка при выдаче книги: {e}")


def return_book(book_id):
    """Отмечает книгу как возвращенную"""
    try:
        with sqlite3.connect('library.db') as conn:
            cursor = conn.cursor()
            
            # Проверяем существование книги
            cursor.execute('SELECT available FROM books WHERE id = ?', (book_id,))
            result = cursor.fetchone()
            
            if result is None:
                print(f"Ошибка: Книга с ID {book_id} не найдена!")
                return
            
            if result[0] == 1:
                print("Книга уже в библиотеке!")
                return
            
            # Обновляем статус
            cursor.execute('UPDATE books SET available = 1 WHERE id = ?', (book_id,))
            conn.commit()
            print(f"Книга с ID {book_id} успешно возвращена!")
    except sqlite3.Error as e:
        print(f"Ошибка при возврате книги: {e}")


def delete_book(book_id):
    """Удаляет книгу из базы данных"""
    try:
        with sqlite3.connect('library.db') as conn:
            cursor = conn.cursor()
            
            # Проверяем существование книги
            cursor.execute('SELECT id FROM books WHERE id = ?', (book_id,))
            result = cursor.fetchone()
            
            if result is None:
                print(f"Ошибка: Книга с ID {book_id} не найдена!")
                return
            
            cursor.execute('DELETE FROM books WHERE id = ?', (book_id,))
            conn.commit()
            print(f"Книга с ID {book_id} успешно удалена!")
    except sqlite3.Error as e:
        print(f"Ошибка при удалении книги: {e}")


# Часть 3: Статистика и обработка ошибок

def get_statistics():
    """Выводит статистику по библиотеке"""
    try:
        with sqlite3.connect('library.db') as conn:
            cursor = conn.cursor()
            
            # Общее количество книг
            cursor.execute('SELECT COUNT(*) FROM books')
            total_books = cursor.fetchone()[0]
            
            # Количество доступных книг
            cursor.execute('SELECT COUNT(*) FROM books WHERE available = 1')
            available_books = cursor.fetchone()[0]
            
            # Количество выданных книг
            borrowed_books = total_books - available_books
            
            # Самый ранний и поздний год
            cursor.execute('SELECT MIN(year), MAX(year) FROM books')
            min_year, max_year = cursor.fetchone()
            
            print("\n=== Статистика библиотеки ===")
            print(f"Общее количество книг: {total_books}")
            print(f"Количество доступных книг: {available_books}")
            print(f"Количество выданных книг: {borrowed_books}")
            if min_year and max_year:
                print(f"Самый ранний год издания: {min_year}")
                print(f"Самый поздний год издания: {max_year}")
            print()
    except sqlite3.Error as e:
        print(f"Ошибка при получении статистики: {e}")


# Часть 4: Главная программа

def main():
    """Главная функция с меню"""
    create_library_database()
    
    # Добавляем начальные книги
    books_data = [
        ("Война и мир", "Л.Н. Толстой", 1869, "978-5-17-082549-6"),
        ("Преступление и наказание", "Ф.М. Достоевский", 1866, "978-5-17-082550-2"),
        ("Мастер и Маргарита", "М.А. Булгаков", 1967, "978-5-17-082551-9"),
        ("Анна Каренина", "Л.Н. Толстой", 1877, "978-5-17-082552-6"),
        ("Идиот", "Ф.М. Достоевский", 1869, "978-5-17-082553-3"),
        ("Евгений Онегин", "А.С. Пушкин", 1833, "978-5-17-082554-0"),
        ("Отцы и дети", "И.С. Тургенев", 1862, "978-5-17-082555-7")
    ]
    add_multiple_books(books_data)
    
    while True:
        print("\n=== Система учёта библиотеки ===")
        print("1. Показать все книги")
        print("2. Добавить книгу")
        print("3. Найти книги по автору")
        print("4. Найти книги по годам")
        print("5. Выдать книгу")
        print("6. Вернуть книгу")
        print("7. Удалить книгу")
        print("8. Показать статистику")
        print("0. Выход")
        
        choice = input("\nВыберите действие: ")
        
        if choice == "1":
            show_all_books()
        
        elif choice == "2":
            title = input("Введите название книги: ")
            author = input("Введите автора: ")
            year = int(input("Введите год издания: "))
            isbn = input("Введите ISBN: ")
            add_book(title, author, year, isbn)
        
        elif choice == "3":
            author = input("Введите имя автора: ")
            find_books_by_author(author)
        
        elif choice == "4":
            start_year = int(input("Введите начальный год: "))
            end_year = int(input("Введите конечный год: "))
            find_books_by_year_range(start_year, end_year)
        
        elif choice == "5":
            book_id = int(input("Введите ID книги: "))
            borrow_book(book_id)
        
        elif choice == "6":
            book_id = int(input("Введите ID книги: "))
            return_book(book_id)
        
        elif choice == "7":
            book_id = int(input("Введите ID книги: "))
            delete_book(book_id)
        
        elif choice == "8":
            get_statistics()
        
        elif choice == "0":
            print("До свидания!")
            break
        
        else:
            print("Неверный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()