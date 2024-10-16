import json
import xml.etree.ElementTree as ET
from xml.dom import minidom
from typing import List, Optional

def iinput(text: str, type_date: str = "str") -> str:
    while True:
        trash = input(text)
        if trash != "" and type_date == "str":
            break
        if type_date == "int":
            try:
                int(trash)
            except Exception as e:
                print("Это не число!")
            else:
                break
        print("Попробуйте еще раз:\n")
            
    return trash

#1)
class Author:
    def __init__(self, name: str = "", books: Optional[List['Book']] = None) -> None:
        self.name = name if name else iinput("Введите имя автора: \n")
        self.books: List[Book] = books if books is not None else []
    
    def add_book(self, book: 'Book'):
        self.books.append(book)

#2)
class Genre:
    def __init__(self, name: str = "", books: Optional[List['Book']] = None) -> None:
        self.name = name if name else iinput("Введите название жанра: \n")
        self.books: List[Book] = books if books is not None else []
    
    def add_book(self, book: 'Book'):
        self.books.append(book)

#3)Book 
class Book:
    def __init__(self, price: int, title: str = "", author: Optional[Author] = None, genre: Optional['Genre'] = None, feedback: Optional[List['Feedback']] = None) -> None:
        self.price = price 
        self.title = title if title else iinput("Введите название книги: \n")
        self.feedbacks: List[Feedback] = feedback if feedback is not None else []

        self.genre: Genre = genre if genre is not None else Genre()
        if self not in self.genre.books : self.genre.add_book(self) 

        self.author = author if author is not None else Author()
        if self not in self.author.books : self.author.add_book(self)

#4)
class Basket:
    def __init__(self, books: Optional[List[Book]] = None) -> None:
        self.books: List[Book] = books if books is not None else []
    
    def add_book(self, book: Book):
        self.books.append(book)

#5
class PurchasedBooks(Basket):
    def __init__(self, date: str = "", books: Optional[List[Book]] = None) -> None:
        super().__init__(books)
        self.date = date if date else iinput("Введите дату покупки: ") 

#6)
class Addres:
    def __init__(self, country: str = "", city: str = "", street: str = "", house: str = "", apartN: str = "") -> None:
        self.country = country if country else iinput("Введите страну: ")
        self.city = city if city else iinput("Введите город: ")
        self.street = street if street else iinput("Введите улицу: ")
        self.house = house if house else iinput("Введите дом: ")
        self.apartN = apartN if apartN else iinput("Введите номер квартиры: ", "int")

#7)
class Customer:
    def __init__(self, name: str = "", basket: Optional[Basket] = None, address: Optional[Addres] = None) -> None:
        self.name = name if name else iinput("Введите имя покупателя: /n")
        self.basket = basket if basket is not None else Basket()
        self.address = address if address is not None else Addres()
        self.purchasedBook =  PurchasedBooks()
        

#8)
class Grade:
    def __init__(self, grade: str = "") -> None:
        grade = grade if grade else iinput("Введите оценку книги от 1 до 5: ")
        gradeInt = 0
        while True:
            try:
                gradeInt = int(grade) 
                if 1 <= int(grade) <= 5:
                    gradeInt = int(grade)
                    break
            except Exception as e:
                print("\n Это не число!")
            grade = iinput("Введите число еще раз: \n")
        
        self.grade = gradeInt

#9)
class Feedback:
    def __init__(self, text: str = "", grade: Grade = None):
        self.text = text if text else iinput("Введите текст отзыва: ")
        self.grade = grade if grade is not None else Grade()

#10)
class Publisher(Basket):
    def __init__(self, books: Optional[List[Book]] = None, name: str = "") -> None:
        super().__init__(books)
        self.name = name if name else iinput("Введите название издательства: \n")

# Функция для сохранения данных в JSON файл
def save_to_json(authors, genres, books, customers, feedbacks, filename="data.json"):
    data = {
        "authors": [{"name": author.name, "books": [book.title for book in author.books]} for author in authors],
        "genres": [{"name": genre.name, "books": [book.title for book in genre.books]} for genre in genres],
        "books": [{"title": book.title, "price": book.price, "author": book.author.name, "genre": book.genre.name} for book in books],
        "customers": [{"name": customer.name, "address": vars(customer.address), "basket": [book.title for book in customer.basket.books]} for customer in customers],
        "feedbacks": [{"text": feedback.text, "grade": feedback.grade.grade} for feedback in feedbacks]
    }

    try:
        with open(filename, 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        existing_data = {}

    # Объединение с новыми данными
    for key in data:
        if key in existing_data:
            existing_data[key].extend(data[key])
        else:
            existing_data[key] = data[key]
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=4)
    print(f"Данные успешно сохранены в {filename}")

# Функция для удаления данных из JSON файла
def clear_data_from_json(keys_to_remove, filename="data.json"):
    try:
        with open(filename, 'r+', encoding='utf-8') as f:
            data = json.load(f)
            for key in keys_to_remove:
                if key in data:
                    del data[key]
            f.seek(0) # Указатель на начало файла
            f.truncate()  # Очистка файла перед записью новых данных
            json.dump(data, f, ensure_ascii=False, indent=4)
        print("Данные успешно удалены из файла.")
    except (FileNotFoundError, json.JSONDecodeError):
        print("Файл не найден или он пуст.")

# Функция для сохранения данных в XML файл с отступами и переносами строк
def save_to_xml(authors, genres, books, customers, feedbacks, filename="data.xml"):
    root = ET.Element("data")

    authors_elem = ET.SubElement(root, "authors")
    for author in authors:
        author_elem = ET.SubElement(authors_elem, "author", name=author.name)
        for book in author.books:
            ET.SubElement(author_elem, "book", title=book.title)

    genres_elem = ET.SubElement(root, "genres")
    for genre in genres:
        genre_elem = ET.SubElement(genres_elem, "genre", name=genre.name)
        for book in genre.books:
            ET.SubElement(genre_elem, "book", title=book.title)

    books_elem = ET.SubElement(root, "books")
    for book in books:
        book_elem = ET.SubElement(books_elem, "book", title=book.title)
        ET.SubElement(book_elem, "price").text = str(book.price)
        ET.SubElement(book_elem, "author").text = book.author.name
        ET.SubElement(book_elem, "genre").text = book.genre.name

    customers_elem = ET.SubElement(root, "customers")
    for customer in customers:
        customer_elem = ET.SubElement(customers_elem, "customer", name=customer.name)
        address_elem = ET.SubElement(customer_elem, "address")
        for key, value in vars(customer.address).items():
            ET.SubElement(address_elem, key).text = str(value)
        basket_elem = ET.SubElement(customer_elem, "basket")
        for book in customer.basket.books:
            ET.SubElement(basket_elem, "book", title=book.title)

    feedbacks_elem = ET.SubElement(root, "feedbacks")
    for feedback in feedbacks:
        feedback_elem = ET.SubElement(feedbacks_elem, "feedback")
        ET.SubElement(feedback_elem, "text").text = feedback.text
        ET.SubElement(feedback_elem, "grade").text = str(feedback.grade.grade)

    # Преобразование в строку с форматированием
    xml_str = ET.tostring(root, encoding="utf-8")
    parsed_str = minidom.parseString(xml_str)
    pretty_xml = parsed_str.toprettyxml(indent="  ")

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(pretty_xml)

    print(f"Данные успешно сохранены в {filename}")

# Функция для удаления данных из XML файла
def clear_data_from_xml(keys_to_remove, filename="data.xml"):
    try:
        tree = ET.parse(filename)
        root = tree.getroot()

        for key in keys_to_remove:
            elements = root.findall(key)
            for element in elements:
                root.remove(element)

        tree.write(filename, encoding="utf-8", xml_declaration=True)
        print("Данные успешно удалены из XML файла.")
    except FileNotFoundError:
        print("Файл не найден.")
    except ET.ParseError:
        print("Ошибка при парсинге XML файла.")

def main():
    arr_author: List[Author] = []
    arr_genre: List[Genre] = []
    arr_book: List[Book] = []
    arr_customer: List[Customer] = []
    arr_feedback: List[Feedback] = []
    while True:
        choice = int(iinput("1)Создай автора книги\n2)Создать жанр книги\n3)Создать книгу\n4)Создать покупателя \n5)Создать отзыв\n6) Загрузить данные в файл json \n7)Удалить данные в файле json\n8)Загрузить данные в xml\n9)Удалить данные xml\n10)Выйти\n", "int"))
        if choice == 1:
            createAuthor = Author()
            arr_author.append(createAuthor)
            continue
        elif choice == 2:
            createGenre = Genre()
            arr_genre.append(createGenre) 
            continue
        elif choice == 3:
            createBook = Book(price=int(iinput("Введите цену книги: ", "int")))
            arr_book.append(createBook)
            continue
        elif choice == 4:
            createCustomer = Customer()
            arr_customer.append(createCustomer)
            continue
        elif choice == 5:
            createFeedback = Feedback()
            arr_feedback.append(createFeedback)
            continue
        elif choice == 6:
            save_to_json(arr_author, arr_genre, arr_book, arr_customer, arr_feedback)
            continue
        elif choice == 7:
            keys_to_remove = ["authors", "genres", "books", "customers", "feedbacks"]
            clear_data_from_json(keys_to_remove)
            continue
        elif choice == 8:
            save_to_xml(arr_author, arr_genre, arr_book, arr_customer, arr_feedback)
            continue
        elif choice == 9: 
            keys_to_remove = ["authors", "genres", "books", "customers", "feedbacks"]
            clear_data_from_xml(keys_to_remove)
            continue
        elif choice == 10:
            break
        else:
            print("Ошибочный ввод, введите еще раз!")
            continue

if __name__ == "__main__":
    main()