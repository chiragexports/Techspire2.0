C_COURSE = {
    'title': 'C Systems Programming',
    'slug': 'c-programming',
    'tagline': 'Master memory addresses, pointers, structs, dynamic allocation, and low-level hardware interaction.',
    'description': 'An intensive deep-dive into C99/C11 systems programming. Understand pointers, pointer arithmetic, memory layouts, cache locality, malloc/free implementations, system calls, and file I/O.',
    'category': 'Systems Engineering',
    'category_icon': 'Cpu',
    'difficulty': 'intermediate',
    'estimated_hours': 40,
    'badge_icon': 'Binary',
    'color_accent': '#06B6D4',
    'order': 2,
    'prerequisites': ['Basic programming logic and familiarity with binary representation'],
    'learning_outcomes': [
        'Master memory address manipulation and multi-level pointers',
        'Perform safe dynamic memory allocation with malloc, calloc, realloc, and free',
        'Construct custom data structures using structs, unions, bitfields, and enum flags',
        'Debug segmentation faults, memory leaks, and buffer overflows with Valgrind & GDB'
    ],
    'modules': [
        {
            'title': 'Module 1: C Fundamentals, Compilation & Toolchains',
            'description': 'GCC toolchain, preprocessor, compiler, assembler, linker, and process memory segments.',
            'chapters': [
                {
                    'title': 'The Four Stages of C Compilation & Object Code',
                    'duration_minutes': 25,
                    'is_free_preview': True,
                    'code_language': 'c',
                    'content_markdown': """# The Four Stages of C Compilation & Object Code

A C program goes through four distinct transformations before becoming an executable ELF binary:
1. **Preprocessing (`gcc -E`)**: Expands `#include` headers, evaluates `#define` macros, and strips comments.
2. **Compilation (`gcc -S`)**: Translates preprocessed C code into architecture-specific Assembly instructions.
3. **Assembly (`gcc -c`)**: Translates assembly instructions into relocatable machine code (`.o` object files).
4. **Linking (`gcc -o`)**: Resolves symbol references, merges object files, and links libc/external libraries into an executable.

```c
#include <stdio.h>

#define MAX_BUFFER 1024

int main(void) {
    printf("Buffer size: %d\\n", MAX_BUFFER);
    return 0;
}
```
""",
                    'code_snippet': """#include <stdio.h>

int main() {
    printf("Techspire Systems Engine Online\\n");
    return 0;
}""",
                    'key_takeaways': [
                        'The preprocessor performs purely textual substitution before parsing.',
                        'Object files contain unresolved symbols that the linker binds.',
                        'Always compile with -Wall -Wextra -Werror for strict safety.'
                    ],
                    'practice_questions': [
                        {
                            'question': 'What is the purpose of the linker stage in compilation?',
                            'answer': 'The linker resolves cross-module function calls, static memory offsets, and binds external libraries (like libc) into a final executable binary.'
                        }
                    ]
                }
            ]
        },
        {
            'title': 'Module 2: Data Types, Operators & Control Flow',
            'description': 'Primitive sizes, two\'s complement signed integers, bitwise operations, and flow control.',
            'chapters': [
                {
                    'title': 'Data Type Representations & Two\'s Complement Integers',
                    'duration_minutes': 25,
                    'is_free_preview': True,
                    'code_language': 'c',
                    'content_markdown': """# Data Type Representations & Two\'s Complement Integers

C integers are represented using two\'s complement binary format for signed types.

```c
#include <stdio.h>
#include <stdint.h>

void inspect_types(void) {
    int32_t a = -1;
    uint32_t b = (uint32_t)a;

    printf("Signed value: %d\\n", a);
    printf("Unsigned bit pattern: 0x%08X\\n", b); // 0xFFFFFFFF
}
```
""",
                    'code_snippet': """#include <stdio.h>

int main() {
    int x = 5; // 0101
    int y = 3; // 0011
    printf("x & y = %d\\n", x & y); // 0001 (1)
    printf("x | y = %d\\n", x | y); // 0111 (7)
    return 0;
}""",
                    'key_takeaways': [
                        'Use stdint.h (int32_t, uint64_t) for fixed-width portability across architectures.',
                        'Signed integer overflow is undefined behavior (UB) in C.',
                        'Bitwise operations provide high-performance flag manipulations.'
                    ],
                    'practice_questions': [
                        {
                            'question': 'Why is <stdint.h> preferred over primitive types like int or long?',
                            'answer': 'Primitive types have platform-dependent sizes (e.g., long is 4 bytes on Windows 64-bit but 8 bytes on Linux 64-bit), while stdint types guarantee fixed byte sizes across all platforms.'
                        }
                    ]
                }
            ]
        },
        {
            'title': 'Module 3: Functions, Call Stacks & Scope',
            'description': 'Stack frame layouts, base pointer (EBP/RBP), return addresses, and recursion.',
            'chapters': [
                {
                    'title': 'Stack Frame Layout & Activation Records',
                    'duration_minutes': 25,
                    'is_free_preview': False,
                    'code_language': 'c',
                    'content_markdown': """# Stack Frame Layout & Activation Records

Every function call pushes an **activation record (stack frame)** onto the process call stack containing:
1. Function arguments.
2. Return instruction pointer (RIP).
3. Saved base frame pointer (RBP).
4. Local variables.

```c
#include <stdio.h>

int factorial(int n) {
    if (n <= 1) return 1;
    return n * factorial(n - 1);
}
```
""",
                    'code_snippet': """#include <stdio.h>

void print_stack_direction(int *parent_addr) {
    int local_var;
    if (&local_var < parent_addr) {
        printf("Stack grows downwards towards lower memory addresses.\\n");
    } else {
        printf("Stack grows upwards towards higher memory addresses.\\n");
    }
}

int main() {
    int main_var;
    print_stack_direction(&main_var);
    return 0;
}""",
                    'key_takeaways': [
                        'Local variables reside in stack frames and are destroyed upon function return.',
                        'Never return the address of a local stack variable (leads to dangling pointer UB).',
                        'Excessive recursion without base case causes stack overflow crashes.'
                    ],
                    'practice_questions': [
                        {
                            'question': 'Why is returning a pointer to a local stack variable dangerous in C?',
                            'answer': 'When the function returns, its stack frame is popped and the memory is reclaimed. The pointer becomes dangling, and reading/writing it causes undefined behavior or memory corruption.'
                        }
                    ]
                }
            ]
        },
        {
            'title': 'Module 4: Pointers, Memory Addresses & Arithmetic',
            'description': 'Pointers, dereferencing, multi-level pointers, void pointers, and pointer arithmetic.',
            'chapters': [
                {
                    'title': 'Pointer Mechanics & Pointer Arithmetic Scaling',
                    'duration_minutes': 30,
                    'is_free_preview': False,
                    'code_language': 'c',
                    'content_markdown': """# Pointer Mechanics & Pointer Arithmetic Scaling

A pointer is a variable that holds the raw memory address of another object.

## 1. Pointer Arithmetic Scaling
Adding `1` to a pointer advances it by `sizeof(*ptr)` bytes:

```c
#include <stdio.h>

int main(void) {
    int arr[] = {10, 20, 30, 40};
    int *p = arr;

    printf("Value at p: %d\\n", *p);         // 10
    printf("Value at p+2: %d\\n", *(p + 2)); // 30 (offset by 2 * sizeof(int) = 8 bytes)
    return 0;
}
```
""",
                    'code_snippet': """#include <stdio.h>

void swap(int *a, int *b) {
    int temp = *a;
    *a = *b;
    *b = temp;
}

int main() {
    int x = 10, y = 20;
    swap(&x, &y);
    printf("Swapped: x=%d, y=%d\\n", x, y);
    return 0;
}""",
                    'key_takeaways': [
                        'The dereference operator (*) accesses the memory location pointed to.',
                        'The address-of operator (&) extracts the memory address of an lvalue.',
                        'Pointer arithmetic automatically multiplies offsets by sizeof(type).'
                    ],
                    'practice_questions': [
                        {
                            'question': 'What is a void* pointer in C and what are its restrictions?',
                            'answer': 'A void* is a generic pointer that can point to any type. It cannot be directly dereferenced or used in pointer arithmetic without explicit type casting.'
                        }
                    ]
                }
            ]
        },
        {
            'title': 'Module 5: Arrays, C-Strings & Buffer Safety',
            'description': 'Contiguous memory layout, null-terminated strings, and buffer overflow prevention.',
            'chapters': [
                {
                    'title': 'Null-Terminated Strings & Safe String APIs',
                    'duration_minutes': 25,
                    'is_free_preview': False,
                    'code_language': 'c',
                    'content_markdown': """# Null-Terminated Strings & Safe String APIs

In C, strings are contiguous arrays of `char` terminated by a null byte (`\\0`).

```c
#include <stdio.h>
#include <string.h>

void safe_string_copy(char *dest, size_t dest_size, const char *src) {
    // Avoid unsafe strcpy; use snprintf or strncpy with explicit null termination
    snprintf(dest, dest_size, "%s", src);
}
```
""",
                    'code_snippet': """#include <stdio.h>
#include <string.h>

int main() {
    char str[] = "Techspire";
    printf("String length: %zu\\n", strlen(str)); // 9
    printf("Array size in bytes: %zu\\n", sizeof(str)); // 10 (includes null byte)
    return 0;
}""",
                    'key_takeaways': [
                        'Always allocate length + 1 bytes to accommodate the null terminator.',
                        'Never use gets() or unbounded strcpy() which cause buffer overflow exploits.',
                        'strlen counts characters up to the null byte; sizeof returns total buffer bytes.'
                    ],
                    'practice_questions': [
                        {
                            'question': 'What is the security risk of using strcpy instead of snprintf/strncpy?',
                            'answer': 'strcpy does not check destination buffer boundaries. If the source string is longer than the destination buffer, it overwrites adjacent stack memory causing a buffer overflow vulnerability.'
                        }
                    ]
                }
            ]
        },
        {
            'title': 'Module 6: User-Defined Types (Structs, Unions & Enums)',
            'description': 'Struct memory alignment, padding, bitfields, unions, and enums.',
            'chapters': [
                {
                    'title': 'Structure Memory Alignment & Padding Optimization',
                    'duration_minutes': 30,
                    'is_free_preview': False,
                    'code_language': 'c',
                    'content_markdown': """# Structure Memory Alignment & Padding Optimization

Hardware architectures read memory more efficiently when data types are aligned to address boundaries that are multiples of their size.

```c
#include <stdio.h>

// Unoptimized struct: 12 bytes due to padding
struct BadLayout {
    char a;    // 1 byte + 3 bytes padding
    int b;     // 4 bytes
    char c;    // 1 byte + 3 bytes padding
};

// Optimized struct: 8 bytes
struct GoodLayout {
    int b;     // 4 bytes
    char a;    // 1 byte
    char c;    // 1 byte + 2 bytes padding
};
```
""",
                    'code_snippet': """#include <stdio.h>

typedef struct {
    int id;
    float grade;
} Student;

int main() {
    Student s = {1, 98.5f};
    printf("Student ID: %d, Grade: %.1f\\n", s.id, s.grade);
    return 0;
}""",
                    'key_takeaways': [
                        'Compilers insert padding bytes between struct members to satisfy hardware alignment.',
                        'Order struct members from largest to smallest to minimize memory waste.',
                        'Unions share the same memory location across all members, sizing to the largest member.'
                    ],
                    'practice_questions': [
                        {
                            'question': 'How does a union differ from a struct in C?',
                            'answer': 'In a struct, each member has its own dedicated memory offset. In a union, all members share the same starting memory address, and the union size is determined by its largest member.'
                        }
                    ]
                }
            ]
        },
        {
            'title': 'Module 7: Dynamic Memory Allocation (Heap Management)',
            'description': 'Heap management using malloc, calloc, realloc, and free, avoiding leaks and double frees.',
            'chapters': [
                {
                    'title': 'Heap Allocation Mechanics, Leak Prevention & Realloc',
                    'duration_minutes': 35,
                    'is_free_preview': False,
                    'code_language': 'c',
                    'content_markdown': """# Heap Allocation Mechanics, Leak Prevention & Realloc

Dynamic memory is allocated on the heap via runtime system calls (`brk`/`sbrk`/`mmap`).

```c
#include <stdio.h>
#include <stdlib.h>

int* create_dynamic_array(size_t size) {
    int *arr = (int*)malloc(size * sizeof(int));
    if (!arr) {
        perror("Memory allocation failed");
        return NULL;
    }
    return arr;
}
```
""",
                    'code_snippet': """#include <stdio.h>
#include <stdlib.h>

int main() {
    int *data = (int*)calloc(5, sizeof(int));
    if (!data) return 1;

    for (int i = 0; i < 5; i++) data[i] = (i + 1) * 10;
    for (int i = 0; i < 5; i++) printf("%d ", data[i]);
    printf("\\n");

    free(data);
    data = NULL; // Safe pointer neutralization
    return 0;
}""",
                    'key_takeaways': [
                        'Always verify that malloc/calloc return value is not NULL before using.',
                        'Every dynamic allocation must have exactly one corresponding free() call.',
                        'Set pointers to NULL immediately after calling free() to prevent double-free bugs.'
                    ],
                    'practice_questions': [
                        {
                            'question': 'What is the risk of using realloc(ptr, new_size) without a temporary pointer?',
                            'answer': 'If realloc fails, it returns NULL without freeing the original buffer. If you assign the return directly to ptr, you lose the reference and create an unrecoverable memory leak.'
                        }
                    ]
                }
            ]
        },
        {
            'title': 'Module 8: File I/O, Streams & Binary Data',
            'description': 'File descriptors, buffered I/O with fopen/fread/fwrite, and binary record storage.',
            'chapters': [
                {
                    'title': 'Buffered File I/O & Binary Serialization',
                    'duration_minutes': 25,
                    'is_free_preview': False,
                    'code_language': 'c',
                    'content_markdown': """# Buffered File I/O & Binary Serialization

C provides buffered I/O streams using `FILE*` handles defined in `<stdio.h>`.

```c
#include <stdio.h>

typedef struct {
    int id;
    char name[32];
} Record;

int save_record(const char *filename, Record *r) {
    FILE *fp = fopen(filename, "wb");
    if (!fp) return -1;
    size_t written = fwrite(r, sizeof(Record), 1, fp);
    fclose(fp);
    return (written == 1) ? 0 : -1;
}
```
""",
                    'code_snippet': """#include <stdio.h>

int main() {
    FILE *fp = fopen("output.txt", "w");
    if (fp) {
        fprintf(fp, "Techspire Systems Engine\\n");
        fclose(fp);
        printf("Wrote output file successfully.\\n");
    }
    return 0;
}""",
                    'key_takeaways': [
                        'Always check if fopen returned NULL before performing read/write operations.',
                        'Use binary mode ("rb"/"wb") for cross-platform binary data serialization.',
                        'Always close opened file streams with fclose() to flush internal buffers.'
                    ],
                    'practice_questions': [
                        {
                            'question': 'What is the difference between text mode ("r") and binary mode ("rb") in fopen?',
                            'answer': 'Text mode translates line endings (like \\r\\n to \\n on Windows), which can corrupt raw binary files. Binary mode preserves byte sequences exactly.'
                        }
                    ]
                }
            ]
        },
        {
            'title': 'Module 9: C Preprocessor & Multi-File Architecture',
            'description': 'Header guards (#ifndef / #pragma once), static internal linkage, and Makefiles.',
            'chapters': [
                {
                    'title': 'Header Guards, Static Linkage & Makefiles',
                    'duration_minutes': 25,
                    'is_free_preview': False,
                    'code_language': 'c',
                    'content_markdown': """# Header Guards, Static Linkage & Makefiles

Preventing multiple header inclusion and managing symbol visibility across translation units.

```c
// math_utils.h
#ifndef MATH_UTILS_H
#define MATH_UTILS_H

int calculate_crc(const char *data, size_t len);

#endif // MATH_UTILS_H
```
""",
                    'code_snippet': """// static limits function scope to this translation unit
static int internal_helper(void) {
    return 42;
}

int public_api(void) {
    return internal_helper() * 2;
}""",
                    'key_takeaways': [
                        'Header guards prevent duplicate type definition compilation errors.',
                        'The static keyword on global functions/variables enforces internal linkage.',
                        'Makefiles automate dependency tracking and incremental compilation.'
                    ],
                    'practice_questions': [
                        {
                            'question': 'What does the static keyword do when applied to a global variable in C?',
                            'answer': 'It restricts the variable\'s scope (visibility) to the current translation unit (.c file), preventing linker name collisions with other files.'
                        }
                    ]
                }
            ]
        },
        {
            'title': 'Module 10: Systems Programming, Signals & Debugging',
            'description': 'System calls, POSIX signal handling, Valgrind memory leak auditing, and GDB.',
            'chapters': [
                {
                    'title': 'POSIX Signals, Valgrind & GDB Debugging',
                    'duration_minutes': 35,
                    'is_free_preview': False,
                    'code_language': 'c',
                    'content_markdown': """# POSIX Signals, Valgrind & GDB Debugging

Debugging segmentation faults and memory leaks using industry toolchains.

```c
#include <stdio.h>
#include <signal.h>
#include <stdlib.h>

void sigint_handler(int signum) {
    printf("\\n[SHUTDOWN] Intercepted SIGINT (%d). Gracefully exiting...\\n", signum);
    exit(0);
}
```
""",
                    'code_snippet': """#include <stdio.h>
#include <signal.h>

int main() {
    printf("Process PID ready for POSIX signals.\\n");
    return 0;
}""",
                    'key_takeaways': [
                        'Valgrind detects memory leaks, invalid heap reads, and use-after-free bugs.',
                        'Compile with gcc -g to generate DWARF debugging symbols for GDB.',
                        'Signal handlers must be reentrant and only call async-signal-safe functions.'
                    ],
                    'practice_questions': [
                        {
                            'question': 'What is the primary function of Valgrind\'s memcheck tool?',
                            'answer': 'It tracks all memory allocations, reads, and writes in user space to detect memory leaks, uninitialized memory usage, and out-of-bounds buffer accesses.'
                        }
                    ]
                }
            ]
        }
    ],
    'assessment': {
        'title': 'C Systems Programming Assessment',
        'description': 'Verification exam covering process memory, pointer arithmetic, dynamic memory management, and struct alignment.',
        'passing_score': 70,
        'time_limit_minutes': 20,
        'questions': [
            {
                'question_text': 'What is the size in bytes added to a pointer `char *p` when evaluating `p + 4`?',
                'question_type': 'single',
                'explanation': 'sizeof(char) is always 1 byte according to the C specification. Therefore, p + 4 advances 4 bytes.',
                'points': 25,
                'options': [
                    {'text': '1 byte', 'is_correct': False},
                    {'text': '4 bytes', 'is_correct': True},
                    {'text': '8 bytes', 'is_correct': False},
                    {'text': '16 bytes', 'is_correct': False}
                ]
            },
            {
                'question_text': 'Which standard library function allocates memory on the heap and initializes all bytes to zero?',
                'question_type': 'single',
                'explanation': 'calloc(count, size) allocates contiguous memory and clears all bits to zero.',
                'points': 25,
                'options': [
                    {'text': 'malloc()', 'is_correct': False},
                    {'text': 'calloc()', 'is_correct': True},
                    {'text': 'realloc()', 'is_correct': False},
                    {'text': 'alloca()', 'is_correct': False}
                ]
            },
            {
                'question_text': 'What condition causes a "dangling pointer" in C?',
                'question_type': 'single',
                'explanation': 'A dangling pointer arises when a pointer continues to hold the memory address of an object that has already been deallocated by free() or gone out of stack scope.',
                'points': 25,
                'options': [
                    {'text': 'A pointer that points to a memory location that has already been freed', 'is_correct': True},
                    {'text': 'A pointer that has been explicitly assigned to NULL', 'is_correct': False},
                    {'text': 'A pointer storing a negative memory address', 'is_correct': False},
                    {'text': 'A pointer pointing to the Text Segment', 'is_correct': False}
                ]
            },
            {
                'question_text': 'What will be the output of `printf("%d", *(&x));` where `int x = 100;`?',
                'question_type': 'single',
                'explanation': '&x retrieves the memory address of x, and * dereferences that address back to the value of x (100).',
                'points': 25,
                'options': [
                    {'text': 'The hexadecimal memory address of x', 'is_correct': False},
                    {'text': '100', 'is_correct': True},
                    {'text': '0', 'is_correct': False},
                    {'text': 'Compilation error', 'is_correct': False}
                ]
            }
        ]
    }
}
