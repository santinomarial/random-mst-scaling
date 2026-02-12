# Random MST Scaling Experiments

This project explores how the weight of a Minimum Spanning Tree (MST) grows as the number of vertices increases under different random graph models. The goal is to move beyond theory and validate asymptotic behavior through large-scale empirical experiments.

Rather than treating this as a toy implementation, the focus here is on **correctness**, **clean structure**, **reproducibility**, and **performance** across dense and sparse graph regimes.

## What This Project Studies

We evaluate five graph models:

- **Dimension 0** – Complete graph with independent random edge weights
- **Dimension 1** – Hypercube graph  
- **Dimension 2** – Random Euclidean graph in 2D
- **Dimension 3** – Random Euclidean graph in 3D
- **Dimension 4** – Random Euclidean graph in 4D

For Euclidean dimensions *d* ≥ 2, geometric arguments suggest the MST weight should grow as:

```
f(n) = Θ(n^((d-1)/d))
```

The experiments strongly confirm this prediction.

## Observed Scaling Behavior

Empirically, we observe:

| Dimension | Growth Rate |
|-----------|-------------|
| 0 | Θ(1) |
| 1 | Θ(n) |
| 2 | Θ(n^(1/2)) |
| 3 | Θ(n^(2/3)) |
| 4 | Θ(n^(3/4)) |

### Intuition

For Euclidean graphs, the scaling is straightforward:

1. Typical nearest-neighbor distance scales as *n*^(-1/*d*)
2. An MST contains *n* − 1 edges
3. Total weight therefore scales as *n* · *n*^(-1/*d*) = *n*^((*d*-1)/*d*)

The normalized experimental plots flatten toward constants, providing clear empirical evidence for the predicted growth rates.

## Implementation Details

The MST is computed using **Kruskal's algorithm** with a **Union-Find** data structure implementing:

- Path compression
- Union by rank

This ensures near-linear amortized time for cycle detection.

### Code Structure

The code is intentionally modular:

- `generators.py` — Graph construction logic for each model
- `mst.py` — Kruskal's algorithm and Union-Find implementation
- `randmst.py` — Command-line experiment runner

Graph generation and MST computation are separated to keep the system easy to reason about and extend.

## Runtime Characteristics

Let *n* = number of vertices and *m* = number of edges.

Kruskal's algorithm runs in **O(*m* log *m*)** time.

### Complexity by Graph Type

**Dense complete graphs:**
- *m* = Θ(*n*²)
- Runtime ≈ O(*n*² log *n*)

**Hypercube graphs:**
- *m* = Θ(*n* log *n*)
- Runtime ≈ O(*n* (log *n*)²)

The observed performance aligns with these theoretical bounds. Dense models are dominated by edge sorting, while sparse models scale significantly better.

## Running Experiments

### Usage

```bash
python3 randmst.py <seed> <n> <trials> <dimension>
```

### Example

```bash
python3 randmst.py 0 4096 10 2
```

This runs 10 trials on a 2D Euclidean graph with 4096 vertices, using seed 0.

### Output Format

```
average n trials dimension
```

Each run performs multiple independent trials using deterministic seeding to ensure **full reproducibility**.

## Why This Is Interesting

This project connects:

- **Asymptotic analysis** – theoretical growth laws
- **Geometric graph intuition** – why structure determines scaling
- **Efficient MST implementation** – practical algorithms at scale
- **Empirical validation** – experimental confirmation of predictions

It demonstrates how theoretical growth laws emerge naturally from structure — and how to design experiments that clearly expose those behaviors.

## Requirements

- Python 3.6+
- NumPy (for Euclidean graph generation)

## License

[Specify your license here]

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.
