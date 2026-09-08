# -*- coding: utf-8 -*-
"""
Curriculum definition for Artificial Intelligence & Modern LLM Engineering.
Comprehensive 9-module curriculum covering AI search agents, deep learning foundations,
the Transformer architecture, LLM fine-tuning, RAG systems, AI agents, and alignment.
"""

AI_COURSE = {
    "title": "Artificial Intelligence & Modern LLM Engineering",
    "slug": "artificial-intelligence-modern-llm-engineering",
    "description": "Master AI agents, neural foundations, the Transformer architecture, LLM fine-tuning (LoRA), RAG pipelines, and autonomous agents.",
    "category": "ai-ml",
    "level": "advanced",
    "duration_weeks": 12,
    "thumbnail_gradient": "from-fuchsia-600 via-pink-700 to-rose-900",
    "is_featured": True,
    "modules": [
        {
            "order": 1,
            "title": "Intelligent Agents & Classical Heuristic Search",
            "description": "Agent environments, state space exploration, A* search, heuristic design, and Minimax game trees.",
            "chapters": [
                {
                    "order": 1,
                    "title": "A* Search Algorithm & Admissible Heuristics",
                    "description": "Implement optimal pathfinding with priority queues and admissible, consistent heuristics.",
                    "duration_minutes": 40,
                    "content": """# A* Search Algorithm & Heuristic Optimality

A* evaluates candidate path states by combining exact cost-so-far $g(n)$ and estimated heuristic cost-to-goal $h(n)$:
$$f(n) = g(n) + h(n)$$

```python
import heapq

def a_star_search(start, goal, get_neighbors, heuristic):
    # Priority Queue storing tuples of (f_score, current_node)
    open_set = []
    heapq.heappush(open_set, (0, start))
    
    g_score = {start: 0}
    came_from = {}

    while open_set:
        current_f, current = heapq.heappop(open_set)

        if current == goal:
            # Reconstruct optimal path
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            return path[::-1]

        for neighbor, cost in get_neighbors(current):
            tentative_g = g_score[current] + cost
            if tentative_g < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score = tentative_g + heuristic(neighbor, goal)
                heapq.heappush(open_set, (f_score, neighbor))

    return None  # No path exists
```

## Key Invariants
- **Admissibility**: A heuristic $h(n)$ is admissible if it never overestimates the true minimal cost to goal ($h(n) \le h^*(n)$).
- **Consistency (Monotonicity)**: $h(n) \le c(n, a, n') + h(n')$. Consistency guarantees that the first time a node is expanded, its optimal path is discovered."""
                },
                {
                    "order": 2,
                    "title": "Adversarial Search: Minimax & Alpha-Beta Pruning",
                    "description": "Game-playing AI engines with depth-limited evaluation and branch pruning.",
                    "duration_minutes": 45,
                    "content": """# Minimax & Alpha-Beta Pruning

Alpha-Beta pruning eliminates evaluation of branches that cannot influence the final minimax decision.

```python
def alpha_beta(state, depth: int, alpha: float, beta: float, is_maximizing: bool) -> float:
    if depth == 0 or state.is_terminal():
        return state.evaluate_utility()

    if is_maximizing:
        max_eval = float('-inf')
        for child in state.get_legal_moves():
            eval_score = alpha_beta(child, depth - 1, alpha, beta, False)
            max_eval = max(max_eval, eval_score)
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break  # Beta cutoff / branch pruning
        return max_eval
    else:
        min_eval = float('inf')
        for child in state.get_legal_moves():
            eval_score = alpha_beta(child, depth - 1, alpha, beta, True)
            min_eval = min(min_eval, eval_score)
            beta = min(beta, eval_score)
            if beta <= alpha:
                break  # Alpha cutoff / branch pruning
        return min_eval
```

## Efficiency Gain
Alpha-Beta reduces the effective branching factor from $b^d$ to $b^{d/2}$ in best-case move ordering, doubling the search horizon."""
                }
            ]
        },
        {
            "order": 2,
            "title": "Deep Learning Foundations for AI",
            "description": "Feedforward neural networks, computational graphs, Backpropagation with autograd, and AdamW optimization.",
            "chapters": [
                {
                    "order": 1,
                    "title": "Backpropagation & Computational Graphs",
                    "description": "Derive matrix calculus gradients, chain rule across layers, and custom autograd engines.",
                    "duration_minutes": 50,
                    "content": """# Backpropagation & Computational Graphs

Backpropagation computes partial derivatives of the loss function $\mathcal{L}$ with respect to all network weights $\mathbf{W}$ using the multivariate chain rule.

```python
import torch
import torch.nn as nn

class MultiLayerPerceptron(nn.Module):
    def __init__(self, input_dim: int, hidden_dim: int, output_dim: int):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.LayerNorm(hidden_dim),
            nn.GELU(),
            nn.Linear(hidden_dim, output_dim)
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x)

# Forward & Backward pass
model = MultiLayerPerceptron(128, 256, 10)
x = torch.randn(32, 128)
labels = torch.randint(0, 10, (32,))

criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3, weight_decay=1e-2)

optimizer.zero_grad()
outputs = model(x)
loss = criterion(outputs, labels)
loss.backward()  # Automatic differentiation computes gradients
optimizer.step()
```

## Key Takeaways
- LayerNorm and GELU activations stabilize gradient propagation compared to classical Sigmoid/ReLU."""
                }
            ]
        },
        {
            "order": 3,
            "title": "The Transformer Architecture Demystified",
            "description": "Scaled Dot-Product Attention, Multi-Head Attention, Rotary Positional Embeddings (RoPE), and KV Caching.",
            "chapters": [
                {
                    "order": 1,
                    "title": "Self-Attention Mechanism & FlashAttention",
                    "description": "Implement scaled dot-product attention from scratch with Q, K, V projections and causal masking.",
                    "duration_minutes": 55,
                    "content": """# Scaled Dot-Product Attention

The core attention operation computes compatibility scores between Query and Key vectors to weight Value vectors:
$$\\text{Attention}(Q, K, V) = \\text{softmax}\\left(\\frac{QK^T}{\\sqrt{d_k}} + M\\right)V$$

```python
import torch
import torch.nn as nn
import math

class ScaledDotProductAttention(nn.Module):
    def __init__(self, d_k: int):
        super().__init__()
        self.scale = 1.0 / math.sqrt(d_k)

    def forward(self, q: torch.Tensor, k: torch.Tensor, v: torch.Tensor, mask: torch.Tensor | None = None) -> torch.Tensor:
        # q, k, v: [Batch, Heads, Seq_len, d_k]
        scores = torch.matmul(q, k.transpose(-2, -1)) * self.scale

        if mask is not None:
            # Mask out future tokens for autoregressive causal generation
            scores = scores.masked_fill(mask == 0, -1e9)

        attn_weights = torch.softmax(scores, dim=-1)
        output = torch.matmul(attn_weights, v)
        return output
```

## Key Takeaways
- Causal masking sets upper-triangular attention logits to $-\\infty$, preventing tokens from attending to future context."""
                },
                {
                    "order": 2,
                    "title": "Multi-Head Attention & Rotary Embeddings (RoPE)",
                    "description": "Implement Multi-Query Attention (MQA), Grouped-Query Attention (GQA), and RoPE rotations.",
                    "duration_minutes": 50,
                    "content": """# Multi-Head Attention & KV Caching

Multi-Head Attention projects representations into multiple subspaces, allowing models to attend to different relational aspects simultaneously.

## KV-Cache for Autoregressive Decoding
During text generation, past Key and Value tensors are cached in GPU memory so each new token only requires computing $Q_{\\text{new}}$ against cached $K_{\\le t}, V_{\\le t}$, reducing per-token generation complexity from $O(T^2)$ to $O(T)$.

## Key Modern Innovations
- **Grouped-Query Attention (GQA)**: Shares single Key/Value heads across multiple Query heads (used in LLaMA 3 / Mistral) to reduce KV-cache memory bandwidth."""
                }
            ]
        },
        {
            "order": 4,
            "title": "LLM Pretraining, Fine-Tuning & Quantization",
            "description": "Autoregressive causal language modeling, Instruction Tuning, LoRA, QLoRA (4-bit), and DeepSpeed ZeRO.",
            "chapters": [
                {
                    "order": 1,
                    "title": "Parameter-Efficient Fine-Tuning with LoRA & QLoRA",
                    "description": "Decompose weight update matrices with low-rank adapters and NF4 quantization.",
                    "duration_minutes": 50,
                    "content": """# LoRA: Low-Rank Adaptation

LoRA freezes base weights $W_0 \\in \\mathbb{R}^{d \\times k}$ and injects trainable rank decomposition matrices:
$$W = W_0 + \\Delta W = W_0 + \\frac{\\alpha}{r} (B \\cdot A)$$
where $A \\in \\mathbb{R}^{r \\times k}$ and $B \\in \\mathbb{R}^{d \\times r}$ with rank $r \\ll \\min(d, k)$.

```python
# Conceptual LoRA linear layer
class LoRALinear(nn.Module):
    def __init__(self, base_layer: nn.Linear, rank: int = 8, alpha: float = 16.0):
        super().__init__()
        self.base_layer = base_layer
        self.base_layer.weight.requires_grad = False  # Freeze base weights
        
        self.scaling = alpha / rank
        self.lora_A = nn.Parameter(torch.randn(rank, base_layer.in_features) * (1 / rank))
        self.lora_B = nn.Parameter(torch.zeros(base_layer.out_features, rank))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        base_out = self.base_layer(x)
        lora_out = (x @ self.lora_A.T @ self.lora_B.T) * self.scaling
        return base_out + lora_out
```

## Key Benefits
- Reduces trainable parameters by $>99\%$ while matching full fine-tuning performance."""
                }
            ]
        },
        {
            "order": 5,
            "title": "Retrieval-Augmented Generation (RAG) Systems",
            "description": "Vector databases, dense embedding models, hierarchical chunking, hybrid BM25 + dense search, and re-ranking.",
            "chapters": [
                {
                    "order": 1,
                    "title": "Production RAG Architecture & Vector Indexing",
                    "description": "Design resilient semantic retrieval systems with HNSW indexing and cross-encoder re-ranking.",
                    "duration_minutes": 50,
                    "content": """# Production RAG Pipeline Architecture

```python
def production_rag_pipeline(user_query: str, vector_store, reranker, llm) -> str:
    # 1. Generate dense query embedding
    query_embedding = embed_text(user_query)

    # 2. Retrieve top-20 candidate passages via HNSW Cosine Similarity
    candidates = vector_store.similarity_search(query_embedding, top_k=20)

    # 3. Cross-Encoder Re-Ranking to select top-5 high precision context chunks
    pairs = [[user_query, doc.page_content] for doc in candidates]
    scores = reranker.predict(pairs)
    ranked_docs = [doc for _, doc in sorted(zip(scores, candidates), reverse=True)][:5]

    # 4. Construct grounded prompt with citations
    context_str = "\\n---\\n".join([f"[{i+1}] {d.page_content}" for i, d in enumerate(ranked_docs)])
    prompt = f\"\"\"Answer the query using ONLY the provided context. If unsure, state you do not know.
Context:
{context_str}

Query: {user_query}
Answer:\"\"\"

    # 5. Synthesize answer with LLM
    return llm.generate(prompt)
```

## Key Takeaways
- Re-ranking with Cross-Encoders resolves lost-in-the-middle context degradation and improves precision."""
                }
            ]
        },
        {
            "order": 6,
            "title": "Autonomous AI Agents & Tool Calling",
            "description": "ReAct (Reasoning + Acting) loops, JSON schema function calling, Multi-agent orchestrations, and long-term memory.",
            "chapters": [
                {
                    "order": 1,
                    "title": "The ReAct Agent Framework & Function Calling",
                    "description": "Build autonomous agents capable of dynamic reasoning, API execution, and iterative reflection.",
                    "duration_minutes": 55,
                    "content": """# Autonomous ReAct Agent Loop

```python
import json

class ReActAgent:
    def __init__(self, llm, tools: dict):
        self.llm = llm
        self.tools = tools

    def run(self, goal: str, max_iterations: int = 5) -> str:
        trajectory = [f"Goal: {goal}"]

        for step in range(max_iterations):
            prompt = "\\n".join(trajectory) + "\\nThought: Next logical action\\nAction: tool_name[arg]"
            response = self.llm.generate(prompt)

            if "Final Answer:" in response:
                return response.split("Final Answer:")[1].strip()

            # Parse Action
            tool_name, tool_arg = self._parse_action(response)
            if tool_name in self.tools:
                observation = self.tools[tool_name](tool_arg)
                trajectory.append(f"Observation: {observation}")
            else:
                trajectory.append(f"Observation: Tool '{tool_name}' not found.")

        return "Goal could not be completed within step limit."
```

## Key Takeaways
- Interleaving Thought and Action steps reduces hallucination and allows agents to self-correct during API failures."""
                }
            ]
        },
        {
            "order": 7,
            "title": "AI Alignment, RLHF & Direct Preference Optimization",
            "description": "Reward modeling, PPO reinforcement learning, Direct Preference Optimization (DPO), and Constitutional AI.",
            "chapters": [
                {
                    "order": 1,
                    "title": "RLHF vs Direct Preference Optimization (DPO)",
                    "description": "Align model behaviors with human values using pair-wise preference loss without reward modeling.",
                    "duration_minutes": 45,
                    "content": """# Direct Preference Optimization (DPO)

DPO optimizes policy $\pi_\theta$ directly on preference pairs $(x, y_w, y_l)$ where $y_w$ is preferred over $y_l$:
$$\mathcal{L}_{\\text{DPO}}(\pi_\\theta; \\pi_\\text{ref}) = -\\mathbb{E}_{(x, y_w, y_l)} \\left[ \\log \\sigma \\left( \\beta \\log \\frac{\\pi_\\theta(y_w|x)}{\\pi_\\text{ref}(y_w|x)} - \\beta \\log \\frac{\\pi_\\theta(y_l|x)}{\\pi_\\text{ref}(y_l|x)} \\right) \\right]$$

## Key Benefits
- Bypasses the instability of training a separate reward model and reinforcement learning Actor-Critic loop."""
                }
            ]
        },
        {
            "order": 8,
            "title": "AI Evaluation, Safety & Guardrails",
            "description": "LLM-as-a-Judge, Ragas metrics (Faithfulness, Answer Relevance), Prompt Injection defense, and NeMo Guardrails.",
            "chapters": [
                {
                    "order": 1,
                    "title": "Automated LLM Evaluation & Ragas Metrics",
                    "description": "Quantify hallucination rates, semantic answer relevance, and context recall.",
                    "duration_minutes": 40,
                    "content": """# Automated LLM Evaluation Frameworks

## Key Ragas Metrics
1. **Faithfulness**: Proportion of claims in generated output supported by retrieved context.
2. **Answer Relevance**: Semantic alignment between generated answer and initial user prompt.
3. **Context Precision**: Signal-to-noise ratio of retrieved chunks relative to ground truth answer.

```python
# Faithfulness verification prompt template
FAITHFULNESS_JUDGE_PROMPT = \"\"\"Given the context and statement, decide if the statement is directly supported.
Context: {context}
Statement: {statement}
Answer [YES/NO]:\"\"\"
```"""
                }
            ]
        },
        {
            "order": 9,
            "title": "Production Deployment & High-Throughput Serving",
            "description": "vLLM, Continuous Batching, PagedAttention, Tensor Parallelism, and ONNX/TensorRT-LLM runtime optimization.",
            "chapters": [
                {
                    "order": 1,
                    "title": "PagedAttention & High-Throughput Serving with vLLM",
                    "description": "Eliminate GPU memory fragmentation and serve concurrent streams with continuous batching.",
                    "duration_minutes": 45,
                    "content": """# High-Throughput LLM Serving

## PagedAttention Architecture
Inspired by virtual memory paging in operating systems, PagedAttention partitions continuous KV caches into fixed-size physical memory blocks, reducing GPU VRAM waste from $60-80\%$ to under $4\%$.

## Continuous Batching
Unlike static request batching that waits for the longest sequence to terminate, continuous batching injects new incoming requests into available iteration slots dynamically."""
                }
            ]
        }
    ],
    "assessment": {
        "title": "Artificial Intelligence & LLM Engineering Certification Exam",
        "description": "Assess your understanding of attention mechanisms, low-rank adaptation, vector search, ReAct agents, and LLM evaluation.",
        "passing_score": 70,
        "time_limit_minutes": 25,
        "questions": [
            {
                "question_text": "What is the primary role of causal masking in autoregressive Transformer decoder language models?",
                "question_type": "single",
                "explanation": "Causal masking zeros out attention weights to subsequent future token positions to ensure predictions only depend on known preceding context.",
                "points": 20,
                "options": [
                    {"text": "To prevent tokens from attending to future positions during generation", "is_correct": True},
                    {"text": "To reduce parameter memory size by half", "is_correct": False},
                    {"text": "To compute gradients faster in backward passes", "is_correct": False},
                    {"text": "To encode absolute positional frequencies", "is_correct": False}
                ]
            },
            {
                "question_text": "How does LoRA (Low-Rank Adaptation) achieve parameter-efficient fine-tuning of large language models?",
                "question_type": "single",
                "explanation": "LoRA freezes original base weights and introduces low-rank decomposition matrices (B * A) with rank r << d to represent weight updates.",
                "points": 20,
                "options": [
                    {"text": "By freezing base weights and training small low-rank adapter matrices", "is_correct": True},
                    {"text": "By pruning 90% of attention heads", "is_correct": False},
                    {"text": "By removing the embedding layer", "is_correct": False},
                    {"text": "By quantizing the weights to 1-bit integers", "is_correct": False}
                ]
            },
            {
                "question_text": "In a production RAG system, why is a Cross-Encoder Re-Ranker applied after initial vector retrieval?",
                "question_type": "single",
                "explanation": "Bi-encoders compute vector embeddings independently for fast candidate retrieval, whereas cross-encoders perform full joint cross-attention between query and document to accurately score semantic relevance.",
                "points": 20,
                "options": [
                    {"text": "Cross-encoders perform joint attention between query and passage for higher precision scoring", "is_correct": True},
                    {"text": "Cross-encoders compress embeddings to save storage", "is_correct": False},
                    {"text": "To replace the LLM generator entirely", "is_correct": False},
                    {"text": "To convert markdown into HTML", "is_correct": False}
                ]
            },
            {
                "question_text": "What is the core execution loop of the ReAct (Reasoning + Acting) autonomous agent framework?",
                "question_type": "single",
                "explanation": "ReAct iteratively alternates between verbal reasoning traces (Thought), tool execution (Action), and environment feedback (Observation).",
                "points": 20,
                "options": [
                    {"text": "Interleaving Thought, Action, and Observation cycles", "is_correct": True},
                    {"text": "Pretraining on web text, then evaluating on test sets", "is_correct": False},
                    {"text": "Random exploration with uniform rewards", "is_correct": False},
                    {"text": "Compiling Python AST into bytecode", "is_correct": False}
                ]
            },
            {
                "question_text": "How does PagedAttention in vLLM reduce GPU VRAM waste during LLM serving?",
                "question_type": "single",
                "explanation": "PagedAttention treats KV cache memory like virtual memory pages, allocating non-contiguous physical blocks on demand rather than reserving large contiguous blocks per request.",
                "points": 20,
                "options": [
                    {"text": "Allocates KV caches in non-contiguous physical memory pages dynamically", "is_correct": True},
                    {"text": "Discards KV caches after every 5 tokens", "is_correct": False},
                    {"text": "Swaps weights to hard disk drives during generation", "is_correct": False},
                    {"text": "Restricts batch sizes to 1", "is_correct": False}
                ]
            }
        ]
    }
}
