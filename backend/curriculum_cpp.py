CPP_COURSE = {
    'title': 'Modern C++ Architecture',
    'slug': 'cpp-programming',
    'tagline': 'RAII, smart pointers, Standard Template Library (STL), templates, and move semantics in C++17/20.',
    'description': 'Master modern C++ paradigms. Eliminate raw pointers using unique_ptr and shared_ptr, leverage STL containers and algorithms, understand compile-time templates, move semantics (rvalue references), and concurrency.',
    'category': 'Systems Engineering',
    'category_icon': 'Cpu',
    'difficulty': 'intermediate',
    'estimated_hours': 45,
    'badge_icon': 'Boxes',
    'color_accent': '#6366F1',
    'order': 3,
    'prerequisites': ['Basic understanding of C syntax or object-oriented concepts'],
    'learning_outcomes': [
        'Apply Resource Acquisition Is Initialization (RAII) principles',
        'Master smart pointers: std::unique_ptr, std::shared_ptr, and std::weak_ptr',
        'Utilize the STL: vector, map, unordered_map, set, stack, and algorithms',
        'Leverage rvalue references, move constructors, and perfect forwarding'
    ],
    'modules': [
        {
            'title': 'Module 1: Modern C++ Foundations & Compilation',
            'description': 'C++ standards (C++11/14/17/20), namespaces, auto type deduction, and strongly-typed enums.',
            'chapters': [
                {
                    'title': 'Modern C++ Standards Evolution & Type Deduction',
                    'duration_minutes': 25,
                    'is_free_preview': True,
                    'code_language': 'cpp',
                    'content_markdown': """# Modern C++ Standards Evolution & Type Deduction

Modern C++ introduces automatic type deduction via `auto` and `decltype`, constexpr compile-time execution, and scoped enums (`enum class`).

```cpp
#include <iostream>
#include <vector>

enum class EngineState : uint8_t {
    IDLE = 0,
    INITIALIZING,
    RUNNING,
    ERROR
};

int main() {
    auto state = EngineState::RUNNING;
    constexpr int bufferSize = 1024 * 4; // Computed strictly at compile-time
    return 0;
}
```
""",
                    'code_snippet': """#include <iostream>

int main() {
    auto message = "Techspire Modern C++ Engine";
    std::cout << message << "\\n";
    return 0;
}""",
                    'key_takeaways': [
                        'enum class prevents implicit conversion to integers and name collisions.',
                        'auto deduces types at compile-time with zero runtime performance cost.',
                        'constexpr guarantees expressions are evaluated during compilation.'
                    ],
                    'practice_questions': [
                        {
                            'question': 'What is the benefit of enum class over traditional C-style enum?',
                            'answer': 'enum class is strongly typed and strongly scoped, preventing name pollution and implicit unsafe integer conversions.'
                        }
                    ]
                }
            ]
        },
        {
            'title': 'Module 2: References, Pointers & Const Correctness',
            'description': 'Lvalue references, pointer differences, and const-correct member functions.',
            'chapters': [
                {
                    'title': 'Lvalue References & Const Correctness',
                    'duration_minutes': 25,
                    'is_free_preview': True,
                    'code_language': 'cpp',
                    'content_markdown': """# Lvalue References & Const Correctness

In C++, a reference is an alias to an existing object and cannot be null or rebound.

```cpp
#include <iostream>

void printPayload(const std::string& data) { // Avoids expensive copy by passing const reference
    std::cout << "Data size: " << data.size() << "\\n";
}
```
""",
                    'code_snippet': """#include <iostream>

void increment(int &val) {
    val++;
}

int main() {
    int num = 41;
    increment(num);
    std::cout << "Incremented: " << num << "\\n"; // 42
    return 0;
}""",
                    'key_takeaways': [
                        'Pass large objects by const ref (const T&) to eliminate copy overhead.',
                        'References cannot be NULL and must be initialized upon declaration.',
                        'const member functions guarantee they will not modify object state.'
                    ],
                    'practice_questions': [
                        {
                            'question': 'How does a C++ reference differ from a pointer?',
                            'answer': 'A reference cannot be null, cannot be uninitialized, cannot be reseated to another object after initialization, and does not require explicit dereference syntax (*).'
                        }
                    ]
                }
            ]
        },
        {
            'title': 'Module 3: Object-Oriented C++ & Lifecycle Management',
            'description': 'Classes, constructors, delegating constructors, explicit, and the Rule of Zero/Three/Five.',
            'chapters': [
                {
                    'title': 'Constructors, Explicit Keyword & Rule of Five',
                    'duration_minutes': 30,
                    'is_free_preview': False,
                    'code_language': 'cpp',
                    'content_markdown': """# Constructors, Explicit Keyword & Rule of Five

Managing resources in classes with user-defined copy/move constructors and destructors.

```cpp
#include <iostream>
#include <utility>

class Buffer {
public:
    explicit Buffer(size_t size) : size_(size), data_(new int[size]) {}
    
    // Destructor
    ~Buffer() { delete[] data_; }

    // Move Constructor
    Buffer(Buffer&& other) noexcept : size_(other.size_), data_(other.data_) {
        other.size_ = 0;
        other.data_ = nullptr;
    }
private:
    size_t size_;
    int* data_;
};
```
""",
                    'code_snippet': """#include <iostream>

class Engine {
public:
    explicit Engine(int horsepower) : hp_(horsepower) {}
    int getHp() const { return hp_; }
private:
    int hp_;
};

int main() {
    Engine e(500);
    std::cout << "Horsepower: " << e.getHp() << "\\n";
    return 0;
}""",
                    'key_takeaways': [
                        'explicit prevents unintended implicit type conversions in single-argument constructors.',
                        'The Rule of Five states: if you implement destructor, implement copy ctor, copy assign, move ctor, and move assign.',
                        'Always mark move constructors noexcept to enable STL optimizations.'
                    ],
                    'practice_questions': [
                        {
                            'question': 'Why should single-argument constructors be marked explicit?',
                            'answer': 'To prevent the compiler from performing unintended implicit type conversions that can lead to subtle logic bugs.'
                        }
                    ]
                }
            ]
        },
        {
            'title': 'Module 4: Operator Overloading & User-Defined Conversions',
            'description': 'Overloading stream operators (<<, >>), arithmetic, subscript, and spaceship operator (<=>).',
            'chapters': [
                {
                    'title': 'Operator Overloading & Three-Way Comparison (<=>)',
                    'duration_minutes': 25,
                    'is_free_preview': False,
                    'code_language': 'cpp',
                    'content_markdown': """# Operator Overloading & Three-Way Comparison (<=>)

C++20 introduces the spaceship operator (`<=>`) for automatic generation of all comparison operators (`==`, `!=`, `<`, `<=`, `>`, `>=`).

```cpp
#include <iostream>
#include <compare>

struct Vector2D {
    int x;
    int y;

    auto operator<=>(const Vector2D&) const = default;
};
```
""",
                    'code_snippet': """#include <iostream>

struct Complex {
    double real, imag;
    Complex operator+(const Complex& other) const {
        return {real + other.real, imag + other.imag};
    }
};

int main() {
    Complex a{1.0, 2.0}, b{3.0, 4.0};
    Complex c = a + b;
    std::cout << "Sum: " << c.real << " + " << c.imag << "i\\n";
    return 0;
}""",
                    'key_takeaways': [
                        'Stream insertion (<<) should be overloaded as a non-member friend function.',
                        'C++20 default spaceship operator creates all 6 relational operators automatically.',
                        'Overload operators only when their semantics are intuitive and match standard arithmetic expectations.'
                    ],
                    'practice_questions': [
                        {
                            'question': 'Why should operator<< be implemented as a non-member function?',
                            'answer': 'Because the left-hand operand is std::ostream (not your class), so it cannot be a member function of your class.'
                        }
                    ]
                }
            ]
        },
        {
            'title': 'Module 5: Templates, Concepts & Metaprogramming',
            'description': 'Function templates, class templates, type traits, and C++20 concepts.',
            'chapters': [
                {
                    'title': 'Generic Templates & C++20 Concepts Constraints',
                    'duration_minutes': 30,
                    'is_free_preview': False,
                    'code_language': 'cpp',
                    'content_markdown': """# Generic Templates & C++20 Concepts Constraints

C++20 Concepts constrain template types at compile-time with clean compiler error diagnostics.

```cpp
#include <iostream>
#include <concepts>

template <typename T>
concept Numeric = std::integral<T> || std::floating_point<T>;

template <Numeric T>
T calculate_mean(T a, T b) {
    return (a + b) / 2;
}
```
""",
                    'code_snippet': """#include <iostream>

template <typename T>
T find_max(T a, T b) {
    return (a > b) ? a : b;
}

int main() {
    std::cout << "Max int: " << find_max(10, 20) << "\\n";
    std::cout << "Max float: " << find_max(3.14, 2.71) << "\\n";
    return 0;
}""",
                    'key_takeaways': [
                        'Templates generate specialized machine code at compile-time for each instantiated type.',
                        'Concepts eliminate cryptic multi-page SFINAE compiler errors.',
                        'Template code must typically reside in header files for compiler visibility.'
                    ],
                    'practice_questions': [
                        {
                            'question': 'What problem do C++20 Concepts solve over traditional SFINAE templates?',
                            'answer': 'Concepts provide readable, declarative constraints on template type parameters and produce clear, readable compiler error messages when requirements are not met.'
                        }
                    ]
                }
            ]
        },
        {
            'title': 'Module 6: STL Sequence Containers (Vector, Deque, List)',
            'description': 'Dynamic arrays with std::vector, memory capacity scaling, deque, and list.',
            'chapters': [
                {
                    'title': 'std::vector Internals, Capacity & Emplace',
                    'duration_minutes': 30,
                    'is_free_preview': False,
                    'code_language': 'cpp',
                    'content_markdown': """# std::vector Internals, Capacity & Emplace

`std::vector` is a contiguous dynamic array that doubles capacity upon reallocation.

```cpp
#include <iostream>
#include <vector>

int main() {
    std::vector<int> numbers;
    numbers.reserve(100); // Pre-allocate to prevent frequent reallocations

    for (int i = 0; i < 10; i++) {
        numbers.emplace_back(i * 10); // Construct in place
    }
    return 0;
}
```
""",
                    'code_snippet': """#include <iostream>
#include <vector>

int main() {
    std::vector<std::string> names = {"Alex", "Sarah", "David"};
    names.push_back("Elena");
    std::cout << "Size: " << names.size() << ", Capacity: " << names.capacity() << "\\n";
    return 0;
}""",
                    'key_takeaways': [
                        'Use vector.reserve() when the approximate element count is known upfront.',
                        'emplace_back constructs elements in-place, eliminating temporary copies.',
                        'Vector memory is contiguous, maximizing CPU L1/L2 cache locality.'
                    ],
                    'practice_questions': [
                        {
                            'question': 'How does emplace_back differ from push_back in std::vector?',
                            'answer': 'push_back accepts an existing object and copies or moves it into the vector. emplace_back forwards arguments directly to the element constructor to build the object in-place inside the allocated buffer.'
                        }
                    ]
                }
            ]
        },
        {
            'title': 'Module 7: STL Associative & Unordered Containers',
            'description': 'std::map (Red-Black Tree), std::unordered_map (Hash Table), set, and unordered_set.',
            'chapters': [
                {
                    'title': 'Map vs Unordered Map Performance Tradeoffs',
                    'duration_minutes': 25,
                    'is_free_preview': False,
                    'code_language': 'cpp',
                    'content_markdown': """# Map vs Unordered Map Performance Tradeoffs

- `std::map`: Implemented as a self-balancing Red-Black Tree. Maintains sorted keys. O(log N) lookup.
- `std::unordered_map`: Implemented as a hash table with bucket chaining. Average O(1) lookup.

```cpp
#include <iostream>
#include <unordered_map>

int main() {
    std::unordered_map<std::string, int> registry = {
        {"python", 1},
        {"cpp", 2},
        {"c", 3}
    };

    if (auto it = registry.find("cpp"); it != registry.end()) {
        std::cout << "Track ID: " << it->second << "\\n";
    }
    return 0;
}
```
""",
                    'code_snippet': """#include <iostream>
#include <map>

int main() {
    std::map<int, std::string> nodes;
    nodes[3] = "Leaf";
    nodes[1] = "Root";
    nodes[2] = "Branch";

    for (const auto& [id, label] : nodes) {
        std::cout << id << " -> " << label << "\\n"; // Sorted output: 1, 2, 3
    }
    return 0;
}""",
                    'key_takeaways': [
                        'Use std::unordered_map for O(1) lookups when ordering does not matter.',
                        'Use std::map when elements must be iterated in sorted order.',
                        'Use structured bindings (auto [k, v]) for clean pair iteration.'
                    ],
                    'practice_questions': [
                        {
                            'question': 'What is the time complexity of searching an element in std::map vs std::unordered_map?',
                            'answer': 'std::map has O(log N) worst-case time complexity (Red-Black Tree). std::unordered_map has O(1) average time complexity (Hash Table) and O(N) worst-case under severe hash collisions.'
                        }
                    ]
                }
            ]
        },
        {
            'title': 'Module 8: RAII & Smart Pointers (Memory Safety)',
            'description': 'Eliminating raw pointers using std::unique_ptr, std::shared_ptr, and std::weak_ptr.',
            'chapters': [
                {
                    'title': 'Smart Pointers & The Rule of Zero',
                    'duration_minutes': 30,
                    'is_free_preview': False,
                    'code_language': 'cpp',
                    'content_markdown': """# Smart Pointers & The Rule of Zero

Smart pointers in `<memory>` guarantee deterministic resource cleanup when pointers leave scope.

```cpp
#include <iostream>
#include <memory>

class SocketConnection {
public:
    SocketConnection() { std::cout << "Socket open\\n"; }
    ~SocketConnection() { std::cout << "Socket closed\\n"; }
};

void run() {
    auto conn = std::make_unique<SocketConnection>();
    // Automatic cleanup when conn leaves scope!
}
```
""",
                    'code_snippet': """#include <iostream>
#include <memory>

int main() {
    std::unique_ptr<int> ptr = std::make_unique<int>(42);
    std::cout << "Value: " << *ptr << "\\n";
    return 0;
}""",
                    'key_takeaways': [
                        'std::unique_ptr has zero runtime overhead over a raw pointer.',
                        'Always use std::make_unique and std::make_shared rather than manual new.',
                        'Use std::weak_ptr to break cyclic reference leaks in shared_ptr graphs.'
                    ],
                    'practice_questions': [
                        {
                            'question': 'Why should std::make_unique be used instead of unique_ptr<T>(new T())?',
                            'answer': 'std::make_unique is exception-safe and prevents potential memory leaks if an exception is thrown between new and smart pointer construction.'
                        }
                    ]
                }
            ]
        },
        {
            'title': 'Module 9: Move Semantics & Perfect Forwarding',
            'description': 'Rvalue references (T&&), std::move, move constructors, and std::forward.',
            'chapters': [
                {
                    'title': 'Rvalues, Move Constructors & std::move',
                    'duration_minutes': 30,
                    'is_free_preview': False,
                    'code_language': 'cpp',
                    'content_markdown': """# Rvalues, Move Constructors & std::move

Move semantics transfer resource ownership from temporary (rvalue) objects without deep memory copies.

```cpp
#include <iostream>
#include <vector>
#include <utility>

std::vector<int> generate_large_data() {
    std::vector<int> temp(1000000, 42);
    return temp; // Move constructed into caller with O(1) pointer swap
}
```
""",
                    'code_snippet': """#include <iostream>
#include <string>
#include <utility>

int main() {
    std::string str1 = "Techspire";
    std::string str2 = std::move(str1); // Ownership transferred
    std::cout << "str2: " << str2 << "\\n";
    return 0;
}""",
                    'key_takeaways': [
                        'std::move does not move data; it casts an lvalue to an rvalue reference (T&&).',
                        'Move operations swap internal pointers, running in O(1) constant time.',
                        'Never access a moved-from object except to assign to it or destroy it.'
                    ],
                    'practice_questions': [
                        {
                            'question': 'What does std::move actually do under the hood?',
                            'answer': 'It performs an unconditional static_cast to an rvalue reference type (T&&) allowing the compiler to select move constructors/assignment operators.'
                        }
                    ]
                }
            ]
        },
        {
            'title': 'Module 10: Modern C++ Concurrency & Multithreading',
            'description': 'std::thread, std::mutex, std::lock_guard, std::atomic, and std::async.',
            'chapters': [
                {
                    'title': 'Threads, Mutexes & Lock Guards',
                    'duration_minutes': 35,
                    'is_free_preview': False,
                    'code_language': 'cpp',
                    'content_markdown': """# Threads, Mutexes & Lock Guards

Safe concurrent programming using standard C++ multithreading primitives.

```cpp
#include <iostream>
#include <thread>
#include <mutex>

std::mutex mtx;
int shared_counter = 0;

void safe_increment() {
    std::lock_guard<std::mutex> lock(mtx); // RAII lock acquisition and release
    shared_counter++;
}
```
""",
                    'code_snippet': """#include <iostream>
#include <thread>

void worker(int id) {
    std::cout << "Thread " << id << " finished.\\n";
}

int main() {
    std::thread t1(worker, 1);
    t1.join();
    return 0;
}""",
                    'key_takeaways': [
                        'std::lock_guard uses RAII to guarantee mutex unlock upon scope exit.',
                        'std::atomic provides lock-free thread-safe atomic operations.',
                        'Always join() or detach() a std::thread before its destructor runs.'
                    ],
                    'practice_questions': [
                        {
                            'question': 'What happens if a std::thread object is destroyed while still joinable?',
                            'answer': 'std::terminate is called immediately, causing the entire process to crash.'
                        }
                    ]
                }
            ]
        }
    ],
    'assessment': {
        'title': 'Modern C++ Certification Exam',
        'description': 'Evaluates modern C++ idioms, RAII patterns, smart pointer lifetimes, and STL container complexity.',
        'passing_score': 70,
        'time_limit_minutes': 20,
        'questions': [
            {
                'question_text': 'Which smart pointer in C++ guarantees exclusive single ownership of a resource?',
                'question_type': 'single',
                'explanation': 'std::unique_ptr guarantees exclusive ownership and disables copy construction.',
                'points': 25,
                'options': [
                    {'text': 'std::shared_ptr', 'is_correct': False},
                    {'text': 'std::unique_ptr', 'is_correct': True},
                    {'text': 'std::weak_ptr', 'is_correct': False},
                    {'text': 'std::auto_ptr', 'is_correct': False}
                ]
            },
            {
                'question_text': 'What does RAII stand for in C++ software engineering?',
                'question_type': 'single',
                'explanation': 'RAII stands for Resource Acquisition Is Initialization, tying resource lifetime to object scope.',
                'points': 25,
                'options': [
                    {'text': 'Resource Allocation In Interfaces', 'is_correct': False},
                    {'text': 'Resource Acquisition Is Initialization', 'is_correct': True},
                    {'text': 'Runtime Architecture Internal Instruction', 'is_correct': False},
                    {'text': 'Recursive Array Index Integration', 'is_correct': False}
                ]
            },
            {
                'question_text': 'What is the average time complexity of key lookup in `std::unordered_map`?',
                'question_type': 'single',
                'explanation': 'std::unordered_map is implemented as a hash table with average O(1) constant time lookup.',
                'points': 25,
                'options': [
                    {'text': 'O(1)', 'is_correct': True},
                    {'text': 'O(log N)', 'is_correct': False},
                    {'text': 'O(N)', 'is_correct': False},
                    {'text': 'O(N log N)', 'is_correct': False}
                ]
            },
            {
                'question_text': 'Which utility function is used to convert an lvalue expression into an rvalue to invoke move constructors?',
                'question_type': 'single',
                'explanation': 'std::move casts an lvalue to an rvalue reference (T&&) enabling move semantics.',
                'points': 25,
                'options': [
                    {'text': 'std::forward', 'is_correct': False},
                    {'text': 'std::move', 'is_correct': True},
                    {'text': 'std::cast', 'is_correct': False},
                    {'text': 'std::transfer', 'is_correct': False}
                ]
            }
        ]
    }
}
