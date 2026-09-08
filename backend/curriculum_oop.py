# -*- coding: utf-8 -*-
"""
Curriculum definition for Object-Oriented Design & Design Patterns.
Comprehensive 9-module curriculum covering OOP fundamentals, SOLID principles, Gang of Four (GoF)
creational, structural, and behavioral patterns, domain modeling, and enterprise architecture.
"""

OOP_COURSE = {
    "title": "Object-Oriented Design & Design Patterns",
    "slug": "object-oriented-design-patterns",
    "description": "Master SOLID principles, GoF design patterns, domain modeling, clean code architecture, and scalable software design.",
    "category": "software-engineering",
    "level": "intermediate",
    "duration_weeks": 10,
    "thumbnail_gradient": "from-violet-600 via-purple-700 to-indigo-900",
    "is_featured": True,
    "modules": [
        {
            "order": 1,
            "title": "The Four Pillars of Object-Oriented Programming",
            "description": "Encapsulation, Abstraction, Inheritance, and Polymorphism applied to clean software architecture.",
            "chapters": [
                {
                    "order": 1,
                    "title": "Encapsulation, Data Hiding & Invariants",
                    "description": "Protect internal object state, enforce class invariants, and eliminate anemic domain models.",
                    "duration_minutes": 35,
                    "content": """# Encapsulation & Class Invariants

Encapsulation bundles data (attributes) and behavior (methods) while restricting direct external access to internal state.

```python
class BankAccount:
    def __init__(self, account_id: str, initial_balance: float = 0.0):
        if initial_balance < 0:
            raise ValueError("Initial balance cannot be negative")
        self._account_id = account_id
        self._balance = initial_balance  # Encapsulated state

    @property
    def balance(self) -> float:
        return self._balance

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self._balance += amount

    def withdraw(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if amount > self._balance:
            raise ValueError("Insufficient funds")
        self._balance -= amount
```

## Key Takeaways
- Encapsulation prevents invalid state transitions and guarantees object integrity at all times."""
                },
                {
                    "order": 2,
                    "title": "Polymorphism & Dynamic Dispatch",
                    "description": "Master subtype polymorphism, virtual method dispatch tables (vtable), and interface contracts.",
                    "duration_minutes": 40,
                    "content": """# Subtype Polymorphism & Dynamic Dispatch

Polymorphism allows objects of different subtypes to respond to identical method invocations with specialized behaviors.

```python
from abc import ABC, abstractmethod

class PaymentGateway(ABC):
    @abstractmethod
    def process_payment(self, amount: float) -> bool:
        pass

class StripePaymentGateway(PaymentGateway):
    def process_payment(self, amount: float) -> bool:
        print(f"Authorizing Stripe charge for ${amount:.2f}")
        return True

class PayPalPaymentGateway(PaymentGateway):
    def process_payment(self, amount: float) -> bool:
        print(f"Redirecting to PayPal checkout for ${amount:.2f}")
        return True

def checkout(gateway: PaymentGateway, total: float):
    # Dynamic polymorphism: callers depend on abstraction, not concrete implementations
    if gateway.process_payment(total):
        print("Order confirmed successfully!")
```

## Key Takeaways
- Program to an interface, not an implementation."""
                }
            ]
        },
        {
            "order": 2,
            "title": "The SOLID Principles of Clean Architecture",
            "description": "Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, and Dependency Inversion.",
            "chapters": [
                {
                    "order": 1,
                    "title": "Single Responsibility & Open/Closed Principles",
                    "description": "Refactor monolithic god-classes and design extensible systems via strategy composition.",
                    "duration_minutes": 45,
                    "content": """# SRP & Open/Closed Principles

## 1. Single Responsibility Principle (SRP)
A class should have one, and only one, reason to change (one actor/stakeholder).

## 2. Open/Closed Principle (OCP)
Software entities (classes, modules, functions) should be open for extension, but closed for modification.

```python
from abc import ABC, abstractmethod

class TaxStrategy(ABC):
    @abstractmethod
    def calculate(self, amount: float) -> float:
        pass

class USTax(TaxStrategy):
    def calculate(self, amount: float) -> float:
        return amount * 0.08

class EUTax(TaxStrategy):
    def calculate(self, amount: float) -> float:
        return amount * 0.20

class OrderProcessor:
    def __init__(self, tax_strategy: TaxStrategy):
        self._tax_strategy = tax_strategy

    def calculate_total(self, subtotal: float) -> float:
        tax = self._tax_strategy.calculate(subtotal)
        return subtotal + tax
```

## Key Takeaways
- Adding a new country tax does NOT require modifying `OrderProcessor`, satisfying OCP."""
                },
                {
                    "order": 2,
                    "title": "LSP, ISP & Dependency Inversion (DIP)",
                    "description": "Substitutability contracts, narrow interface segregation, and IoC dependency injection.",
                    "duration_minutes": 45,
                    "content": """# LSP, ISP & Dependency Inversion

## 1. Liskov Substitution Principle (LSP)
Subtypes must be substitutable for their base types without altering program correctness (Square/Rectangle problem).

## 2. Interface Segregation Principle (ISP)
Clients should not be forced to depend on interfaces they do not use.

## 3. Dependency Inversion Principle (DIP)
High-level modules should not depend on low-level modules. Both should depend on abstractions.

```python
# DIP: High-level notification service depends on NotificationSender abstraction
class NotificationSender(ABC):
    @abstractmethod
    def send(self, recipient: str, message: str) -> None:
        pass

class EmailService(NotificationSender):
    def send(self, recipient: str, message: str) -> None:
        print(f"Sending Email to {recipient}: {message}")

class UserNotifier:
    def __init__(self, sender: NotificationSender):  # Dependency Injection
        self.sender = sender

    def alert(self, user_email: str, msg: str):
        self.sender.send(user_email, msg)
```"""
                }
            ]
        },
        {
            "order": 3,
            "title": "Creational Design Patterns",
            "description": "Factory Method, Abstract Factory, Builder, Singleton, and Prototype patterns.",
            "chapters": [
                {
                    "order": 1,
                    "title": "Factory Method & Abstract Factory",
                    "description": "Decouple object creation logic from client consumption and construct families of related objects.",
                    "duration_minutes": 40,
                    "content": """# Factory Method & Abstract Factory

```python
from abc import ABC, abstractmethod

class Button(ABC):
    @abstractmethod
    def render(self) -> str:
        pass

class DarkButton(Button):
    def render(self) -> str:
        return "[Dark Theme Button]"

class LightButton(Button):
    def render(self) -> str:
        return "[Light Theme Button]"

class GUIFactory(ABC):
    @abstractmethod
    def create_button(self) -> Button:
        pass

class DarkThemeFactory(GUIFactory):
    def create_button(self) -> Button:
        return DarkButton()

class LightThemeFactory(GUIFactory):
    def create_button(self) -> Button:
        return LightButton()
```

## Key Takeaways
- Abstract Factory provides an interface for creating families of related or dependent objects without specifying their concrete classes."""
                },
                {
                    "order": 2,
                    "title": "Builder & Thread-Safe Singleton",
                    "description": "Construct complex multi-step objects with fluent APIs and implement thread-safe singletons.",
                    "duration_minutes": 40,
                    "content": """# Builder & Singleton Patterns

## 1. Fluent Builder Pattern
```python
class HTTPRequest:
    def __init__(self, url: str, method: str, headers: dict, body: str):
        self.url = url
        self.method = method
        self.headers = headers
        self.body = body

class HTTPRequestBuilder:
    def __init__(self, url: str):
        self.url = url
        self.method = "GET"
        self.headers = {}
        self.body = ""

    def set_method(self, method: str):
        self.method = method
        return self

    def add_header(self, key: str, value: str):
        self.headers[key] = value
        return self

    def set_body(self, body: str):
        self.body = body
        return self

    def build(self) -> HTTPRequest:
        return HTTPRequest(self.url, self.method, self.headers, self.body)

# Usage
req = HTTPRequestBuilder("https://api.techspire.com/v1/auth") \\
    .set_method("POST") \\
    .add_header("Authorization", "Bearer token123") \\
    .set_body('{"action": "login"}') \\
    .build()
```"""
                }
            ]
        },
        {
            "order": 4,
            "title": "Structural Design Patterns",
            "description": "Adapter, Decorator, Facade, Composite, Proxy, and Bridge patterns.",
            "chapters": [
                {
                    "order": 1,
                    "title": "Adapter & Facade Patterns",
                    "description": "Bridge incompatible API interfaces and provide simplified unified facades over complex subsystems.",
                    "duration_minutes": 40,
                    "content": """# Adapter & Facade Patterns

## 1. Adapter Pattern (Interface Translation)
```python
class LegacyXmlLogger:
    def log_xml(self, xml_payload: str):
        print(f"<log>{xml_payload}</log>")

class JsonLoggerTarget(ABC):
    @abstractmethod
    def log_json(self, data: dict):
        pass

class XmlToJsonAdapter(JsonLoggerTarget):
    def __init__(self, legacy_logger: LegacyXmlLogger):
        self.legacy_logger = legacy_logger

    def log_json(self, data: dict):
        xml = "".join(f"<{k}>{v}</{k}>" for k, v in data.items())
        self.legacy_logger.log_xml(xml)
```

## Key Takeaways
- Adapter enables classes with incompatible interfaces to collaborate seamlessly."""
                },
                {
                    "order": 2,
                    "title": "Decorator & Proxy Patterns",
                    "description": "Attach dynamic responsibilities to objects and control access via caching/lazy-loading proxies.",
                    "duration_minutes": 45,
                    "content": """# Decorator & Proxy Patterns

## Decorator Pattern (Wrapping Behaviors)
```python
class DataSource(ABC):
    @abstractmethod
    def write(self, data: str) -> None:
        pass

class FileDataSource(DataSource):
    def write(self, data: str) -> None:
        print(f"Writing raw data to file: {data}")

class EncryptionDecorator(DataSource):
    def __init__(self, wrappee: DataSource):
        self._wrappee = wrappee

    def write(self, data: str) -> None:
        encrypted = f"ENC({data})"
        print("Encrypting payload...")
        self._wrappee.write(encrypted)
```"""
                }
            ]
        },
        {
            "order": 5,
            "title": "Behavioral Patterns I: Event & State Handling",
            "description": "Observer (Pub/Sub), Strategy, Command, and State machine patterns.",
            "chapters": [
                {
                    "order": 1,
                    "title": "Observer Pattern & Event-Driven Architecture",
                    "description": "Implement decoupled publish-subscribe event systems with weak references.",
                    "duration_minutes": 45,
                    "content": """# Observer Pattern (Publish-Subscribe)

The Observer pattern defines a one-to-many dependency so that when one object changes state, all its dependents are notified automatically.

```python
class Observer(ABC):
    @abstractmethod
    def update(self, event_type: str, data: dict) -> None:
        pass

class EventManager:
    def __init__(self):
        self._listeners: dict[str, list[Observer]] = {}

    def subscribe(self, event_type: str, listener: Observer):
        self._listeners.setdefault(event_type, []).append(listener)

    def notify(self, event_type: str, data: dict):
        for listener in self._listeners.get(event_type, []):
            listener.update(event_type, data)
```"""
                },
                {
                    "order": 2,
                    "title": "Strategy & Command Patterns (Undo/Redo)",
                    "description": "Encapsulate executable actions with rollback support and hot-swappable algorithms.",
                    "duration_minutes": 45,
                    "content": """# Command Pattern with Undo Support

```python
class Command(ABC):
    @abstractmethod
    def execute(self) -> None:
        pass
    @abstractmethod
    def undo(self) -> None:
        pass

class InsertTextCommand(Command):
    def __init__(self, doc, text: str):
        self.doc = doc
        self.text = text

    def execute(self):
        self.doc.content += self.text

    def undo(self):
        self.doc.content = self.doc.content[:-len(self.text)]
```"""
                }
            ]
        },
        {
            "order": 6,
            "title": "Behavioral Patterns II: Workflow & Traversal",
            "description": "Chain of Responsibility, Template Method, Iterator, Mediator, and Visitor patterns.",
            "chapters": [
                {
                    "order": 1,
                    "title": "Chain of Responsibility & Middleware Pipelines",
                    "description": "Build HTTP request filtering pipelines and authentication validation chains.",
                    "duration_minutes": 40,
                    "content": """# Chain of Responsibility (Middleware Pipeline)

```python
class Handler(ABC):
    def __init__(self, next_handler: 'Handler | None' = None):
        self.next_handler = next_handler

    @abstractmethod
    def handle(self, request: dict) -> bool:
        if self.next_handler:
            return self.next_handler.handle(request)
        return True

class AuthHandler(Handler):
    def handle(self, request: dict) -> bool:
        if not request.get("authenticated"):
            print("Authentication failed!")
            return False
        return super().handle(request)

class RateLimitHandler(Handler):
    def handle(self, request: dict) -> bool:
        if request.get("rate_limited"):
            print("Rate limit exceeded!")
            return False
        return super().handle(request)
```"""
                }
            ]
        },
        {
            "order": 7,
            "title": "Domain-Driven Design (DDD) & Enterprise Patterns",
            "description": "Entities, Value Objects, Aggregates, Repositories, Domain Events, and Anemic vs Rich Models.",
            "chapters": [
                {
                    "order": 1,
                    "title": "Entities, Value Objects & Aggregate Roots",
                    "description": "Model rich domain invariants using immutable value objects and aggregate boundaries.",
                    "duration_minutes": 50,
                    "content": """# Domain-Driven Design (DDD) Modeling

## 1. Value Object (Identity defined solely by attributes, Immutable)
```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Money:
    amount: float
    currency: str

    def add(self, other: 'Money') -> 'Money':
        if self.currency != other.currency:
            raise ValueError("Currency mismatch")
        return Money(self.amount + other.amount, self.currency)
```

## 2. Aggregate Root (Transactional boundary)
An Aggregate Root guarantees business consistency for all internal entities inside its boundary."""
                }
            ]
        },
        {
            "order": 8,
            "title": "Concurrency & Multithreaded Design Patterns",
            "description": "Thread Pool, Producer-Consumer, Double-Checked Locking, and Immutability.",
            "chapters": [
                {
                    "order": 1,
                    "title": "Producer-Consumer & Thread Pools",
                    "description": "Coordinate asynchronous worker threads safely using thread-safe blocking queues.",
                    "duration_minutes": 45,
                    "content": """# Producer-Consumer Pattern

```python
import threading
import queue
import time

work_queue = queue.Queue(maxsize=10)

def producer():
    for i in range(20):
        work_queue.put(f"Job-{i}")
        print(f"Produced Job-{i}")
        time.sleep(0.05)

def worker(worker_id: int):
    while True:
        job = work_queue.get()
        if job is None:
            break
        print(f"Worker {worker_id} processing {job}")
        work_queue.task_done()
```"""
                }
            ]
        },
        {
            "order": 9,
            "title": "Refactoring & Anti-Pattern Detection",
            "description": "Code smells, refactoring techniques (Extract Method, Replace Conditionals), and architectural anti-patterns.",
            "chapters": [
                {
                    "order": 1,
                    "title": "Refactoring Code Smells to Polymorphism",
                    "description": "Identify switch-case smell, primitive obsession, and God objects.",
                    "duration_minutes": 45,
                    "content": """# Refactoring Code Smells

## Common Code Smells & Solutions
1. **Primitive Obsession** $\\to$ Replace with Value Objects (e.g., `EmailAddress`, `PhoneNumber`).
2. **Switch Statements / Large If-Else Chains** $\\to$ Replace Conditional with Polymorphism / Strategy Pattern.
3. **God Class** $\\to$ Extract Classes and apply Single Responsibility Principle.
4. **Feature Envy** $\\to$ Move Method to the class possessing the required data."""
                }
            ]
        }
    ],
    "assessment": {
        "title": "Object-Oriented Design & Design Patterns Certification Exam",
        "description": "Demonstrate mastery of SOLID principles, GoF creational, structural, and behavioral patterns, and clean architecture.",
        "passing_score": 70,
        "time_limit_minutes": 25,
        "questions": [
            {
                "question_text": "Which SOLID principle states that high-level modules should not depend on low-level modules, and both should depend on abstractions?",
                "question_type": "single",
                "explanation": "The Dependency Inversion Principle (DIP) mandates depending on abstract interfaces rather than concrete class implementations.",
                "points": 20,
                "options": [
                    {"text": "Dependency Inversion Principle (DIP)", "is_correct": True},
                    {"text": "Single Responsibility Principle (SRP)", "is_correct": False},
                    {"text": "Liskov Substitution Principle (LSP)", "is_correct": False},
                    {"text": "Open/Closed Principle (OCP)", "is_correct": False}
                ]
            },
            {
                "question_text": "Which Gang of Four (GoF) structural design pattern allows incompatible interfaces to collaborate by converting the interface of a class into another interface expected by clients?",
                "question_type": "single",
                "explanation": "The Adapter pattern converts the interface of a class into another interface clients expect, enabling incompatible classes to work together.",
                "points": 20,
                "options": [
                    {"text": "Adapter Pattern", "is_correct": True},
                    {"text": "Bridge Pattern", "is_correct": False},
                    {"text": "Facade Pattern", "is_correct": False},
                    {"text": "Proxy Pattern", "is_correct": False}
                ]
            },
            {
                "question_text": "How does an immutable Value Object differ from an Entity in Domain-Driven Design (DDD)?",
                "question_type": "single",
                "explanation": "An Entity has a distinct conceptual identity that runs through time, while a Value Object is defined strictly by its attribute values and has no persistent identifier.",
                "points": 20,
                "options": [
                    {"text": "Value Objects are identified solely by their attributes and are immutable", "is_correct": True},
                    {"text": "Entities have no unique ID", "is_correct": False},
                    {"text": "Value Objects must always contain database primary keys", "is_correct": False},
                    {"text": "There is no difference between Entities and Value Objects", "is_correct": False}
                ]
            },
            {
                "question_text": "Which design pattern is best suited for implementing multi-step Undo and Redo operations in an application?",
                "question_type": "single",
                "explanation": "The Command pattern encapsulates a request as an object, allowing parameterization of clients with queues, logs, and undoable operations.",
                "points": 20,
                "options": [
                    {"text": "Command Pattern", "is_correct": True},
                    {"text": "Singleton Pattern", "is_correct": False},
                    {"text": "Template Method Pattern", "is_correct": False},
                    {"text": "Observer Pattern", "is_correct": False}
                ]
            },
            {
                "question_text": "What is the primary violation when a child class overrides a base class method with preconditions that are stricter than the parent?",
                "question_type": "single",
                "explanation": "Liskov Substitution Principle (LSP) requires that preconditions cannot be strengthened in a subtype.",
                "points": 20,
                "options": [
                    {"text": "Liskov Substitution Principle (LSP) violation", "is_correct": True},
                    {"text": "Single Responsibility Principle violation", "is_correct": False},
                    {"text": "Interface Segregation Principle violation", "is_correct": False},
                    {"text": "Encapsulation violation", "is_correct": False}
                ]
            }
        ]
    }
}
