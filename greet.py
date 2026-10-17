# Parent class 
class Person:
    def __init__(self, name, age): 
        self.name = name 
        self.age = age 

    def greet(self):
        print(f"Hello, I am {self.name}.") 

 # Child class — inherits Person 
class Student(Person):
    def __init__(self, name, age, school): 
        super().__init__(name, age) # call parent __init__ 
        self.school = school 

# OVERRIDE parent method 
    def greet(self): 
        print(f"Hi! I am {self.name}, a student at {self.school}.") 

p = Person("Mr Bello", 40) 
s = Student("Alex", 14, "Cityview Academy") 
p.greet() 
s.greet()
