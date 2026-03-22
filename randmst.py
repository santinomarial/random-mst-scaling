#!/usr/bin/env python3
from __future__ import annotations

import argparse
import math

from numpy.random import Generator, default_rng

from mst import kruskal_mst_weight
from generators import (
    gen_edges_dim0_sparse,
    gen_edges_dim1_hypercube,
    gen_edges_euclid_sparse,
)

_VALID_DIMS = frozenset({0, 1, 2, 3, 4})
_TRIAL_SEED_STRIDE = 1_000_003


def run_trial(n: int, dim: int, rng: Generator) -> float:
    """Uses threshold-retry sparsification for dims 0, 2, 3, 4."""
    if dim == 0:
        for c in (2.0, 3.0, 4.0, 6.0, 8.0):
            t = min(c * math.log(max(n, 2)) / n, 1.0)
            w = kruskal_mst_weight(n, gen_edges_dim0_sparse(n, t, rng))
            if w is not None:
                return w
        raise RuntimeError(f"dim=0 graph disconnected after all thresholds (n={n})")

    if dim == 1:
        w = kruskal_mst_weight(n, gen_edges_dim1_hypercube(n, rng))
        if w is None:
            raise RuntimeError(f"dim=1 hypercube unexpectedly disconnected (n={n})")
        return w

    for c in (1.5, 2.0, 3.0, 4.0, 6.0):
        r = c * (math.log(max(n, 2)) / n) ** (1.0 / dim)
        w = kruskal_mst_weight(n, gen_edges_euclid_sparse(n, dim, r, rng))
        if w is not None:
            return w
    raise RuntimeError(f"dim={dim} graph disconnected after all radii (n={n})")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Average MST weight over independent random trials."
    )
    parser.add_argument("seed", type=int, help="Master RNG seed")
    parser.add_argument("n", type=int, help="Number of vertices")
    parser.add_argument("trials", type=int, help="Number of independent trials")
    parser.add_argument(
        "dimension",
        type=int,
        choices=sorted(_VALID_DIMS),
        metavar="dimension",
        help="Graph model: 0=complete, 1=hypercube, 2–4=Euclidean",
    )
    args = parser.parse_args()

    total = 0.0
    for t in range(args.trials):
        rng = default_rng(args.seed + t * _TRIAL_SEED_STRIDE)
        total += run_trial(args.n, args.dimension, rng)

    avg = total / args.trials
    print(f"{avg:.6f} {args.n} {args.trials} {args.dimension}")


if __name__ == "__main__":
    main()
