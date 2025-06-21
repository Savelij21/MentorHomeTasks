"""
1. Singleton

Условия:
Реализуйте класс Logger с использованием паттерна Singleton, чтобы гарантировать,
что в программе существует только один экземпляр логгера.
Класс должен:
 - Иметь метод log(self, message: str), который добавляет сообщение в список логов.
 - Иметь метод get_logs(self), который возвращает список всех сообщений.
Покажите, что два экземпляра Logger — это один и тот же объект.
Технические требования:
 - Реализация должна быть написана вручную, не использовать сторонние библиотеки.
 - Singleton можно реализовать через __new__, декоратор или метакласс (на выбор).

Пример использования

logger1 = Logger()
logger2 = Logger()

logger1.log("First message")
logger2.log("Second message")

assert logger1 is logger2, "Logger is not a singleton!"
assert logger1.get_logs() == ["First message", "Second message"]

"""
from abc import ABC, abstractmethod
from typing import Self


class Logger:
    __instance = None
    __logs: list[str] = []

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def log(self, message: str):
        self.__logs.append(message)

    def get_logs(self):
        return self.__logs


logger1 = Logger()
logger2 = Logger()

logger1.log("First message")
logger2.log("Second message")

print("--- Task 1 ---")
assert logger1 is logger2, "Logger is not a singleton!"
assert logger1.get_logs() == ["First message", "Second message"]


"""
2. SOLID (S)

У вас есть класс Report, который:
 - хранит данные отчета,
 - генерирует его в PDF,
 - сохраняет на диск.
Разделите этот класс на части, каждая из которых будет отвечать только за одну ответственность.

class Report:
    def __init__(self, title, content):
        self.title = title
        self.content = content
    def generate_pdf(self):
        print("PDF generated")
    def save_to_file(self, filename):
        print(f"Saved {filename}")

"""


class Report:
    def __init__(self, title, content):
        self.title = title
        self.content = content


class PDFGenerator:
    def generate_pdf(self, report: Report):
        # Логика с report
        print("PDF generated")


class SaverToFile:
    def save_to_file(self, report: Report, filename):
        # Логика с report
        print(f"Saved {filename}")


"""
3. SOLID (O)

Реализуйте систему оплаты: базовый класс PaymentProcessor, у которого есть метод pay().
Добавьте поддержку разных способов оплаты (PayPal, CreditCard, Crypto) без изменения базового кода.
Цель: Использовать полиморфизм или абстракции (например, через ABC).

"""


# -- base --
class PaymentSystem(ABC):
    @abstractmethod
    def pay(self):
        pass


class PaymentProcessor:

    def pay(self, payment_system: PaymentSystem):
        payment_system.pay()


# -- implementations --
class PayPal(PaymentSystem):
    def pay(self):
        print("PayPal payment processed.")


class CreditCard(PaymentSystem):
    def pay(self):
        print("CreditCard payment processed.")


class Crypto(PaymentSystem):
    def pay(self):
        print("Crypto payment processed.")


print("\n\n--- Task 3 ---")

payment_systems: list[PaymentSystem] = [PayPal(), CreditCard(), Crypto()]
payment_processor = PaymentProcessor()
for ps in payment_systems:
    payment_processor.pay(ps)


"""
4. SOLID (L)

Реализуйте класс Bird и подклассы Sparrow и Penguin.
Убедитесь, что замена Bird на любой его подкласс не ломает код.
"""


class Bird(ABC):
    @abstractmethod
    def fly(self):
        pass


class Sparrow(Bird):
    def fly(self):
        print("Sparrow is flying!")


class Penguin(Bird):
    def fly(self):
        print("Penguin can't fly :(")


"""
5. SOLID (I)

Представьте интерфейс Animal с методами: fly(), run(), swim().
Реализуйте Lion(), которая умеет только бегать, не заставляя её реализовывать ненужные методы.

------------------- !!! ---------------------------- 
Не совсем понял - нужно ли наследовать Lion от Animal?
Если мы Интерфейсами называем абстрактные классы, у которых все методы - абстрактные,
то по требованию задачи я не могу наследовать Lion от Animal, так как мне придется реализовывать
не нужные методы в Lion. Либо же я делаю Animal абстрактным классом, у которого методы уже не абстрактные
и мне в Lion не нужно реализовывать ненужные методы.

Крч говоря я сделал так, как я сделал бы в проекте - Lion наследуется от интерфейса только с нужным ему
методом, Animal (как по требованию задачи) реализует все нужные методы.
------------------- !!! ---------------------------- 

"""


class Flyable(ABC):
    @abstractmethod
    def fly(self):
        pass


class Runnable(ABC):
    @abstractmethod
    def run(self):
        pass


class Swimmable(ABC):
    @abstractmethod
    def swim(self):
        pass


class Animal(Flyable, Runnable, Swimmable):
    def fly(self):
        pass

    def run(self):
        pass

    def swim(self):
        pass


class Lion(Runnable):
    def run(self):
        print("Lion is running!")


"""
6. staticmethod, classmethod, property

Создайте класс Temperature, который хранит температуру в градусах Цельсия, но:
 - умеет создавать объект из градусов Фаренгейта (@classmethod),
 - вычисляет температуру в Кельвинах как свойство (@property),
 - предоставляет статический метод для проверки, является ли температура точкой замерзания воды (0°C или ниже).

"""


class Temperature:
    def __init__(self, degrees_celsius: float):
        self.degrees_celsius: float = round(degrees_celsius, 2)

    @classmethod
    def from_fahrenheit(cls, degrees_fahrenheit: float) -> Self:
        _degrees_celsius: float = (degrees_fahrenheit - 32) * 5 / 9
        return cls(_degrees_celsius)

    @property
    def kelvins(self) -> float:
        return self.degrees_celsius + 273.15

    @staticmethod
    def is_water_freezing(degrees_celsius: int) -> bool:
        return degrees_celsius <= 0


