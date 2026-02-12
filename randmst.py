#!/usr/bin/env python3
import sys
import math
import random
from typing import List, Tuple

from mst import kruskal_mst_weight
from generators import (
    gen_edges_dim0_sparse,
    gen_edges_dim1_hypercube,
    gen_edges_euclid_sparse,
)

def run_trial(n: int, dim: int, rng: random.Random) -> float:
    """
    Returns MST total weight for one random instance.
    Uses sparsification for dim in {0,2,3,4}. Exact for dim=1.
    """
    if dim == 0:
        # Sparse Erdos-Renyi style generation with weights in [0, t]
        # We try increasing constants until the sparse graph is connected enough for MST.
        for c in (2.0, 3.0, 4.0, 6.0, 8.0):
            t = c * math.log(max(n, 2)) / n
            t = min(t, 1.0)
            edges = gen_edges_dim0_sparse(n, t, rng)
            w = kruskal_mst_weight(n, edges)
            if w is not None:
                return w
        # Fallback: if something went wrong, last attempt result (or raise)
        raise RuntimeError("Failed to build connected-enough sparse graph for dim=0")

    if dim == 1:
        edges = gen_edges_dim1_hypercube(n, rng)
        w = kruskal_mst_weight(n, edges)
        if w is None:
            raise RuntimeError("Hypercube graph unexpectedly disconnected.")
        return w

    if dim in (2, 3, 4):
        # Points in unit hypercube; keep edges within radius r.
        for c in (1.5, 2.0, 3.0, 4.0, 6.0):
            r = c * (math.log(max(n, 2)) / n) ** (1.0 / dim)
            edges = gen_edges_euclid_sparse(n, dim, r, rng)
            w = kruskal_mst_weight(n, edges)
            if w is not None:
                return w
        raise RuntimeError(f"Failed to build connected-enough sparse graph for dim={dim}")

    raise ValueError("dimension must be 0,1,2,3,4")

def main():
    # Recommended interface in the handout:
    # ./randmst 0 numpoints numtrials dimension
    # output: average numpoints numtrials dimension
    if len(sys.argv) != 5:
        print("usage: ./randmst 0 numpoints numtrials dimension", file=sys.stderr)
        sys.exit(2)

    _flag = int(sys.argv[1])
    n = int(sys.argv[2])
    trials = int(sys.argv[3])
    dim = int(sys.argv[4])

    # Independent randomness per trial: seed from system randomness
    base = random.SystemRandom().randrange(1 << 60)
    total = 0.0
    for t in range(trials):
        rng = random.Random(base + 1000003 * t)
        total += run_trial(n, dim, rng)

    avg = total / trials
    print(f"{avg:.10f} {n} {trials} {dim}")

if __name__ == "__main__":
    main()
