from collections import UserDict
from datetime import datetime

class Field:
    def __init__(self, value):
        self.__value = None
        self.value = value


    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value


    def __str__(self):
        return str(self.value)
    
class Name(Field):
    pass

class Birthday(Field):
    def __init__(self, value):
        if not self.is_valid_birthday(value):
            raise ValueError("Invalid birthday")
        super().__init__(value)


    @Field.value.setter
    def value(self, value: str):
        if not self.is_valid_birthday(value):
            raise ValueError("Invalid birthday")
        self.__value = datetime.strptime(value, '%Y.%m.%d').date()

    @staticmethod
    def is_valid_birthday(value):
        try:
            datetime.strptime(value, '%Y.%m.%d')
            return True
        except ValueError:
            return False



class Phone(Field):
    def __init__(self, value):
        if not self.is_valid_phone(value):
            raise ValueError("Invalid phone number")
        super().__init__(value)

    
    @Field.value.setter
    def value(self, value: str):
        if not self.is_valid_phone(value):
            raise ValueError("Invalid phone number")
        self.__value = value


    @staticmethod
    def is_valid_phone(value):
        return isinstance(value, str) and len(value) == 10 and value.isdigit()
    

class Record:
    def __init__(self, name, birthday = None):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday) if birthday else None


    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(str(p) for p in self.phones)}"
    

    def days_to_birthday(self):
        if self.birthday:
            today = datetime.now().date()
            next_birthday = self.birthday.value.replace(year=today.year)
            if next_birthday < today:
                next_birthday = next_birthday.replace(year=today.year + 1)
            return (next_birthday - today).days
        else:
            return None
    

    def add_phone(self, phone_number: str):
        phone = Phone(phone_number)
        if not phone.is_valid_phone(phone.value):
            raise ValueError("Invalid phone number")
        if phone not in self.phones:
            self.phones.append(phone)


    def find_phone(self, phone_number: str):
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return None
    

    def edit_phone(self, old_phone, new_phone):
        phone_found = False
        for i, phone in enumerate(self.phones):
            if phone.value == old_phone:
                new_phone_obj = Phone(new_phone)
                if not phone.value:
                    raise ValueError("Invalid phone number")
                self.phones[i] = new_phone_obj
                phone_found = True
                break 
        if not phone_found:
            raise ValueError("Phone number not found in the list")


    def remove_phone(self, phone):
        for ph in self.phones:
            if ph.value == phone:
                self.phones.remove(ph)
                break


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        if name in self.data:
            return self.data[name]
        else:
            return None
        
    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def iterator(self, item_number):
        counter = 0
        result = ''
        for item, record in self.data.items():
            result += f'{item}: {record}'
            counter += 1
            if counter >= item_number:
                yield result
                counter = 0
                result = ''