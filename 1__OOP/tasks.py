

"""
Задание 1. Инкапсуляция
Создайте класс BankAccount, который инкапсулирует данные о балансе.
Реализуйте методы:
 - deposit(amount) — пополнение счёта;
 - withdraw(amount) — снятие средств (не должно позволять уйти в минус);
 - get_balance() — получить текущий баланс.
Баланс должен быть защищён от прямого изменения (например, self.__balance).
"""


class BankAccount:
    def __init__(self):
        self.__balance: int = 0

    def get_balance(self) -> int:
        return self.__balance

    def deposit(self, amount: int) -> None:
        self.__balance += amount

    def withdraw(self, amount: int) -> None:
        if amount > self.__balance:
            raise ValueError("Недостаточно средств")
        self.__balance -= amount\



"""
Задание 2. Наследование
Создайте базовый класс Employee с атрибутами name, position, salary и методом get_info().
Создайте подклассы:
 - Developer, у которого есть доп. атрибут programming_language;
 - Manager, у которого есть список подчинённых (employees).

Каждый подкласс должен переопределять метод get_info().
"""


class Employee:
    def __init__(self, name: str, position: str, salary: int):
        self.name: str = name
        self.position: str = position
        self.salary: int = salary

    def get_info(self):
        return f"{self.name}, {self.position}, {self.salary}"


class Developer(Employee):
    def __init__(self, name: str, position: str, salary: int, programming_language: str):
        super().__init__(name, position, salary)
        self.programming_language: str = programming_language

    def get_info(self):
        return f"{self.name}, {self.position}, {self.salary}, {self.programming_language}"


class Manager(Employee):
    def __init__(self, name: str, position: str, salary: int, employees: list[Employee]):
        super().__init__(name, position, salary)
        self.employees: list[Employee] = employees

    def get_info(self):
        return f"{self.name}, {self.position}, {self.salary}, {self.employees}"


"""
Задание 3. Полиморфизм
Создайте базовый класс Shape с методом area() и perimeter() (возвращает 0 по умолчанию).
Создайте подклассы:
 - Rectangle (по width, height);
 - Circle (по radius).

Продемонстрируйте работу полиморфизма: создайте список фигур и выведите площадь и периметр каждой из них с помощью одного и того же кода.
"""


class Shape:
    def area(self) -> int | float:
        return 0

    def perimeter(self) -> int | float:
        return 0


class Rectangle(Shape):
    def __init__(self, width: int, height: int):
        self.width: int = width
        self.height: int = height

    def area(self) -> int | float:
        return self.width * self.height

    def perimeter(self) -> int | float:
        return (2 * self.width) + (2 * self.height)


class Circle(Shape):
    def __init__(self, radius: int):
        self.radius: int = radius

    def area(self) -> int | float:
        return round(3.14 * (self.radius ** 2), 2)

    def perimeter(self) -> int | float:
        return round(2 * 3.14 * self.radius, 2)


figures: list[Shape] = [
    Rectangle(10, 20),
    Rectangle(5, 10),
    Circle(5),
    Circle(10),
]

print("\n\n--- Task 3 ---")
for figure in figures:
    print(
        f"Figure: {figure.__class__.__name__}, "
        f"Area: {figure.area()}, "
        f"Perimeter: {figure.perimeter()}")


"""
Задание 4. Абстракция и интерфейс
Используйте модуль abc.
Создайте абстрактный класс Transport с абстрактными методами:
 - start_engine(),
 - stop_engine(),
 - move().
Создайте классы Car и Boat, реализующие интерфейс Transport.
"""


from abc import ABC, abstractmethod


class Transport(ABC):
    @abstractmethod
    def start_engine(self):
        pass

    @abstractmethod
    def stop_engine(self):
        pass

    @abstractmethod
    def move(self):
        pass


class Car(Transport):
    def start_engine(self):
        print("Машина заведена")

    def stop_engine(self):
        print("Машина заглушена")

    def move(self):
        print("Машина едет")


class Boat(Transport):
    def start_engine(self):
        print("Лодка заведена")

    def stop_engine(self):
        print("Лодка заглушена")

    def move(self):
        print("Лодка едет")


"""
Задание 5. Множественное наследование
Создайте два класса:
 - Flyable, с методом fly() (выводит I'm flying!);
 - Swimmable, с методом swim() (выводит I'm swimming!).

Создайте класс Duck, наследующий оба класса. Добавьте метод make_sound() (выводит Quack!).
Создайте экземпляр Duck и вызовите все три метода.
"""


class Flyable(ABC):
    def fly(self):
        print("I'm flying!")


class Swimmable(ABC):
    def swim(self):
        print("I'm swimming!")


class Duck(Flyable, Swimmable):
    def make_sound(self):
        print("Quack!")


print("\n\n--- Task 5 ---")
duck = Duck()
duck.fly()
duck.swim()
duck.make_sound()


"""
(Дополнительно) Задание 6. Комбинированное: Зоопарк
Создайте абстрактный класс Animal с методами speak() и move().
Создайте классы Dog, Bird, Fish. Пусть:
 - Dog говорит "Woof!" и бегает,
 - Bird говорит "Tweet!" и летает (наследует Flyable),
 - Fish молчит и плавает (наследует Swimmable).

Положите всех животных в один список и вызовите методы speak() и move() в цикле.
"""


class Animal(ABC):
    @abstractmethod
    def speak(self):
        pass

    @abstractmethod
    def move(self):
        pass


class Dog(Animal):
    def speak(self):
        print("Woof!")

    def move(self):
        print("Dog is running")


class Bird(Animal, Flyable):
    def speak(self):
        print("Tweet!")

    def move(self):
        self.fly()


class Fish(Animal, Swimmable):
    def speak(self):
        print("...")

    def move(self):
        self.swim()


animals: list[Animal] = [Dog(), Bird(), Fish()]

print("\n\n--- Task 6 ---")
for animal in animals:
    animal.speak()
    animal.move()

