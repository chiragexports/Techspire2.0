# -*- coding: utf-8 -*-
"""
Curriculum definition for Data Structures & Algorithms in Depth.
Comprehensive 10-module curriculum covering asymptotic complexity, fundamental & advanced
data structures, algorithmic paradigms, graph algorithms, and dynamic programming.
"""

DSA_COURSE = {
    "title": "Data Structures & Algorithms in Depth",
    "slug": "data-structures-algorithms-depth",
    "description": "Master algorithmic problem solving, time and space asymptotic complexity, advanced trees, graphs, and dynamic programming patterns.",
    "category": "computer-science",
    "level": "advanced",
    "duration_weeks": 12,
    "thumbnail_gradient": "from-emerald-600 via-teal-700 to-cyan-900",
    "is_featured": True,
    "modules": [
        {
            "order": 1,
            "title": "Asymptotic Analysis & Mathematical Foundations",
            "description": "Big-O, Big-Omega, Big-Theta, Master Theorem, and Amortized Complexity analysis.",
            "chapters": [
                {
                    "order": 1,
                    "title": "Big-O Notation & Growth Rates",
                    "description": "Formal definitions of asymptotic bounds, Dominance rules, and common complexity classes.",
                    "duration_minutes": 35,
                    "content": """# Asymptotic Analysis & Growth Rates

Asymptotic analysis evaluates algorithm performance as input size $N \to \infty$, independent of specific hardware or compiler optimizations.

## 1. Mathematical Definitions

- **Big-O ($O$)**: Asymptotic upper bound. $f(n) = O(g(n))$ if $\exists c > 0, n_0$ such that $0 \le f(n) \le c \cdot g(n)$ for all $n \ge n_0$.
- **Big-$\Omega$ ($\Omega$)**: Asymptotic lower bound. $f(n) = \Omega(g(n))$ if $f(n) \ge c \cdot g(n)$ for all $n \ge n_0$.
- **Big-$\Theta$ ($\Theta$)**: Asymptotic tight bound. $f(n) = \Theta(g(n)) \iff f(n) = O(g(n)) \land f(n) = \Omega(g(n))$.

## Complexity Classes Hierarchy
$$O(1) < O(\log N) < O(N) < O(N \log N) < O(N^2) < O(2^N) < O(N!)$$

```python
# Comparing Growth Rates in Practice
def constant_time(arr: list[int]) -> int:
    return arr[0] if arr else -1  # O(1)

def logarithmic_time(n: int) -> int:
    steps = 0
    while n > 1:
        n //= 2
        steps += 1
    return steps  # O(log n)
```

## Key Takeaways
- Always drop lower-order terms and constant coefficients ($3N^2 + 5N + 100 \implies O(N^2)$).
- Analyze worst-case, average-case, and best-case performance independently."""
                },
                {
                    "order": 2,
                    "title": "Amortized Analysis & Recurrence Relations",
                    "description": "Master Theorem, Recursion Trees, and Aggregate/Accounting Amortized methods.",
                    "duration_minutes": 40,
                    "content": """# Amortized Analysis & Recurrence Relations

## 1. The Master Theorem
For recurrences of the form $T(n) = a T(n/b) + O(n^d)$:
1. If $d < \log_b a \implies T(n) = O(n^{\log_b a})$
2. If $d = \log_b a \implies T(n) = O(n^d \log n)$
3. If $d > \log_b a \implies T(n) = O(n^d)$

## 2. Dynamic Array Resizing (Amortized $O(1)$)
When an array doubles in capacity each time it fills up:
- Cost of inserting $N$ elements = $N$ (normal insertions) + $(1 + 2 + 4 + ... + N) \approx 3N$ operations.
- Average cost per operation = $3N / N = O(1)$ amortized time.

## Key Takeaways
- Even if a single operation takes $O(N)$ worst-case (array reallocation), the sequence of $N$ operations is bounded by $O(N)$, giving $O(1)$ amortized cost."""
                }
            ]
        },
        {
            "order": 2,
            "title": "Linear Data Structures: Arrays & Linked Lists",
            "description": "Dynamic arrays, Singly/Doubly linked lists, Skip lists, and pointer cycle detection.",
            "chapters": [
                {
                    "order": 1,
                    "title": "Singly & Doubly Linked List Implementation",
                    "description": "Build high-performance linked lists with pointer manipulation and sentinel nodes.",
                    "duration_minutes": 40,
                    "content": """# Singly & Doubly Linked Lists

Linked lists store nodes containing data and pointer references to adjacent nodes.

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class SinglyLinkedList:
    def __init__(self):
        self.head = None

    def insert_head(self, val: int):
        new_node = ListNode(val, self.head)
        self.head = new_node

    def reverse(self):
        prev = None
        curr = self.head
        while curr:
            next_temp = curr.next
            curr.next = prev
            prev = curr
            curr = next_temp
        self.head = prev
```

## Key Takeaways
- Linked lists provide $O(1)$ head insertion/deletion without shifting elements, but lack $O(1)$ random indexing ($O(N)$ lookup)."""
                },
                {
                    "order": 2,
                    "title": "Fast & Slow Pointers (Floyd's Cycle Detection)",
                    "description": "Detect cycles in linked lists and locate cycle entry points in O(1) space.",
                    "duration_minutes": 35,
                    "content": """# Floyd's Cycle Detection Algorithm

The Tortoise and Hare algorithm detects loops in $O(N)$ time and $O(1)$ auxiliary memory.

```python
def detect_cycle_entry(head: ListNode) -> ListNode | None:
    slow = head
    fast = head

    # Phase 1: Determine if a cycle exists
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            break
    else:
        return None  # No cycle

    # Phase 2: Find cycle entry node
    entry = head
    while entry != slow:
        entry = entry.next
        slow = slow.next

    return entry
```

## Mathematical Proof
Distance from head to cycle entry equals distance from collision point to cycle entry modulo loop length."""
                }
            ]
        },
        {
            "order": 3,
            "title": "Stacks, Queues & Monotonic Variants",
            "description": "LIFO/FIFO paradigms, circular ring buffers, min-stacks, and monotonic stacks for range queries.",
            "chapters": [
                {
                    "order": 1,
                    "title": "Stack & Queue Internals with Ring Buffers",
                    "description": "Implement thread-safe circular queues and $O(1)$ MinStack.",
                    "duration_minutes": 35,
                    "content": """# Circular Ring Buffers & MinStack

```python
class MinStack:
    def __init__(self):
        self.stack = []
        self.min_stack = []

    def push(self, val: int) -> None:
        self.stack.append(val)
        current_min = min(val, self.min_stack[-1] if self.min_stack else val)
        self.min_stack.append(current_min)

    def pop(self) -> int:
        self.min_stack.pop()
        return self.stack.pop()

    def get_min(self) -> int:
        return self.min_stack[-1]
```

## Key Takeaways
- Maintaining a parallel minimum stack achieves $O(1)$ retrieval of the current minimum element."""
                },
                {
                    "order": 2,
                    "title": "Monotonic Stacks & Next Greater Element",
                    "description": "Solve sliding window maximums, daily temperatures, and histogram rectangle areas in O(N).",
                    "duration_minutes": 45,
                    "content": """# Monotonic Stacks & Largest Rectangle in Histogram

A monotonic stack maintains elements in strictly increasing or decreasing order.

```python
def largest_rectangle_area(heights: list[int]) -> int:
    stack = []  # Indices of increasing heights
    max_area = 0
    heights.append(0)  # Sentinel to flush stack at end

    for i, h in enumerate(heights):
        while stack and heights[stack[-1]] > h:
            height = heights[stack.pop()]
            width = i if not stack else i - stack[-1] - 1
            max_area = max(max_area, height * width)
        stack.append(i)

    return max_area
```

## Key Takeaways
- Monotonic stacks reduce quadratic $O(N^2)$ brute-force nearest-element searches to single-pass $O(N)$ operations."""
                }
            ]
        },
        {
            "order": 4,
            "title": "Hash Tables & Collision Resolution",
            "description": "Hash functions, separate chaining, open addressing (linear, quadratic, double hashing), and Robin Hood hashing.",
            "chapters": [
                {
                    "order": 1,
                    "title": "Hash Table Architecture & Collision Strategies",
                    "description": "Implement a hash map with dynamic load factor resizing and polynomial rolling hashing.",
                    "duration_minutes": 45,
                    "content": """# Hash Table Architecture

Hash tables map keys to bucket indices using a deterministic hash function: $\\text{index} = \\text{hash}(key) \\pmod M$.

```python
class HashMapSeparateChaining:
    def __init__(self, capacity: int = 16):
        self.capacity = capacity
        self.size = 0
        self.buckets = [[] for _ in range(capacity)]
        self.load_factor_threshold = 0.75

    def _hash(self, key) -> int:
        return hash(key) % self.capacity

    def put(self, key, value):
        idx = self._hash(key)
        for i, (k, v) in enumerate(self.buckets[idx]):
            if k == key:
                self.buckets[idx][i] = (key, value)
                return
        self.buckets[idx].append((key, value))
        self.size += 1
        if self.size / self.capacity > self.load_factor_threshold:
            self._resize(self.capacity * 2)

    def get(self, key):
        idx = self._hash(key)
        for k, v in self.buckets[idx]:
            if k == key:
                return v
        raise KeyError(key)
```

## Key Takeaways
- With uniform hashing and a bounded load factor ($\alpha \le 0.75$), lookup, insertion, and deletion run in $O(1)$ average time."""
                }
            ]
        },
        {
            "order": 5,
            "title": "Trees & Balanced Binary Search Trees",
            "description": "Binary Trees, BST properties, AVL rotations, and Red-Black tree balancing invariants.",
            "chapters": [
                {
                    "order": 1,
                    "title": "Binary Tree Traversals (In-order, Pre-order, Post-order, Level-order)",
                    "description": "Recursive and iterative DFS traversals and BFS queue-based level traversals.",
                    "duration_minutes": 40,
                    "content": """# Binary Tree Traversals

```python
from collections import deque

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def level_order_traversal(root: TreeNode | None) -> list[list[int]]:
    if not root:
        return []
    result = []
    queue = deque([root])
    while queue:
        level_size = len(queue)
        current_level = []
        for _ in range(level_size):
            node = queue.popleft()
            current_level.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        result.append(current_level)
    return result
```

## Traversal Types
- **In-order (Left, Root, Right)**: Yields sorted order in a Binary Search Tree (BST).
- **Pre-order (Root, Left, Right)**: Useful for tree serialization and copying.
- **Post-order (Left, Right, Root)**: Useful for bottom-up computation (e.g. subtree sizes, tree deletion)."""
                },
                {
                    "order": 2,
                    "title": "Self-Balancing Trees: AVL Rotations & Red-Black Trees",
                    "description": "Maintain strict logarithmic height invariants with Left/Right single and double rotations.",
                    "duration_minutes": 50,
                    "content": """# AVL & Red-Black Balancing Invariants

Unbalanced BSTs can degenerate into $O(N)$ linked lists. Self-balancing trees guarantee $O(\log N)$ worst-case height.

## AVL Tree Balance Factor
$$\\text{Balance Factor}(node) = \\text{height}(left) - \\text{height}(right) \\in \\{-1, 0, 1\\}$$

```python
def rotate_left(z: TreeNode) -> TreeNode:
    y = z.right
    t2 = y.left
    y.left = z
    z.right = t2
    return y  # New subtree root
```

## Key Takeaways
- AVL trees are strictly balanced (faster lookups), making them ideal for read-heavy workloads.
- Red-Black trees allow slightly looser balancing (faster insertions/deletions), used in C++ `std::map` and Java `TreeMap`."""
                }
            ]
        },
        {
            "order": 6,
            "title": "Priority Queues & Binary Heaps",
            "description": "Min-heaps, Max-heaps, Floyd's O(N) heapify algorithm, and Top-K streaming elements.",
            "chapters": [
                {
                    "order": 1,
                    "title": "Binary Heap Implementation & Heapify",
                    "description": "Array-backed complete binary tree implementation with sift-up and sift-down.",
                    "duration_minutes": 45,
                    "content": """# Binary Heap Implementation

In an array-backed heap with 0-indexed nodes:
- Left Child: $2i + 1$
- Right Child: $2i + 2$
- Parent: $\\lfloor (i - 1) / 2 \\rfloor$

```python
class MinHeap:
    def __init__(self):
        self.heap = []

    def push(self, val: int):
        self.heap.append(val)
        self._sift_up(len(self.heap) - 1)

    def pop(self) -> int:
        if not self.heap:
            raise IndexError("pop from empty heap")
        min_val = self.heap[0]
        last_val = self.heap.pop()
        if self.heap:
            self.heap[0] = last_val
            self._sift_down(0)
        return min_val

    def _sift_up(self, idx: int):
        parent = (idx - 1) // 2
        if idx > 0 and self.heap[idx] < self.heap[parent]:
            self.heap[idx], self.heap[parent] = self.heap[parent], self.heap[idx]
            self._sift_up(parent)

    def _sift_down(self, idx: int):
        smallest = idx
        left = 2 * idx + 1
        right = 2 * idx + 2
        if left < len(self.heap) and self.heap[left] < self.heap[smallest]:
            smallest = left
        if right < len(self.heap) and self.heap[right] < self.heap[smallest]:
            smallest = right
        if smallest != idx:
            self.heap[idx], self.heap[smallest] = self.heap[smallest], self.heap[idx]
            self._sift_down(smallest)
```

## Key Takeaways
- Building a heap from an unsorted array takes $O(N)$ time using Floyd's bottom-up heapify algorithm, not $O(N \log N)$."""
                }
            ]
        },
        {
            "order": 7,
            "title": "Graph Algorithms & Network Flow",
            "description": "BFS, DFS, Kahn's Topological Sort, Dijkstra, Bellman-Ford, and Minimum Spanning Trees (Kruskal/Prim).",
            "chapters": [
                {
                    "order": 1,
                    "title": "Breadth-First Search & Dijkstra's Shortest Path",
                    "description": "Find single-source shortest paths on weighted and unweighted directed graphs.",
                    "duration_minutes": 50,
                    "content": """# Shortest Path Algorithms: BFS & Dijkstra

```python
import heapq

def dijkstra(graph: dict[int, list[tuple[int, int]]], start: int) -> dict[int, float]:
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    pq = [(0, start)]  # (distance, node)

    while pq:
        curr_dist, u = heapq.heappop(pq)

        if curr_dist > distances[u]:
            continue

        for v, weight in graph[u]:
            new_dist = curr_dist + weight
            if new_dist < distances[v]:
                distances[v] = new_dist
                heapq.heappush(pq, (new_dist, v))

    return distances
```

## Complexity Analysis
- Dijkstra with min-heap runs in $O((V + E) \log V)$ time.
- Requires non-negative edge weights; use Bellman-Ford ($O(V \cdot E)$) for negative edge weights."""
                },
                {
                    "order": 2,
                    "title": "Topological Sort & Cycle Detection in Directed Graphs",
                    "description": "Resolve dependency graphs using Kahn's in-degree algorithm and Tarjan's DFS.",
                    "duration_minutes": 40,
                    "content": """# Topological Sorting (Kahn's Algorithm)

Topological ordering arranges vertices linearly such that for every directed edge $u \to v$, $u$ comes before $v$.

```python
from collections import deque

def topological_sort(num_courses: int, prerequisites: list[list[int]]) -> list[int]:
    adj = {i: [] for i in range(num_courses)}
    in_degree = [0] * num_courses

    for dest, src in prerequisites:
        adj[src].append(dest)
        in_degree[dest] += 1

    queue = deque([i for i in range(num_courses) if in_degree[i] == 0])
    order = []

    while queue:
        u = queue.popleft()
        order.append(u)
        for v in adj[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                queue.append(v)

    return order if len(order) == num_courses else []  # Empty if cycle exists!
```

## Key Takeaways
- If the final output length is less than $V$, the graph contains a directed cycle (deadlock dependency)."""
                }
            ]
        },
        {
            "order": 8,
            "title": "Divide & Conquer, Sorting & Binary Search",
            "description": "Merge Sort, Quick Sort (3-way partitioning), and Binary Search on answer spaces.",
            "chapters": [
                {
                    "order": 1,
                    "title": "QuickSort, MergeSort & Sorting Invariants",
                    "description": "Analyze stability, in-place behavior, worst-case pivot degradation, and IntroSort.",
                    "duration_minutes": 45,
                    "content": """# Sorting Algorithms & Partitioning

```python
def quicksort_3way(arr: list[int], low: int, high: int):
    if low >= high:
        return
    # Dutch National Flag Partitioning for duplicate keys
    lt = low
    gt = high
    pivot = arr[low]
    i = low + 1

    while i <= gt:
        if arr[i] < pivot:
            arr[lt], arr[i] = arr[i], arr[lt]
            lt += 1
            i += 1
        elif arr[i] > pivot:
            arr[gt], arr[i] = arr[i], arr[gt]
            gt -= 1
        else:
            i += 1

    quicksort_3way(arr, low, lt - 1)
    quicksort_3way(arr, gt + 1, high)
```

## Sorting Properties Summary
- **MergeSort**: Stable, $O(N \log N)$ worst-case, requires $O(N)$ extra memory.
- **QuickSort**: Unstable, $O(N \log N)$ average, in-place $O(\log N)$ auxiliary call-stack."""
                },
                {
                    "order": 2,
                    "title": "Binary Search on Monotonic Answer Spaces",
                    "description": "Find optimal thresholds using predicate monotonic binary searching (Capacity to Ship Packages).",
                    "duration_minutes": 40,
                    "content": """# Binary Search on Monotonic Answer Spaces

Binary search applies not just to sorted arrays, but to any monotonic predicate function $f(x) \\to \\{\\text{False}, \\dots, \\text{False}, \\text{True}, \\dots, \\text{True}\\}$.

```python
def min_ship_capacity(weights: list[int], days: int) -> int:
    def can_ship(capacity: int) -> bool:
        day_count = 1
        current_load = 0
        for w in weights:
            if current_load + w > capacity:
                day_count += 1
                current_load = w
            else:
                current_load += w
        return day_count <= days

    left, right = max(weights), sum(weights)
    ans = right

    while left <= right:
        mid = (left + right) // 2
        if can_ship(mid):
            ans = mid
            right = mid - 1  # Try smaller capacity
        else:
            left = mid + 1

    return ans
```

## Key Takeaways
- Identify the search space $[\\text{min}, \\text{max}]$ and monotonic feasibility checker to solve complex optimization problems in $O(N \log(\\text{range}))$. """
                }
            ]
        },
        {
            "order": 9,
            "title": "Dynamic Programming Masterclass",
            "description": "Optimal substructure, overlapping subproblems, 0/1 Knapsack, LCS, LIS, and Bitmask DP.",
            "chapters": [
                {
                    "order": 1,
                    "title": "Top-Down Memoization vs Bottom-Up Tabulation",
                    "description": "Transform recursive tree traversals into linear iterative dynamic programming solutions.",
                    "duration_minutes": 50,
                    "content": """# Dynamic Programming Principles

Dynamic Programming solves problems with **Overlapping Subproblems** and **Optimal Substructure**.

## 0/1 Knapsack Problem
Given weights $w$ and values $v$, maximize value with maximum weight capacity $W$.

```python
def knapsack_01(weights: list[int], values: list[int], capacity: int) -> int:
    n = len(weights)
    # dp[w] stores max value achievable with capacity w
    dp = [0] * (capacity + 1)

    for i in range(n):
        wt, val = weights[i], values[i]
        # Iterate backwards to avoid using the same item multiple times
        for w in range(capacity, wt - 1, -1):
            dp[w] = max(dp[w], dp[w - wt] + val)

    return dp[capacity]
```

## Key Takeaways
- 1D space optimization reduces memory complexity from $O(N \cdot W)$ to $O(W)$ by traversing right-to-left."""
                },
                {
                    "order": 2,
                    "title": "Longest Common Subsequence & Edit Distance",
                    "description": "Multi-dimensional sequence alignment DP patterns with space optimization.",
                    "duration_minutes": 45,
                    "content": """# 2D Dynamic Programming: Edit Distance

Compute minimum operations (Insert, Delete, Replace) to convert string $S_1$ to $S_2$.

```python
def min_distance(word1: str, word2: str) -> int:
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(
                    dp[i - 1][j],    # Deletion
                    dp[i][j - 1],    # Insertion
                    dp[i - 1][j - 1] # Replacement
                )

    return dp[m][n]
```

## State Transitions
$$\\text{dp}[i][j] = \\begin{cases} \\text{dp}[i-1][j-1] & \\text{if } S_1[i] == S_2[j] \\\\ 1 + \\min(\\text{insert, delete, replace}) & \\text{otherwise} \\end{cases}$$"""
                }
            ]
        },
        {
            "order": 10,
            "title": "Advanced Structures: Tries, Disjoint Sets & Range Queries",
            "description": "Prefix Tries, Union-Find with path compression, Segment Trees, and Fenwick (BIT) trees.",
            "chapters": [
                {
                    "order": 1,
                    "title": "Trie (Prefix Tree) & Autocomplete Engines",
                    "description": "Implement efficient string dictionary lookups and prefix matching in O(L) time.",
                    "duration_minutes": 40,
                    "content": """# Trie (Prefix Tree)

A Trie stores strings character by character along edges, enabling $O(L)$ search where $L$ is string length.

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str):
        curr = self.root
        for char in word:
            if char not in curr.children:
                curr.children[char] = TrieNode()
            curr = curr.children[char]
        curr.is_end_of_word = True

    def starts_with(self, prefix: str) -> bool:
        curr = self.root
        for char in prefix:
            if char not in curr.children:
                return False
            curr = curr.children[char]
        return True
```

## Key Takeaways
- Tries provide instantaneous prefix querying without regex or scanning through large vocabularies."""
                },
                {
                    "order": 2,
                    "title": "Disjoint Set Union (Union-Find) with Path Compression",
                    "description": "Manage dynamic connectivity and cycle detection in nearly O(1) Ackermann time.",
                    "duration_minutes": 45,
                    "content": """# Disjoint Set Union (DSU / Union-Find)

Union-Find keeps track of partitioned elements into disjoint subsets.

```python
class UnionFind:
    def __init__(self, size: int):
        self.parent = list(range(size))
        self.rank = [1] * size
        self.num_components = size

    def find(self, i: int) -> int:
        if self.parent[i] == i:
            return i
        # Path compression
        self.parent[i] = self.find(self.parent[i])
        return self.parent[i]

    def union(self, i: int, j: int) -> bool:
        root_i = self.find(i)
        root_j = self.find(j)
        if root_i == root_j:
            return False  # Already connected

        # Union by rank
        if self.rank[root_i] < self.rank[root_j]:
            self.parent[root_i] = root_j
        elif self.rank[root_i] > self.rank[root_j]:
            self.parent[root_j] = root_i
        else:
            self.parent[root_j] = root_i
            self.rank[root_i] += 1

        self.num_components -= 1
        return True
```

## Key Takeaways
- With Path Compression and Union by Rank, $M$ operations take $O(M \cdot \alpha(N))$ time, where $\alpha$ is the Inverse Ackermann function ($\alpha(N) < 5$ for all practical universe sizes)."""
                }
            ]
        }
    ],
    "assessment": {
        "title": "Data Structures & Algorithms Certification Exam",
        "description": "Demonstrate your proficiency in asymptotic complexity, balanced trees, graph theory, and dynamic programming.",
        "passing_score": 70,
        "time_limit_minutes": 30,
        "questions": [
            {
                "question_text": "What is the time complexity of building a Binary Heap from an unsorted array of N elements using Floyd's algorithm?",
                "question_type": "single",
                "explanation": "Floyd's bottom-up heapify algorithm operates in O(N) time because the majority of nodes are near the bottom of the tree and move down very few levels.",
                "points": 20,
                "options": [
                    {"text": "O(N log N)", "is_correct": False},
                    {"text": "O(N)", "is_correct": True},
                    {"text": "O(N^2)", "is_correct": False},
                    {"text": "O(log N)", "is_correct": False}
                ]
            },
            {
                "question_text": "Which algorithm is optimal for finding single-source shortest paths on a directed graph with non-negative edge weights?",
                "question_type": "single",
                "explanation": "Dijkstra's algorithm with a min-priority queue achieves O((V + E) log V) time complexity on graphs with non-negative edge weights.",
                "points": 20,
                "options": [
                    {"text": "Dijkstra's Algorithm", "is_correct": True},
                    {"text": "Floyd-Warshall Algorithm", "is_correct": False},
                    {"text": "Breadth-First Search without weights", "is_correct": False},
                    {"text": "Kruskal's Algorithm", "is_correct": False}
                ]
            },
            {
                "question_text": "What does a cycle in a prerequisite dependency graph indicate when attempting Topological Sort?",
                "question_type": "single",
                "explanation": "Topological ordering is only possible on Directed Acyclic Graphs (DAGs); a directed cycle represents a circular dependency deadlock.",
                "points": 20,
                "options": [
                    {"text": "The graph contains no valid topological ordering (deadlock)", "is_correct": True},
                    {"text": "The sort completes in O(1) time", "is_correct": False},
                    {"text": "The graph is a Minimum Spanning Tree", "is_correct": False},
                    {"text": "All vertices have in-degree 0", "is_correct": False}
                ]
            },
            {
                "question_text": "In the 0/1 Knapsack dynamic programming problem, why do we iterate backwards over capacity when using a 1D DP array?",
                "question_type": "single",
                "explanation": "Iterating backwards ensures that values from the current item in the current iteration do not overwrite previous states and get used multiple times.",
                "points": 20,
                "options": [
                    {"text": "To prevent using the same item multiple times in the same step", "is_correct": True},
                    {"text": "To improve cache locality", "is_correct": False},
                    {"text": "Because Knapsack is an unbounded problem", "is_correct": False},
                    {"text": "To sort elements in ascending order", "is_correct": False}
                ]
            },
            {
                "question_text": "What is the amortized time complexity per operation in a Disjoint Set Union (Union-Find) with Path Compression and Union by Rank?",
                "question_type": "single",
                "explanation": "With both optimizations, DSU runs in O(alpha(N)) where alpha is the Inverse Ackermann function, which is effectively O(1) constant time in practice.",
                "points": 20,
                "options": [
                    {"text": "O(1) / O(alpha(N)) nearly constant time", "is_correct": True},
                    {"text": "O(N)", "is_correct": False},
                    {"text": "O(N log N)", "is_correct": False},
                    {"text": "O(log^2 N)", "is_correct": False}
                ]
            }
        ]
    }
}
