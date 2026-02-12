Perfect. Here’s a clean, strong, human-sounding README that renders properly on GitHub and reads like an intentional engineering project — not a class submission.

You can paste this directly into README.md.

Random MST Scaling Experiments

This project explores how the weight of a Minimum Spanning Tree (MST) grows as the number of vertices increases under different random graph models. The goal was to move beyond theory and validate asymptotic behavior through large-scale empirical experiments.

Rather than treating this as a toy implementation, the focus here is on correctness, clean structure, reproducibility, and performance across dense and sparse graph regimes.

What This Project Studies

We evaluate five graph models:

Dimension 0 – Complete graph with independent random edge weights

Dimension 1 – Hypercube graph

Dimension 2 – Random Euclidean graph in 2D

Dimension 3 – Random Euclidean graph in 3D

Dimension 4 – Random Euclidean graph in 4D

For Euclidean dimensions 
𝑑
≥
2
d≥2, geometric arguments suggest the MST weight should grow like:

f(n) = Θ(n<sup>(d − 1)/d</sup>)

The experiments strongly confirm this prediction.

Observed Scaling Behavior

Empirically:

Dimension 0: Θ(1)

Dimension 1: Θ(n)

Dimension 2: Θ(n<sup>1/2</sup>)

Dimension 3: Θ(n<sup>2/3</sup>)

Dimension 4: Θ(n<sup>3/4</sup>)

For Euclidean graphs, the intuition is straightforward:

Typical nearest-neighbor distance scales as n<sup>−1/d</sup>

An MST contains n − 1 edges

Total weight therefore scales as n · n<sup>−1/d</sup> = n<sup>(d − 1)/d</sup>

The normalized experimental plots flatten toward constants, providing clear empirical evidence for the predicted growth rates.

Implementation Details

The MST is computed using Kruskal’s algorithm with a Union–Find data structure implementing:

Path compression

Union by rank

This ensures near-linear amortized time for cycle detection.

The code is intentionally modular:

generators.py — graph construction logic for each model

mst.py — Kruskal’s algorithm and Union–Find

randmst.py — command-line experiment runner

Graph generation and MST computation are separated to keep the system easy to reason about and extend.

Runtime Characteristics

Let:

n = number of vertices

m = number of edges

Kruskal runs in:

O(m log m)

For dense complete graphs:

m = Θ(n²)
Runtime ≈ O(n² log n)

For hypercube graphs:

m = Θ(n log n)
Runtime ≈ O(n (log n)²)

The observed performance aligns with these theoretical bounds. Dense models are dominated by edge sorting, while sparse models scale significantly better.

Running Experiments
python3 randmst.py <seed> <n> <trials> <dimension>


Example:

python3 randmst.py 0 4096 10 2


Output format:

average n trials dimension


Each run performs multiple independent trials using deterministic seeding to ensure reproducibility.

Why This Is Interesting

This project connects:

Asymptotic analysis

Geometric graph intuition

Efficient MST implementation

Empirical validation at scale

It demonstrates how theoretical growth laws emerge naturally from structure — and how to design experiments that clearly expose those behaviors.