from collections import UserDict

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)
    
class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        if not self.is_valid_phone(value):
            raise ValueError("Invalid phone number")
        super().__init__(value)


    @staticmethod
    def is_valid_phone(value):
        return isinstance(value, str) and len(value) == 10 and value.isdigit()
    

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(str(p) for p in self.phones)}"
    

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