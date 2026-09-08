# -*- coding: utf-8 -*-
"""
Curriculum definition for Operating Systems & Low-Level Systems Architecture.
Comprehensive 10-module curriculum covering kernel design, process/thread management,
CPU scheduling, synchronization, virtual memory paging, file systems, IPC, and container isolation.
"""

OS_COURSE = {
    "title": "Operating Systems & Low-Level Systems Architecture",
    "slug": "operating-systems-low-level-architecture",
    "description": "Master kernel architectures, system calls, virtual memory paging, multithreading synchronization, file systems, IPC, and Linux namespaces.",
    "category": "systems",
    "level": "advanced",
    "duration_weeks": 11,
    "thumbnail_gradient": "from-slate-700 via-zinc-800 to-stone-900",
    "is_featured": True,
    "modules": [
        {
            "order": 1,
            "title": "Kernel Architecture & Hardware-OS Boundary",
            "description": "Dual-mode CPU execution, User vs Kernel space, Trap gates, Interrupt Vector Tables, and System Calls.",
            "chapters": [
                {
                    "order": 1,
                    "title": "Dual-Mode Execution & System Call Internals",
                    "description": "Trace hardware ring switching (Ring 3 to Ring 0) and the x86-64 syscall instruction boundary.",
                    "duration_minutes": 40,
                    "content": """# Dual-Mode Execution & System Call Internals

Modern processors enforce security and stability through hardware privilege levels (x86 CPU Rings):
- **Ring 0 (Kernel Mode)**: Unrestricted access to physical memory, CPU control registers (CR0, CR3), and I/O ports.
- **Ring 3 (User Mode)**: Sandboxed execution; privileged instructions trigger General Protection Faults (#GP).

## 1. The Anatomy of a System Call
When an application requests OS services (e.g. `read()`, `write()`, `mmap()`):
1. User application places system call number in register `RAX` and arguments in `RDI, RSI, RDX, R10, R8, R9`.
2. Executes `syscall` instruction $\\to$ CPU transitions privilege mode from Ring 3 to Ring 0.
3. Hardware saves User Instruction Pointer (`RIP`) to `RCX` and flags to `R11`.
4. CPU jumps to address stored in `MSR_LSTAR` (Model-Specific Register), entering `entry_SYSCALL_64`.
5. Kernel swaps user stack with kernel stack (`SWAPGS`), executes handler, and returns via `sysretq`.

```c
// Direct assembly invocation of write(1, "Hello\\n", 6) on Linux x86-64
#include <unistd.h>

void sys_write_direct(const char* msg, int len) {
    long syscall_num = 1; // __NR_write
    long fd = 1;          // STDOUT_FILENO
    long ret;
    
    __asm__ volatile (
        "movq %1, %%rax\\n"
        "movq %2, %%rdi\\n"
        "movq %3, %%rsi\\n"
        "movq %4, %%rdx\\n"
        "syscall\\n"
        "movq %%rax, %0\\n"
        : "=r"(ret)
        : "r"(syscall_num), "r"(fd), "r"(msg), "r"((long)len)
        : "rax", "rdi", "rsi", "rdx", "rcx", "r11", "memory"
    );
}
```

## Key Takeaways
- User applications never directly execute kernel functions; they issue traps/syscalls which safely transfer execution through controlled gates."""
                }
            ]
        },
        {
            "order": 2,
            "title": "Process Management, Threads & Context Switching",
            "description": "Process Control Block (PCB), process lifecycle, fork/exec, clone(), and hardware register context saving.",
            "chapters": [
                {
                    "order": 1,
                    "title": "Process Control Block & Context Switch Mechanism",
                    "description": "Understand register state preservation, kernel stack switching, and TLB cache invalidation.",
                    "duration_minutes": 45,
                    "content": """# Process Control Block & Context Switching

The Operating System represents every running program through a Process Control Block (`task_struct` in Linux).

## What Happens During a Context Switch?
1. An interrupt (Timer interrupt / I/O event) or voluntary yield (`sched_yield()`) transfers control to scheduler.
2. Kernel saves current process CPU registers (general purpose, instruction pointer `RIP`, stack pointer `RSP`) onto its kernel stack.
3. Scheduler selects the next candidate process from the runqueue.
4. If switching across distinct processes:
   - Kernel loads new Page Global Directory (CR3 register), changing the virtual-to-physical memory mapping.
   - Flushes non-global entries in the Translation Lookaside Buffer (TLB).
5. Restores the new process registers and resumes execution.

```c
#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>

int main() {
    pid_t pid = fork();
    if (pid == 0) {
        // Child Process (Copy-on-Write address space)
        printf("Child process (PID: %d), parent is %d\\n", getpid(), getppid());
        _exit(0);
    } else if (pid > 0) {
        // Parent Process
        int status;
        waitpid(pid, &status, 0); // Reclaim child PCB to prevent zombie state
        printf("Parent reaped child %d successfully\\n", pid);
    }
    return 0;
}
```"""
                }
            ]
        },
        {
            "order": 3,
            "title": "CPU Scheduling & Real-Time Dispatching",
            "description": "FCFS, SJF, Round-Robin, Completely Fair Scheduler (CFS), and Real-time priority inversion.",
            "chapters": [
                {
                    "order": 1,
                    "title": "Linux Completely Fair Scheduler (CFS) & Red-Black Runqueues",
                    "description": "Analyze virtual runtime (vruntime), decay factors, and O(log N) task selection.",
                    "duration_minutes": 45,
                    "content": """# Linux Completely Fair Scheduler (CFS)

CFS models an ideal Multi-tasking CPU where $N$ processes run simultaneously with equal power.

## Virtual Runtime (`vruntime`)
Each task tracks `vruntime`: the total CPU execution time weighted inversely by its nice level (priority):
$$vruntime += \\Delta \\text{exec\\_time} \\times \\frac{\\text{NICE\\_0\\_LOAD}}{\\text{task\\_weight}}$$

- Tasks are stored in a self-balancing **Red-Black Tree** ordered strictly by `vruntime`.
- The scheduler always picks the leftmost task (`rb_leftmost`), guaranteeing optimal fairness in $O(1)$ time.

## Key Takeaways
- Lower `vruntime` means a process has received less than its fair share of CPU, giving it highest priority to run next."""
                }
            ]
        },
        {
            "order": 4,
            "title": "Synchronization Primitives & Deadlock Resolution",
            "description": "Race conditions, Peterson's algorithm, Mutexes, Futexes, Semaphores, and Banker's Deadlock algorithm.",
            "chapters": [
                {
                    "order": 1,
                    "title": "Atomic Instructions, Spinlocks & Futexes",
                    "description": "Compare Test-and-Set / Compare-And-Swap (CAS) with Linux fast userspace mutexes (futex).",
                    "duration_minutes": 50,
                    "content": """# Concurrency Synchronization: Spinlocks vs Futex

## 1. Compare-And-Swap (Atomic CAS)
```c
#include <stdatomic.h>
#include <stdbool.h>

typedef struct {
    atomic_flag flag;
} spinlock_t;

void spin_lock(spinlock_t* lock) {
    // Busy-wait loop: Burns CPU cycles; ideal ONLY for very short lock holds
    while (atomic_flag_test_and_set_explicit(&lock->flag, memory_order_acquire)) {
        #if defined(__x86_64__)
        __builtin_ia32_pause(); // Yield pipeline execution slot
        #endif
    }
}

void spin_unlock(spinlock_t* lock) {
    atomic_flag_clear_explicit(&lock->flag, memory_order_release);
}
```

## 2. Linux Futex (Fast Userspace Mutex)
- **Uncontended case**: Acquired in user-space via a single atomic decrement instruction (zero syscall overhead).
- **Contended case**: System call `sys_futex(FUTEX_WAIT)` puts the colliding thread to sleep in kernel wait-queue, avoiding CPU burning."""
                },
                {
                    "order": 2,
                    "title": "Deadlock Detection & Coffman Conditions",
                    "description": "Prevent deadlocks by breaking Mutual Exclusion, Hold and Wait, No Preemption, or Circular Wait.",
                    "duration_minutes": 40,
                    "content": """# Deadlock Prevention & Coffman Conditions

A deadlock occurs if and only if all four **Coffman Conditions** hold simultaneously:
1. **Mutual Exclusion**: Resources cannot be shared concurrently.
2. **Hold and Wait**: Processes holding resources request new ones without releasing current holdings.
3. **No Preemption**: Resources cannot be forcibly seized from a process.
4. **Circular Wait**: A closed cycle of processes exists where each process waits for a resource held by the next.

## Prevention Strategy: Total Resource Ordering
Enforce a global hierarchy on all mutexes: always acquire Lock A before Lock B throughout the entire codebase to mathematically eliminate Circular Wait."""
                }
            ]
        },
        {
            "order": 5,
            "title": "Virtual Memory, Paging & TLB Architecture",
            "description": "Virtual address translation, 4-Level/5-Level Page Tables, TLB shootdowns, Page Fault handling, and LRU eviction.",
            "chapters": [
                {
                    "order": 1,
                    "title": "4-Level Page Table Translation & MMU",
                    "description": "Trace 48-bit canonical virtual address translation into physical frames via CR3, PGD, PUD, PMD, and PTE.",
                    "duration_minutes": 50,
                    "content": """# Virtual Address Translation on x86-64

The Memory Management Unit (MMU) translates virtual addresses to physical RAM using multi-level hierarchical page tables.

## 48-bit Virtual Address Decomposition (4KB Pages)
| Bits [47:39] | Bits [38:30] | Bits [29:21] | Bits [20:12] | Bits [11:0] |
| :---: | :---: | :---: | :---: | :---: |
| **PGD Index** (9b) | **PUD Index** (9b) | **PMD Index** (9b) | **PTE Index** (9b) | **Page Offset** (12b) |

```c
// Demonstrating Virtual Memory mapping with mmap()
#include <sys/mman.h>
#include <stdio.h>

int main() {
    size_t length = 4096 * 10; // 10 pages
    void* addr = mmap(
        NULL, 
        length, 
        PROT_READ | PROT_WRITE, 
        MAP_PRIVATE | MAP_ANONYMOUS, 
        -1, 
        0
    );
    
    // Memory is lazily allocated! Physical frames are assigned on first write (Page Fault #PF)
    int* ptr = (int*)addr;
    ptr[0] = 42; // Triggers Minor Page Fault, kernel assigns physical RAM page

    munmap(addr, length);
    return 0;
}
```

## Key Takeaways
- Translation Lookaside Buffer (TLB) caches recent translations to avoid 4 memory accesses per pointer dereference."""
                }
            ]
        },
        {
            "order": 6,
            "title": "File Systems Architecture & Storage I/O",
            "description": "Virtual File System (VFS), Inodes, Directory entries (dentry), Ext4 Extents, Journaling, and Page Cache.",
            "chapters": [
                {
                    "order": 1,
                    "title": "Inodes, Hard Links vs Soft Links & Ext4 Architecture",
                    "description": "Explore disk block indexing, superblock descriptors, inode tables, and atomic metadata journaling.",
                    "duration_minutes": 45,
                    "content": """# File System Internals: Inodes & VFS

In Unix-like systems, a file's name and directory structure are completely decoupled from its physical data blocks.

## The Inode Structure
An **inode** (Index Node) contains:
- File metadata (file size, permissions, owner UID/GID, modification timestamps).
- Block pointers or extent trees mapping logical file offsets to physical disk sectors.
- Link counter (number of directory entries referencing this inode).
- **Does NOT store the filename** (the filename is stored in directory entry `dentry` tables!).

```bash
# Inspecting inode numbers and link counts
ls -li file.txt
ln file.txt hardlink.txt   # Shares exact same inode; increments link count
ln -s file.txt symlink.txt # New inode with file path as content
```"""
                }
            ]
        },
        {
            "order": 7,
            "title": "Inter-Process Communication (IPC) & High-Performance I/O",
            "description": "Pipes, Shared Memory (POSIX shm), Unix Domain Sockets, epoll, and io_uring event rings.",
            "chapters": [
                {
                    "order": 1,
                    "title": "High-Concurrency I/O Multiplexing (epoll vs io_uring)",
                    "description": "Architect $O(1)$ event loops handling millions of concurrent socket connections.",
                    "duration_minutes": 50,
                    "content": """# I/O Multiplexing: epoll and io_uring

## 1. The Scaling Problem with `select()` and `poll()`
`select()` is $O(N)$: on every event, user space copies the entire descriptor set to kernel space, and the kernel linearly scans all descriptors.

## 2. Linux `epoll` ($O(1)$ Scalability)
- Maintains a kernel Red-Black tree of watched descriptors (`epoll_ctl`).
- Hardware interrupts place active descriptors onto a ready list (`epoll_wait`), returning only active events.

```c
#include <sys/epoll.h>
#include <unistd.h>

#define MAX_EVENTS 64

void event_loop(int server_fd) {
    int epoll_fd = epoll_create1(0);
    struct epoll_event ev, events[MAX_EVENTS];
    
    ev.events = EPOLLIN | EPOLLET; // Edge-triggered mode
    ev.data.fd = server_fd;
    epoll_ctl(epoll_fd, EPOLL_CTL_ADD, server_fd, &ev);

    while (1) {
        int nfds = epoll_wait(epoll_fd, events, MAX_EVENTS, -1);
        for (int n = 0; n < nfds; ++n) {
            // Process ready file descriptor without linear scanning
        }
    }
}
```"""
                }
            ]
        },
        {
            "order": 8,
            "title": "Device Drivers, Interrupts & Direct Memory Access",
            "description": "Interrupt Request (IRQ) lines, Top-Half vs Bottom-Half (Tasklets/Workqueues), and DMA ring buffers.",
            "chapters": [
                {
                    "order": 1,
                    "title": "Direct Memory Access (DMA) & Network Zero-Copy",
                    "description": "Bypass CPU memory copy operations using network ring buffers and splice() / sendfile().",
                    "duration_minutes": 45,
                    "content": """# Direct Memory Access & Zero-Copy I/O

Without DMA, the CPU must execute instructions to transfer every byte between peripheral devices and RAM (Programmed I/O).

## Direct Memory Access (DMA)
A dedicated DMA controller transfers data directly between network interface cards / disk controllers and main system memory without CPU involvement.

## Zero-Copy with `sendfile()`
Standard web server transfer involves 4 context switches and 4 data copies:
1. Disk $\\to$ OS Page Cache (DMA)
2. Page Cache $\\to$ User Space Buffer (CPU copy)
3. User Space $\\to$ Socket Buffer (CPU copy)
4. Socket Buffer $\\to$ NIC Buffer (DMA)

`sendfile()` transfers data directly from OS Page Cache to NIC Buffer in the kernel, eliminating all intermediate CPU buffer copies and user-space context switches!"""
                }
            ]
        },
        {
            "order": 9,
            "title": "Virtualization, Hypervisors & Container Internals",
            "description": "Hardware virtualization (VT-x/AMD-V), KVM, Linux namespaces (PID, NET, MNT), cgroups v2, and chroot.",
            "chapters": [
                {
                    "order": 1,
                    "title": "Linux Namespaces & Cgroups v2: How Containers Work",
                    "description": "Construct a lightweight container engine from scratch using unshare() and cgroups.",
                    "duration_minutes": 55,
                    "content": """# Container Primitives: Namespaces & Cgroups

A Docker container is NOT a virtual machine; it is a standard Linux process isolated using kernel **Namespaces** and resource-constrained using **Cgroups**.

## 1. Linux Namespaces (Isolation)
- `pid`: Isolates process IDs (container process sees itself as PID 1).
- `net`: Isolates network interfaces, routing tables, and IP ports.
- `mnt`: Isolates filesystem mount points.
- `ipc`: Isolates System V IPC and POSIX message queues.
- `uts`: Isolates hostname and domain name.
- `user`: Maps container root UID 0 to an unprivileged UID on host.

```bash
# Creating an isolated process namespace
unshare --mount --uts --ipc --net --pid --fork bash
```

## 2. Control Groups (Cgroups v2 Resource Throttling)
Cgroups limit and measure memory, CPU quotas, and I/O bandwidth:
```bash
# Limit process memory to 256MB in cgroups v2
mkdir /sys/fs/cgroup/sandbox
echo "268435456" > /sys/fs/cgroup/sandbox/memory.max
echo $$ > /sys/fs/cgroup/sandbox/cgroup.procs
```"""
                }
            ]
        },
        {
            "order": 10,
            "title": "Operating System Security & Kernel Sandboxing",
            "description": "Address Space Layout Randomization (ASLR), Non-Executable Stack (DEP/NX), seccomp-bpf, and capabilities.",
            "chapters": [
                {
                    "order": 1,
                    "title": "Seccomp-BPF Syscall Sandboxing & Linux Capabilities",
                    "description": "Restrict process attack surfaces by blocking dangerous syscalls using Berkeley Packet Filters.",
                    "duration_minutes": 45,
                    "content": """# Seccomp-BPF Syscall Sandboxing

Secure Computing Mode (seccomp) with Berkeley Packet Filters attaches a programmable filter to a process to restrict allowed system calls.

```c
#include <seccomp.h>
#include <unistd.h>
#include <stdio.h>

void lockdown_process() {
    scmp_filter_ctx ctx = seccomp_init(SCMP_ACT_KILL); // Default action: kill on violation
    
    // Whitelist only safe syscalls
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(read), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(write), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(exit_group), 0);
    
    seccomp_load(ctx);
    seccomp_release(ctx);
}

int main() {
    lockdown_process();
    printf("Process locked down. Read/write permitted.\\n");
    // Any attempt to call fork(), execve(), or socket() will instantly terminate the process (#SIGSYS)
    return 0;
}
```

## Key Takeaways
- Defense in depth: Combining unprivileged Linux capabilities, seccomp filters, and read-only mount namespaces guarantees robust zero-trust sandboxing."""
                }
            ]
        }
    ],
    "assessment": {
        "title": "Operating Systems & Low-Level Architecture Certification Exam",
        "description": "Assess your understanding of hardware rings, page table translations, scheduling algorithms, and Linux container primitives.",
        "passing_score": 70,
        "time_limit_minutes": 25,
        "questions": [
            {
                "question_text": "What hardware mechanism is used to transition CPU privilege from User Mode (Ring 3) to Kernel Mode (Ring 0) during a system call?",
                "question_type": "single",
                "explanation": "The CPU executes a software trap instruction (e.g. `syscall` or `int 0x80`), which switches privilege levels and jumps to the kernel entry point defined in MSR registers.",
                "points": 20,
                "options": [
                    {"text": "A CPU hardware trap instruction (`syscall`) switching privilege levels", "is_correct": True},
                    {"text": "A standard C function pointer call", "is_correct": False},
                    {"text": "Overwriting the L1 CPU cache", "is_correct": False},
                    {"text": "A direct branch instruction to physical RAM address 0x0", "is_correct": False}
                ]
            },
            {
                "question_text": "In the Linux Completely Fair Scheduler (CFS), how is the next task to execute chosen from the runqueue?",
                "question_type": "single",
                "explanation": "CFS maintains a Red-Black tree ordered by virtual runtime (`vruntime`) and always dispatches the leftmost node with the lowest accumulated `vruntime`.",
                "points": 20,
                "options": [
                    {"text": "The leftmost node in the Red-Black tree with the lowest `vruntime`", "is_correct": True},
                    {"text": "A FIFO queue based solely on arrival time", "is_correct": False},
                    {"text": "Random selection among active processes", "is_correct": False},
                    {"text": "The process holding the most open file descriptors", "is_correct": False}
                ]
            },
            {
                "question_text": "Which condition is NOT one of the four Coffman conditions required for a deadlock to occur?",
                "question_type": "single",
                "explanation": "Preemption PREVENTS deadlocks. The Coffman condition is 'No Preemption' (resources cannot be forcibly seized).",
                "points": 20,
                "options": [
                    {"text": "Forced Preemption", "is_correct": True},
                    {"text": "Mutual Exclusion", "is_correct": False},
                    {"text": "Hold and Wait", "is_correct": False},
                    {"text": "Circular Wait", "is_correct": False}
                ]
            },
            {
                "question_text": "What role does the Translation Lookaside Buffer (TLB) play in virtual memory architecture?",
                "question_type": "single",
                "explanation": "The TLB is a high-speed hardware cache in the MMU that stores recent virtual-to-physical address mappings, avoiding multi-level page table traversals in RAM.",
                "points": 20,
                "options": [
                    {"text": "It caches recent virtual-to-physical page translations to accelerate memory access", "is_correct": True},
                    {"text": "It stores hard disk drive sector mappings", "is_correct": False},
                    {"text": "It compresses RAM pages when memory is low", "is_correct": False},
                    {"text": "It encrypts network packets at the socket level", "is_correct": False}
                ]
            },
            {
                "question_text": "How do Linux Namespaces differ from Linux Control Groups (Cgroups) in container virtualization?",
                "question_type": "single",
                "explanation": "Namespaces provide isolation (what a container can see: PIDs, mount points, networks), while Cgroups enforce resource limits (what a container can consume: CPU, memory, I/O).",
                "points": 20,
                "options": [
                    {"text": "Namespaces provide resource isolation/visibility, while Cgroups enforce resource quotas", "is_correct": True},
                    {"text": "Namespaces are implemented in user space, while Cgroups are in the compiler", "is_correct": False},
                    {"text": "Cgroups are only used on Windows", "is_correct": False},
                    {"text": "There is no difference; they are identical", "is_correct": False}
                ]
            }
        ]
    }
}
