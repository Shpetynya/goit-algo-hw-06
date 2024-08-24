from collections import UserDict
import re


class Field:
    """Базовий клас для полів запису."""
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    """Клас для зберігання імені контакту."""
    def __init__(self, name):
        super().__init__(name)


class Phone(Field):
    """Клас для зберігання номера телефону."""
    def __init__(self, phone):
        if not self.validate_phone(phone):
            raise ValueError("Phone number must be 10 digits.")
        super().__init__(phone)

    @staticmethod
    def validate_phone(phone):
        """Перевіряє, чи номер телефону складається з 10 цифр."""
        return bool(re.fullmatch(r'\d{10}', phone))


class Record:
    """Клас для зберігання інформації про контакт, включаючи ім'я та список телефонів."""
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone_number: str):
        """Додає телефон до списку телефонів."""
        phone = Phone(phone_number)
        self.phones.append(phone)

    def remove_phone(self, phone_number: str):
        """Видаляє телефон зі списку телефонів."""
        phone_to_remove = self.find_phone(phone_number)
        if phone_to_remove:
            self.phones.remove(phone_to_remove)

    def edit_phone(self, old_phone_number: str, new_phone_number: str):
        """Редагує існуючий телефон."""
        old_phone = self.find_phone(old_phone_number)
        if old_phone:
            self.remove_phone(old_phone_number)
            self.add_phone(new_phone_number)
        else:
            raise ValueError(f"Phone number {old_phone_number} not found.")

    def find_phone(self, phone_number: str):
        """Повертає телефон, якщо він є в списку."""
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    """Клас для управління записами в адресній книзі."""

    def add_record(self, record: Record):
        """Додає запис до адресної книги."""
        self.data[record.name.value] = record

    def find(self, name: str):
        """Знаходить запис за ім'ям."""
        return self.data.get(name, None)

    def delete(self, name: str):
        """Видаляє запис з адресної книги за ім'ям."""
        if name in self.data:
            del self.data[name]

    def __str__(self):
        return "\n".join(str(record) for record in self.data.values())




# Створення нової адресної книги
book = AddressBook()

    # Створення запису для John
john_record = Record("John")
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")

    # Додавання запису John до адресної книги
book.add_record(john_record)

    # Створення та додавання нового запису для Jane
jane_record = Record("Jane")
jane_record.add_phone("9876543210")
book.add_record(jane_record)

    # Виведення всіх записів у книзі
     
print(book)

    # Знаходження та редагування телефону для John
john = book.find("John")
john.edit_phone("1234567890", "1112223333")

print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

    # Пошук конкретного телефону у записі John
found_phone = john.find_phone("5555555555")
print(f"{john.name}: {found_phone}")  # Виведення: John: 5555555555

    # Видалення запису Jane
book.delete("Jane")
print(book)
