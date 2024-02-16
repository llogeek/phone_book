import re
from classes.phonebook import PhoneBook

"""Класс Interface создан для взаимодействия пользователя с классом PhoneBook"""
class  Interface:
    
    """Создание объекта телефоннная книга. page_entries: количество записей на странице \
        (по умолчанию на каждой странице подразумевается наличие до 10 записей)"""
    def __init__(self:'Interface', page_entries:'int'=10, file_name:'str' = "phone_book2.csv"):
        self.phone_book = PhoneBook(page_entries, file_name)
    
    """Функция для вывода возможных опций меню"""
    def welcome(self:'Interface'):
        data = 1
        while data != 5:
            data = int(input("""
                    Options:\n\
                         1. Add entry\n\
                         2. Edit entry\n\
                         3. Print all entries\n\
                         4. Search entry\n\
                         5. Exit\n"""))
            self.process_menu(data)
        
    """Печать телефонной книги"""
    def print_data(self:'Interface'):
        print(str(self.phone_book))
    
    """Функция обпработки запросов пользователей: 
                                    1 - добавление записи,
                                    2 - редактирование записей
                                    3 - вывод телефонной книги
                                    4 - поиск в телефонной книге"""
    def process_menu(self:'Interface', option:'int'):
        if option == 1:
            self.add_data()
        elif option == 2:
            self.edit()
        elif option == 3:
            self.print_data()
        elif option == 4:
            self.search()
    
    """Добавление записи. 
            Выполняется проверка того, что данные ФИО не являются пустыми. 
            Проверяется формат рабочего и мобильного номера.
            Проверяется наличие одинаковых записей для избежания дублирования."""
    """Данные номера могут быть введены следующим образом:
       8 (3 цифры) (7-10 цифр пробелов или -)
       8-(3 цифры)-(7-10 цифр пробелов или -)
       7 (3 цифры) (7-10 цифр пробелов или -)
       7-(3 цифры)-(7-10 цифр пробелов или -)"""
    def add_data(self:'Interface'):
        print("Fill in the form:")
        first_name = input("First name: ")
        middle_name = input("Middle name: ")
        last_name  = input("Last name: ")
        organization = input("Organization name: ")
        work_number = input("Work phone number: ")
        personal_number = input("Personal number: ")
        if first_name == "" and middle_name == "" and last_name == "":
            print('User data is empty')
            return
        validate_phone_number_pattern = "^((8|7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$"
        if not re.match(validate_phone_number_pattern, work_number) or not re.match(validate_phone_number_pattern, personal_number):
            print('Phone number must follow the rules numbers!')
            return
        if len(self.phone_book.search_all(first_name, middle_name, last_name, organization, work_number, personal_number).index) != 0:
            print('Such record already exists!')
            return 
        self.phone_book.insert(first_name = first_name, middle_name = middle_name, last_name = last_name, \
                organization = organization,\
                      work_number = work_number,
                          personal_number = personal_number)
    
    """Редактирование записей в телефонной книге"""
    def edit(self:'Interface'):
        edit_option = input("""
                        Choose values to edit (input in 1 row with space):
                        1. First name.
                        2. Middle_name.
                        3. Last name.
                        4. Organization.
                        5. Work phone number.
                        6. Personal phone number.\n""")
        print("Fill the form to find contact")
        first_name = input('First name: ')
        middle_name = input('Middle name: ')
        last_name = input('Last name: ')
        organization = input('Organization name: ')
        self.phone_book.edit(first_name, middle_name, last_name, organization, edit_option)

        
    "Поиск записи в телефонной книге"
    def search(self:'Interface'):
        search_option = input("""
                        Choose values to search (input in 1 row with space):
                        1. First name.
                        2. Middle_name.
                        3. Last name.
                        4. Organization.
                        5. Work phone number.
                        6. Personal phone number.\n""")
        result = self.phone_book.get_data()
        if '1' in search_option:
            first_name = input('First name for search: ')
            result = self.phone_book.search(result, 1, first_name)
        if '2' in search_option:
            middle_name = input('Middle name for search: ')
            result = self.phone_book.search(result, 2, middle_name)
        if '3' in search_option:
            last_name = input('Last name for search: ')
            result = self.phone_book.search(result, 3, last_name)
        if '4' in search_option:
            organization = input('Organization name for search: ')
            result = self.phone_book.search(result, 4, organization)
        if '5' in search_option:
            work_number = input('Work phone number for search (without '"+"'): ')
            result = self.phone_book.search_phone(result, 5, work_number)
        if '6' in search_option:
            personal_number = input('Personal phone number for search (without '"+"'): ')
            result = self.phone_book.search_phone(result, 6, personal_number)
        if len(result) != 0:
            print(result.to_string(index = False))
        else:
            print("Results not found.")
        return result