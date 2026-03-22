# randmst

```bash
python3 randmst.py <seed> <n> <trials> <dimension>
python3 randmst.py 42 4096 10 2
# 28.123456 4096 10 2
```

## Files

| File | Responsibility |
|------|----------------|
| `generators.py` | Edge-list construction for each graph model |
| `mst.py` | Kruskal's algorithm with Union-Find (path halving, union by rank) |
| `randmst.py` | CLI: seeds per-trial RNG, aggregates results, prints output |

## Graph models and MST scaling

| Dimension | Model | MST weight |
|-----------|-------|------------|
| 0 | Complete graph, i.i.d. U[0,1] weights | Θ(1) |
| 1 | Hypercube (edges span powers of 2) | Θ(n) |
| 2 | Euclidean, unit square | Θ(n^(1/2)) |
| 3 | Euclidean, unit cube | Θ(n^(2/3)) |
| 4 | Euclidean, unit hypercube | Θ(n^(3/4)) |

For Euclidean models: an MST has n−1 edges, typical nearest-neighbor distance scales as n^(−1/d), so total weight scales as n · n^(−1/d) = Θ(n^((d−1)/d)).

## Complexity

Kruskal's runs in O(m log m). The sparse generators keep m = O(n log n) for all models, giving O(n (log n)²) overall.

| Model | Edges | Runtime |
|-------|-------|---------|
| dim=0 (threshold-sampled complete) | O(n log n) | O(n (log n)²) |
| dim=1 (hypercube) | O(n log n) | O(n (log n)²) |
| dim≥2 (Euclidean, radius-pruned) | O(n log n) | O(n (log n)²) |

## Requirements

- Python 3.9+
- NumPy
