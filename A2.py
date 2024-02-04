import csv

class Employee:
    def __init__(self, employeeId, firstName, lastName, street, city, state, zip, phone, email):
        self.employeeId = employeeId
        self.firstName = firstName
        self.lastName = lastName
        self.street = street
        self.city = city
        self.state = state
        self.zip = zip
        self.phone = phone
        self.email = email

class HashTable:
    def __init__(self, size=10):
        self.size = size
        self.array = [None] * self.size

    def _hash(self, key, i=0):
        hash1 = hash(key) % self.size
        hash2 = 7 - (hash(key) % 7)
        return (hash1 + i * hash2) % self.size

    def _rehash(self):
        self.size *= 2
        old_array = self.array
        self.array = [None] * self.size
        for item in old_array:
            if item is not None:
                self.insert(item[0], item[1])

    def insert(self, key, value):
        index = self._hash(key)
        while self.array[index] is not None and self.array[index][0] != key:
            index = (index + 1) % self.size
        self.array[index] = (key, value)

        if self._load_factor() >= 0.75:
            self._rehash()

    def get(self, key):
        index = self._hash(key)
        while self.array[index] is not None:
            if self.array[index][0] == key:
                return self.array[index][1]
            index = (index + 1) % self.size
        raise KeyError(key)
        
    def remove(self, key):
        index = self._hash(key)
        i = 0
        while self.array[index] is not None:
            if self.array[index][0] == key:
                self.array[index] = None
                return
            i += 1
            index = self._hash(key, i)
        raise KeyError(key)

    def _load_factor(self):
        used_slots = sum(1 for item in self.array if item is not None)
        return used_slots / self.size

def read_and_create(filename):
    employees = HashTable()
    with open(filename, 'r', newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            employeeId, firstName, lastName, street, city, state, zip, phone, email = row
            employee = Employee(employeeId, firstName, lastName, street, city, state, zip, phone, email)
            employees.insert(employeeId, employee)
    return employees

filename = "us-contacts.csv"
employeeTable = read_and_create(filename)

userInput = input("Enter Employee ID to find employee: ")
try:
    employee = employeeTable.get(userInput)

    print("Employee found:")
    print(f"Employee ID: {employee.employeeId}")
    print(f"Name: {employee.firstName} {employee.lastName}")
    print(f"Address: {employee.street}, {employee.city}, {employee.state}, {employee.zip}")
    print(f"Phone: {employee.phone}")
    print(f"Email: {employee.email}")
    print()
except KeyError:
    print("Employee not found.")
    print()
    print()

userInput = input("Enter Employee ID to remove employee: ")
try:
    employee = employeeTable.remove(userInput)
    print("Employee " + userInput + " removed.")
    print()
except KeyError:
    print("Employee not found.")
    print()

userInput = input("Print Table? Y or N: ")
if userInput == "Y" or userInput == "y":
    print("          ID     Name                  Address                                  Phone          Email")
    for entry in employeeTable.array:
        if entry is not None:
            employee_id, employee = entry
            print(f"Employee: {employee.employeeId}, {employee.firstName} {employee.lastName}, {employee.street}, {employee.city}, {employee.state}, {employee.zip}, {employee.phone}, {employee.email}")
            print()
        else:
            print("-")
else:
    print("Table not printed...")
    print()
    print()
