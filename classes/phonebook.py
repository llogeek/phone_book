import pandas as pd
from csv import writer
class PhoneBook:

    """Инициализация обьекта класса телефонная книга. 
            При создании объекта инициализируется количество записей на странице (по умолчанию на странице до 10 записей).
            Указывается имя файла, в котором хранятся данные (файл .csv).
            Для хранения данных класс использует DataFrame."""
    def __init__(self:'PhoneBook', entries:'int' = 10, file_name:'str' = "phone_book.csv"):
        self.max_entries_page = entries
        self.file_name = file_name
        self.data = pd.read_csv(self.file_name) 
    
    """Функция преобразования данных в строковый формат."""
    def __str__(self:'PhoneBook') -> 'str':
        st = ""
        for i in range(0, len(self.data), self.max_entries_page):
            st += "Page #" + str(i // self.max_entries_page + 1) + "\n"
            st += self.data.iloc[i:(i+self.max_entries_page)].to_string(index=False) + '\n'
        return st
        
    """Функция добавления записей в телефонную книгу.
        Функция принимает некоторое количество именованных аргуменов (**kwargs)."""
    def insert(self:'PhoneBook', **kwargs):
        first_name = kwargs.get("first_name", "")
        middle_name = kwargs.get("middle_name", "")
        last_name = kwargs.get("last_name", "")
        organization = kwargs.get("organization", "")
        work_number = kwargs.get("work_number", "")
        personal_number = kwargs.get("personal_number", "") 
        data = [last_name, first_name, middle_name, organization, work_number, personal_number]
        self.data.loc[len(self.data)] = data
        self.add_to_csv(data=data)
    
    """Добавление записи в файл.
        Функция записывает данные списка в конец уже существующего файла с данными."""
    def add_to_csv(self:'PhoneBook', data:'list'):

        with open(self.file_name, 'a') as f_object:
            writer_object = writer(f_object)
            writer_object.writerow(data)
            f_object.close()
        
    """Перезапись данных в файл."""
    def write_to_csv(self:'PhoneBook'):
        self.data.to_csv(self.file_name, index=False)

    """Функция для получения DataFrame из других классов."""
    def get_data(self:'PhoneBook'):
        return self.data
    
    """Функция, которая по номеру поля возвращает его название."""
    @staticmethod
    def get_field_name(number:'int') -> 'str':
        if number == 1:
            return 'first_name'
        elif number == 2:
            return 'middle_name'
        elif number == 3:
            return 'last_name'
        elif number == 4:
            return 'organization'
        elif number == 5:
            return 'work_number'
        elif number == 6:
            return 'personal_number'
    
    """Функция поиска записей в заданном DataFrame result по полю под номером field_num и со значением value."""
    def search(self:'PhoneBook', result:'pd.DataFrame', field_num:'int', value:'str') -> 'pd.DataFrame':
        return result.loc[result[self.get_field_name(field_num)].str.fullmatch(value)]
    
    """Функция поиска записей в заданном DataFrame result по полю под номером field_num и с номером телефона value."""
    def search_phone(self:'PhoneBook', result:'pd.DataFrame', field_num:'int', value:'str') -> 'pd.DataFrame':
        return result.loc[result[self.get_field_name(field_num)] == value]
    
    """Поиск записи по значениям, заданным для всех полей в таблице."""
    def search_all(self:'PhoneBook', first_name:'str', middle_name:'str', last_name:'str', organization:'str', work_number:'str', personal_number:'str') -> 'pd.DataFrame':
        return self.data.loc[(self.data['first_name'].str.fullmatch(first_name)) &\
                             (self.data['middle_name'].str.fullmatch(middle_name)) &\
                             (self.data['last_name'].str.fullmatch(last_name))&\
                             (self.data['organization'].str.fullmatch(organization)) &\
                             (self.data['work_number'] == work_number)&\
                             (self.data['personal_number'] == personal_number)]
    
    """Редактирование записей. 
        Поиск записи осуществляется по полям Фамилия, Имя, Отчество, Название организации. 
        Для записи указывается строка с набором параметров, которые нужно отредактировать.
        После редактирования таблица данных в файле полностью перезаписывается."""
    def edit(self:'PhoneBook', first_name:'str', middle_name:'str', last_name:'str', organization:'str', edit_option:'str'):
        if len(self.data.loc[(self.data['first_name'].str.fullmatch(first_name)) &\
                             (self.data['middle_name'].str.fullmatch(middle_name)) &\
                             (self.data['last_name'].str.fullmatch(last_name))&\
                             (self.data['organization'].str.fullmatch(organization))]) == 0:
            print('No information.')
            return 
        if '1' in edit_option:
            new_first_name = input('New first name: ')
            self.data.loc[(self.data['first_name'].str.fullmatch(first_name)) &\
                             (self.data['middle_name'].str.fullmatch(middle_name)) &\
                             (self.data['last_name'].str.fullmatch(last_name))&\
                             (self.data['organization'].str.fullmatch(organization)), self.get_field_name(1)] = new_first_name
            first_name = new_first_name
        if '2' in edit_option:
            new_middle_name = input('New middle name: ')
            self.data.loc[(self.data['first_name'].str.fullmatch(first_name)) &\
                             (self.data['middle_name'].str.fullmatch(middle_name)) &\
                             (self.data['last_name'].str.fullmatch(last_name))&\
                             (self.data['organization'].str.fullmatch(organization)), self.get_field_name(2)] = new_middle_name
            middle_name = new_middle_name
        if '3' in edit_option:
            new_last_name = input('New last name: ')
            self.data.loc[(self.data['first_name'].str.fullmatch(first_name)) &\
                             (self.data['middle_name'].str.fullmatch(middle_name)) &\
                             (self.data['last_name'].str.fullmatch(last_name))&\
                             (self.data['organization'].str.fullmatch(organization)), self.get_field_name(3)] = new_last_name
            last_name = new_last_name
        if '4' in edit_option:
            new_organization = input('New organization name: ')
            self.data.loc[(self.data['first_name'].str.fullmatch(first_name)) &\
                             (self.data['middle_name'].str.fullmatch(middle_name)) &\
                             (self.data['last_name'].str.fullmatch(last_name))&\
                             (self.data['organization'].str.fullmatch(organization)), self.get_field_name(4)] = new_organization
            organization = new_organization
        if '5' in edit_option:
            new_work_number = input('New work phone number: ')
            self.data.loc[(self.data['first_name'].str.fullmatch(first_name)) &\
                             (self.data['middle_name'].str.fullmatch(middle_name)) &\
                             (self.data['last_name'].str.fullmatch(last_name))&\
                             (self.data['organization'].str.fullmatch(organization)), self.get_field_name(5)] = new_work_number
            
        if '6' in edit_option:
            new_personal_number = input('New personal phone number: ')
            self.data.loc[(self.data['first_name'].str.fullmatch(first_name)) &\
                             (self.data['middle_name'].str.fullmatch(middle_name)) &\
                             (self.data['last_name'].str.fullmatch(last_name))&\
                             (self.data['organization'].str.fullmatch(organization)), self.get_field_name(6)] = new_personal_number
        self.write_to_csv()
            