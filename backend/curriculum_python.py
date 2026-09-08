PYTHON_COURSE = {
    'title': 'Python Programming Mastery',
    'slug': 'python-programming',
    'tagline': 'From syntax foundations to advanced generators, decorators, memory internals, and production patterns.',
    'description': 'A comprehensive, engineering-grade curriculum covering core Python syntax, functional paradigms, object-oriented architecture, exception hierarchies, memory management, and asynchronous programming.',
    'category': 'Programming Languages',
    'category_icon': 'Code',
    'difficulty': 'beginner',
    'estimated_hours': 45,
    'badge_icon': 'Terminal',
    'color_accent': '#38BDF8',
    'order': 1,
    'prerequisites': ['No prior programming experience required', 'Basic computer literacy'],
    'learning_outcomes': [
        'Write idiomatic Python 3 using PEP 8 standards',
        'Master data structures: lists, dicts, sets, tuples, and comprehensions',
        'Implement Object-Oriented Programming with inheritance, dunder methods, and dataclasses',
        'Build custom decorators, generators, context managers, and iterators',
        'Write robust unit tests and handle production edge-case exceptions'
    ],
    'modules': [
        {
            'title': 'Module 1: Python Fundamentals & Runtime Architecture',
            'description': 'CPython architecture, bytecode execution, memory model, and REPL mechanics.',
            'chapters': [
                {
                    'title': 'CPython Virtual Machine & Bytecode Compilation',
                    'duration_minutes': 20,
                    'is_free_preview': True,
                    'code_language': 'python',
                    'content_markdown': """# CPython Virtual Machine & Bytecode Compilation

Python is a high-level interpreted language whose reference implementation is CPython. When you execute a Python script, the source code (`.py`) is first compiled into intermediate **bytecode** (`.pyc` cached in `__pycache__`), which is then executed by the CPython virtual machine evaluation loop (`ceval.c`).

## 1. The Compilation and Execution Pipeline
1. **Lexical Analysis & Parsing**: Source code is converted into tokens and parsed into an Abstract Syntax Tree (AST).
2. **Bytecode Generation**: The AST is compiled into Python bytecode instructions.
3. **VM Evaluation**: The CPython interpreter executes bytecode instructions on a stack-based virtual machine.

```python
import dis

def compute_tax(amount: float, rate: float = 0.18) -> float:
    total = amount * (1 + rate)
    return round(total, 2)

# Inspect raw virtual machine bytecode
dis.dis(compute_tax)
```
""",
                    'code_snippet': """import dis

def add_numbers(a, b):
    return a + b

print("Disassembled CPython Bytecode:")
dis.dis(add_numbers)""",
                    'key_takeaways': [
                        'CPython compiles source code to stack-based bytecode before execution.',
                        'The dis module allows inspecting low-level bytecode opcodes.',
                        'Bytecode is cached in __pycache__ to accelerate subsequent imports.'
                    ],
                    'practice_questions': [
                        {
                            'question': 'What is the role of the __pycache__ directory in Python projects?',
                            'answer': 'It stores compiled bytecode files (.pyc) corresponding to imported modules to skip compilation on subsequent runs.'
                        }
                    ]
                },
                {
                    'title': 'Memory Model, References & Garbage Collection',
                    'duration_minutes': 25,
                    'is_free_preview': True,
                    'code_language': 'python',
                    'content_markdown': """# Memory Model, References & Garbage Collection

In Python, all values are objects residing in the heap. Variables are merely **names bound to object references**.

## 1. Reference Counting & Cyclic GC
CPython uses two complementary memory management strategies:
- **Reference Counting**: Every object tracks `ob_refcnt`. When reference count drops to 0, memory is freed immediately.
- **Generational Garbage Collector**: Detects and breaks cyclic references (e.g. object A references B, and B references A).

```python
import sys
import gc

a = [1, 2, 3]
print(f"Ref count for a: {sys.getrefcount(a) - 1}") # Compensate for getrefcount argument reference

b = a # Increases ref count
print(f"Ref count after alias: {sys.getrefcount(a) - 1}")
```
""",
                    'code_snippet': """import sys

x = "Techspire"
y = x
print(f"Reference identity check: {x is y}") # True
print(f"Memory Address of x: {hex(id(x))}")""",
                    'key_takeaways': [
                        'CPython deallocates objects immediately when their reference count reaches zero.',
                        'Generational GC runs periodically to collect circular references.',
                        'The is operator checks memory identity, whereas == checks value equality.'
                    ],
                    'practice_questions': [
                        {
                            'question': 'What is the difference between is and == in Python?',
                            'answer': 'The is operator checks object identity (whether two variables point to the same memory address via id()), while == checks value equality.'
                        }
                    ]
                }
            ]
        },
        {
            'title': 'Module 2: Variables, Data Types & Operators',
            'description': 'Primitives, immutability, type casting, bitwise operations, and arithmetic precedence.',
            'chapters': [
                {
                    'title': 'Numeric Types, Precision & Bitwise Manipulation',
                    'duration_minutes': 20,
                    'is_free_preview': True,
                    'code_language': 'python',
                    'content_markdown': """# Numeric Types, Precision & Bitwise Manipulation

Python provides arbitrary-precision integers (`int`), double-precision floating-point numbers (`float`), complex numbers (`complex`), and exact fixed-point decimals (`decimal.Decimal`).

## 1. Arbitrary-Precision Integers vs Floats
Python integers will never overflow; they dynamically scale memory. Floating point numbers follow IEEE 754 standard (53 bits of precision).

```python
from decimal import Decimal

# IEEE 754 floating point representation limitation
print(0.1 + 0.2 == 0.3) # False: 0.30000000000000004

# Precise financial arithmetic with Decimal
d1 = Decimal('0.1')
d2 = Decimal('0.2')
print(d1 + d2 == Decimal('0.3')) # True
```
""",
                    'code_snippet': """# Bitwise flags demonstration
READ_FLAG = 1 << 0   # 0001
WRITE_FLAG = 1 << 1  # 0010
EXEC_FLAG = 1 << 2   # 0100

user_perms = READ_FLAG | WRITE_FLAG
print(f"Has execute permission? {bool(user_perms & EXEC_FLAG)}") # False
print(f"Has read permission? {bool(user_perms & READ_FLAG)}")    # True""",
                    'key_takeaways': [
                        'Use decimal.Decimal for financial applications requiring exact decimal precision.',
                        'Python ints dynamically expand memory and do not suffer from integer overflow.',
                        'Bitwise operators (&, |, ^, <<, >>) operate directly on binary representations.'
                    ],
                    'practice_questions': [
                        {
                            'question': 'Why is float arithmetic imprecise for currency calculations?',
                            'answer': 'Floating point numbers represent values in binary fractions (base 2), which cannot represent numbers like 0.1 or 0.2 exactly.'
                        }
                    ]
                },
                {
                    'title': 'String Interning, Unicode & Formatting',
                    'duration_minutes': 25,
                    'is_free_preview': False,
                    'code_language': 'python',
                    'content_markdown': """# String Interning, Unicode & Formatting

Strings in Python 3 are immutable sequences of Unicode code points (`str`) encoded dynamically using PEP 393 (Flexible String Representation: Latin-1, UCS-2, or UCS-4).

## 1. F-Strings (Formatted String Literals)
```python
name = "Techspire"
version = 2.0
timestamp = 1718000000

# Advanced F-string formatting with expressions and specifiers
log_line = f"[{name:^12}] Ver: {version:.2f} | Hex ID: {timestamp:#010x}"
print(log_line)
```
""",
                    'code_snippet': """title = "Systems Architecture"
print(f"Upper: {title.upper()}")
print(f"Slug: {title.lower().replace(' ', '-')}")
print(f"Slicing reverse: {title[::-1]}")""",
                    'key_takeaways': [
                        'Strings are immutable; concatenating in a loop creates multiple copies. Use .join() instead.',
                        'F-strings provide inline expression evaluation and format specification.',
                        'CPython interns small identifier-like strings for rapid O(1) comparison.'
                    ],
                    'practice_questions': [
                        {
                            'question': 'Why is "".join(list_of_strings) preferred over string concatenation in a loop?',
                            'answer': 'join pre-calculates the required buffer size and allocates memory once in O(N), whereas += in a loop creates new intermediate strings in O(N^2).'
                        }
                    ]
                }
            ]
        },
        {
            'title': 'Module 3: Control Flow & Structural Pattern Matching',
            'description': 'Conditionals, loops, break/continue/else clauses, and structural pattern matching.',
            'chapters': [
                {
                    'title': 'Structural Pattern Matching with match-case',
                    'duration_minutes': 25,
                    'is_free_preview': False,
                    'code_language': 'python',
                    'content_markdown': """# Structural Pattern Matching with match-case

Introduced in Python 3.10 (PEP 634), pattern matching enables elegant destructuring of objects, mappings, and sequences.

```python
def handle_http_event(event: dict):
    match event:
        case {"status": 200, "data": str(payload)}:
            return f"Success: {payload}"
        case {"status": 400..499, "error": str(err)}:
            return f"Client error: {err}"
        case {"status": 500..599}:
            return "Critical server error"
        case _:
            return "Unknown protocol payload"
```
""",
                    'code_snippet': """payload = {"status": 200, "data": "Cluster synced"}
match payload:
    case {"status": 200, "data": msg}:
        print(f"Received OK: {msg}")
    case _:
        print("Unhandled state")""",
                    'key_takeaways': [
                        'match-case combines type checking, value matching, and variable extraction.',
                        'Wildcard case _ acts as the default fallback branch.',
                        'Guards (if condition) can be added to individual case clauses.'
                    ],
                    'practice_questions': [
                        {
                            'question': 'Can match-case extract values into variables during matching?',
                            'answer': 'Yes, variable names in patterns capture matching values and bind them in the local scope.'
                        }
                    ]
                }
            ]
        },
        {
            'title': 'Module 4: Built-in Collections & Data Structures',
            'description': 'Lists, tuples, sets, dictionaries, and memory comprehensions.',
            'chapters': [
                {
                    'title': 'Dictionary Hash Table Internals & Collision Resolution',
                    'duration_minutes': 30,
                    'is_free_preview': False,
                    'code_language': 'python',
                    'content_markdown': """# Dictionary Hash Table Internals & Collision Resolution

Python dictionaries are implemented as compact, order-preserving hash tables based on Raymond Hettinger\'s design.

## 1. Hash Table Mechanism
- Keys must implement deterministic `__hash__()` and `__eq__()` methods.
- Key hash is computed: `hash_val = hash(key)`.
- Perturbation lookup resolves hash collisions in O(1) average time.

```python
# Dict Comprehensions and Merging
user_scores = {"alice": 95, "bob": 88, "charlie": 92}
passed_students = {k: v for k, v in user_scores.items() if v >= 90}

# Modern dict merge operator (Python 3.9+)
config_default = {"theme": "dark", "notifications": True}
config_custom = {"theme": "obsidian_cyan"}
merged = config_default | config_custom
print(merged)
```
""",
                    'code_snippet': """dict_a = {"port": 8000, "host": "127.0.0.1"}
dict_b = {"port": 443, "ssl": True}
# Merge using | operator
final_config = dict_a | dict_b
print("Merged Config:", final_config)""",
                    'key_takeaways': [
                        'Dictionaries preserve insertion order since Python 3.7.',
                        'Dictionary keys must be immutable/hashable types.',
                        'The | and |= operators merge dictionaries cleanly.'
                    ],
                    'practice_questions': [
                        {
                            'question': 'What makes an object hashable in Python?',
                            'answer': 'An object is hashable if it has a hash value that never changes during its lifetime and can be compared to other objects via __eq__.'
                        }
                    ]
                }
            ]
        },
        {
            'title': 'Module 5: Functions, Closures, Scope & Lambdas',
            'description': 'LEGB scope resolution, variadic arguments, closures, and first-class callables.',
            'chapters': [
                {
                    'title': 'Closures & The LEGB Scope Resolution Hierarchy',
                    'duration_minutes': 30,
                    'is_free_preview': False,
                    'code_language': 'python',
                    'content_markdown': """# Closures & The LEGB Scope Resolution Hierarchy

Python resolves variable names following the **LEGB rule**:
1. **L**ocal: Inside the current function.
2. **E**nclosing: In any outer enclosing functions (closures).
3. **G**lobal: Module-level variables.
4. **B**uilt-in: Python built-in namespace (`len`, `range`, `print`).

## 1. Creating True Closures
A closure occurs when an inner function retains access to variables in its enclosing scope even after the outer function has returned.

```python
def make_rate_limiter(max_requests: int):
    count = 0 # Enclosing state variable
    def limiter():
        nonlocal count
        if count >= max_requests:
            return False
        count += 1
        return True
    return limiter
```
""",
                    'code_snippet': """limiter = make_rate_limiter(2)
print(limiter()) # True
print(limiter()) # True
print(limiter()) # False (Limit reached)""",
                    'key_takeaways': [
                        'nonlocal binds a variable to the nearest enclosing scope rather than global scope.',
                        'Closures encapsulate private state without requiring full class definitions.',
                        'Functions are first-class citizens and can be passed as arguments or returned.'
                    ],
                    'practice_questions': [
                        {
                            'question': 'What is the purpose of the nonlocal keyword?',
                            'answer': 'It allows modifying a variable in an enclosing outer function scope without declaring it global.'
                        }
                    ]
                }
            ]
        },
        {
            'title': 'Module 6: Modules, Packages & Exception Hierarchies',
            'description': 'Custom exception hierarchies, context managers, and package imports.',
            'chapters': [
                {
                    'title': 'Robust Exception Hierarchies & Exception Chaining',
                    'duration_minutes': 25,
                    'is_free_preview': False,
                    'code_language': 'python',
                    'content_markdown': """# Robust Exception Hierarchies & Exception Chaining

Production applications should define explicit domain exception hierarchies inheriting from `Exception`.

```python
class TechspireBaseError(Exception):
    '''Base exception for all domain errors.'''

class CourseNotFoundError(TechspireBaseError):
    def __init__(self, course_slug: str):
        super().__init__(f"Course '{course_slug}' does not exist or is unpublished.")
        self.course_slug = course_slug

# Explicit Exception Chaining
try:
    int("invalid_number")
except ValueError as err:
    raise CourseNotFoundError("calc-101") from err
```
""",
                    'code_snippet': """try:
    raise ValueError("Original low-level parsing fault")
except ValueError as exc:
    print(f"Caught and handled: {exc}")""",
                    'key_takeaways': [
                        'Always inherit custom exceptions from Exception, never BaseException.',
                        'Use raise ... from exc to preserve the original exception traceback (cause).',
                        'Never use bare except: clauses as they catch SystemExit and KeyboardInterrupt.'
                    ],
                    'practice_questions': [
                        {
                            'question': 'Why should custom exceptions inherit from Exception rather than BaseException?',
                            'answer': 'BaseException is the parent of critical system signals like KeyboardInterrupt and SystemExit. Inheriting from Exception ensures user code does not intercept system shutdown signals.'
                        }
                    ]
                }
            ]
        },
        {
            'title': 'Module 7: File I/O, Serialization & JSON Processing',
            'description': 'Context managers for file descriptors, binary streams, and JSON serialization.',
            'chapters': [
                {
                    'title': 'Deterministic File Handling & Serialization',
                    'duration_minutes': 25,
                    'is_free_preview': False,
                    'code_language': 'python',
                    'content_markdown': """# Deterministic File Handling & Serialization

The `with` statement ensures file handles are closed deterministically even if an unhandled exception occurs.

```python
import json
from pathlib import Path

def save_telemetry(data: dict, filepath: Path):
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with filepath.open('w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
```
""",
                    'code_snippet': """import json

raw_json = '{"course": "Python", "rating": 5.0, "active": true}'
parsed = json.loads(raw_json)
print("Parsed Title:", parsed["course"])""",
                    'key_takeaways': [
                        'Always specify explicit encoding="utf-8" when opening text files.',
                        'pathlib.Path provides an object-oriented API for file system paths.',
                        'json.dumps serializes objects to JSON strings; json.dump writes directly to file objects.'
                    ],
                    'practice_questions': [
                        {
                            'question': 'What is the advantage of pathlib.Path over os.path?',
                            'answer': 'pathlib provides an object-oriented, cross-platform interface that abstracts OS-specific slash differences and file operations into methods.'
                        }
                    ]
                }
            ]
        },
        {
            'title': 'Module 8: Object-Oriented Architecture & Magic Dunder Methods',
            'description': 'Classes, inheritance, polymorphism, slots, dataclasses, and magic methods.',
            'chapters': [
                {
                    'title': 'Custom Magic Dunder Methods & Dataclasses',
                    'duration_minutes': 35,
                    'is_free_preview': False,
                    'code_language': 'python',
                    'content_markdown': """# Custom Magic Dunder Methods & Dataclasses

Python enables operator overloading and rich object behavior through special double-underscore ("dunder") methods.

```python
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class StudentRecord:
    student_id: int
    name: string
    gpa: float

    def is_honor_roll(self) -> bool:
        return self.gpa >= 3.8
```
""",
                    'code_snippet': """from dataclasses import dataclass

@dataclass
class Point:
    x: float
    y: float

p1 = Point(10.0, 20.0)
print("Dataclass Point:", p1)""",
                    'key_takeaways': [
                        '@dataclass generates __init__, __repr__, and __eq__ boilerplate automatically.',
                        'slots=True in dataclasses restricts memory to a fixed tuple, reducing RAM usage.',
                        'frozen=True makes instances immutable and automatically hashable.'
                    ],
                    'practice_questions': [
                        {
                            'question': 'What are the benefits of setting frozen=True on a dataclass?',
                            'answer': 'It prevents attribute reassignment after instantiation (immutability) and automatically implements __hash__(), allowing instances to be used as dict keys or in sets.'
                        }
                    ]
                }
            ]
        },
        {
            'title': 'Module 9: Advanced Python (Decorators, Generators & Contexts)',
            'description': 'Higher-order decorators, generator pipelines, and custom context managers.',
            'chapters': [
                {
                    'title': 'Decorators, Generators & Context Managers in Production',
                    'duration_minutes': 35,
                    'is_free_preview': False,
                    'code_language': 'python',
                    'content_markdown': """# Decorators, Generators & Context Managers in Production

Mastering higher-order wrapper functions, memory-efficient generator streams, and deterministic cleanup protocols.

```python
import functools
import time

def timing_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"[{func.__name__}] Execution took {elapsed*1000:.2f}ms")
        return result
    return wrapper
```
""",
                    'code_snippet': """import functools

def announce(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}...")
        return func(*args, **kwargs)
    return wrapper

@announce
def ping():
    return "PONG"

print(ping())""",
                    'key_takeaways': [
                        'functools.wraps preserves function identity and docstrings.',
                        'Generators yield values lazily, executing with O(1) space complexity.',
                        'Context managers encapsulate try/finally patterns cleanly.'
                    ],
                    'practice_questions': [
                        {
                            'question': 'How does yield differ from return in a function?',
                            'answer': 'return terminates execution and returns a value, destroying the stack frame. yield pauses function state, emits a value, and allows execution to resume on next().'
                        }
                    ]
                }
            ]
        },
        {
            'title': 'Module 10: Testing, Debugging, Virtualenvs & Tooling',
            'description': 'Pytest testing framework, debugging with pdb, typing, and venv tooling.',
            'chapters': [
                {
                    'title': 'Production Pytest Architecture & Type Validation',
                    'duration_minutes': 30,
                    'is_free_preview': False,
                    'code_language': 'python',
                    'content_markdown': """# Production Pytest Architecture & Type Validation

Writing isolated, parameter-driven unit and integration tests with Pytest.

```python
import pytest

def divide(a: float, b: float) -> float:
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero.")
    return a / b

def test_divide_valid():
    assert divide(10, 2) == 5.0

def test_divide_zero_raises():
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)
```
""",
                    'code_snippet': """def test_math():
    assert 2 + 2 == 4
    print("Test passed successfully!")

test_math()""",
                    'key_takeaways': [
                        'Pytest uses standard assert expressions for clean test validation.',
                        'pytest.raises verifies expected exceptions.',
                        'Always run tests in isolated virtual environments.'
                    ],
                    'practice_questions': [
                        {
                            'question': 'Why is pytest preferred over unittest in modern Python development?',
                            'answer': 'Pytest requires minimal boilerplate, allows standard assert statements with detailed failure introspection, and provides a powerful fixture dependency injection system.'
                        }
                    ]
                }
            ]
        },
        {
            'title': 'Module 11: Real-World Architecture & Projects',
            'description': 'Designing scalable CLI utilities, REST APIs, and concurrency pipelines.',
            'chapters': [
                {
                    'title': 'Building High-Throughput Async Pipelines',
                    'duration_minutes': 35,
                    'is_free_preview': False,
                    'code_language': 'python',
                    'content_markdown': """# Building High-Throughput Async Pipelines

Leveraging `asyncio` for non-blocking I/O operations and asynchronous concurrency.

```python
import asyncio

async def fetch_telemetry(node_id: int):
    await asyncio.sleep(0.05) # Non-blocking I/O simulation
    return {"node": node_id, "status": "HEALTHY"}

async def main():
    tasks = [fetch_telemetry(i) for i in range(10)]
    results = await asyncio.gather(*tasks)
    print(f"Collected {len(results)} node telemetry reports.")
```
""",
                    'code_snippet': """import asyncio

async def sample_coroutine():
    return "Async worker finished"

result = asyncio.run(sample_coroutine())
print(result)""",
                    'key_takeaways': [
                        'asyncio runs on a single thread event loop and is optimal for I/O bound tasks.',
                        'asyncio.gather executes multiple coroutines concurrently.',
                        'Never call blocking synchronous sleep or socket calls inside an async event loop.'
                    ],
                    'practice_questions': [
                        {
                            'question': 'What is the primary difference between multithreading and asyncio in Python?',
                            'answer': 'Multithreading relies on OS-preempted threads constrained by the GIL, whereas asyncio uses cooperative multitasking on a single thread with explicit await points for non-blocking I/O.'
                        }
                    ]
                }
            ]
        }
    ],
    'assessment': {
        'title': 'Python Engineering Certification Exam',
        'description': 'Comprehensive test evaluating syntax, memory models, object-oriented architecture, closures, decorators, and data structure mechanics.',
        'passing_score': 70,
        'time_limit_minutes': 25,
        'questions': [
            {
                'question_text': 'Which of the following data types in Python is mutable?',
                'question_type': 'single',
                'explanation': 'In Python, lists, dictionaries, and sets are mutable. Integers, strings, and tuples are immutable.',
                'points': 20,
                'options': [
                    {'text': 'tuple', 'is_correct': False},
                    {'text': 'list', 'is_correct': True},
                    {'text': 'str', 'is_correct': False},
                    {'text': 'frozenset', 'is_correct': False}
                ]
            },
            {
                'question_text': 'What will be the output of the following Python code snippet?',
                'question_type': 'code',
                'code_context': """def append_to(element, target=[]):
    target.append(element)
    return target

print(append_to(1))
print(append_to(2))""",
                'explanation': 'Default argument expressions in Python are evaluated once when the function definition is executed, NOT every time the function is called. Thus, the same mutable list object is reused.',
                'points': 25,
                'options': [
                    {'text': '[1] followed by [2]', 'is_correct': False},
                    {'text': '[1] followed by [1, 2]', 'is_correct': True},
                    {'text': 'TypeError: default argument error', 'is_correct': False},
                    {'text': '[1, 2] followed by [1, 2]', 'is_correct': False}
                ]
            },
            {
                'question_text': 'Why is @functools.wraps recommended when defining custom decorators?',
                'question_type': 'single',
                'explanation': '@functools.wraps copies original function metadata (such as __name__, __doc__, and type annotations) to the inner wrapper function.',
                'points': 25,
                'options': [
                    {'text': 'It compiles the Python code into C extension for speed', 'is_correct': False},
                    {'text': 'It preserves the original function metadata such as __name__ and __doc__', 'is_correct': True},
                    {'text': 'It prevents memory leaks by freeing the wrapper immediately', 'is_correct': False},
                    {'text': 'It allows the function to run asynchronously by default', 'is_correct': False}
                ]
            },
            {
                'question_text': 'What algorithm does Python 3 use to compute the Method Resolution Order (MRO) for multiple inheritance?',
                'question_type': 'single',
                'explanation': 'Python 3 utilizes C3 Linearization to produce a deterministic and monotonic method resolution order.',
                'points': 30,
                'options': [
                    {'text': 'Depth-First Search (DFS) with backtracking', 'is_correct': False},
                    {'text': 'C3 Linearization Algorithm', 'is_correct': True},
                    {'text': 'Dijkstra Shortest Path Search', 'is_correct': False},
                    {'text': 'Breadth-First Search (BFS) only', 'is_correct': False}
                ]
            }
        ]
    }
}
