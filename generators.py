from __future__ import annotations

import itertools
import math

import numpy as np
from numpy.random import Generator

Edge = tuple[float, int, int]  # (weight, u, v)


def gen_edges_dim0_sparse(n: int, t: float, rng: Generator) -> list[Edge]:
    """
    Complete graph with i.i.d. U[0,1] weights; keep only edges with weight <= t.
    Inclusion probability equals t; kept weights are U[0, t].
    Allocates all n*(n-1)/2 weights at once, then masks.
    """
    if t <= 0.0 or n < 2:
        return []
    t = min(t, 1.0)
    rows, cols = np.triu_indices(n, k=1)   # one allocation: all pairs
    weights = rng.random(len(rows))         # one allocation: all weights
    mask = weights <= t
    w_m = weights[mask]
    r_m = rows[mask]
    c_m = cols[mask]
    return [(float(w), int(u), int(v)) for w, u, v in zip(w_m, r_m, c_m)]


def gen_edges_dim1_hypercube(n: int, rng: Generator) -> list[Edge]:
    """
    Edges (a, b) where |a - b| is a power of 2 and a < b. Weights i.i.d. U[0,1].
    """
    if n < 2:
        return []
    max_pow = int(math.floor(math.log2(n - 1)))
    pairs = [
        (a, a + (1 << k))
        for a in range(n)
        for k in range(max_pow + 1)
        if a + (1 << k) < n
    ]
    weights = rng.random(len(pairs))  # one allocation
    return [(float(w), a, b) for w, (a, b) in zip(weights, pairs)]


def gen_edges_euclid_sparse(n: int, dim: int, r: float, rng: Generator) -> list[Edge]:
    """
    n points uniform in [0,1]^dim; keep edges whose Euclidean distance is <= r.
    Uses grid bucketing (cell size r) to avoid checking all O(n^2) pairs.
    """
    if r <= 0.0 or n < 2:
        return []
    pts: np.ndarray = rng.random((n, dim))  # one allocation: all points

    cell_coords = (pts // r).astype(np.int32)
    buckets: dict[tuple[int, ...], list[int]] = {}
    for i in range(n):
        cid = tuple(cell_coords[i].tolist())
        buckets.setdefault(cid, []).append(i)

    offsets = list(itertools.product((-1, 0, 1), repeat=dim))
    r_sq = r * r

    edges: list[Edge] = []
    for cid, idxs in buckets.items():
        for off in offsets:
            nid = tuple(c + o for c, o in zip(cid, off))
            if nid not in buckets:
                continue
            js = buckets[nid]
            for i in idxs:
                js_gt = [j for j in js if j > i]
                if not js_gt:
                    continue
                diff = pts[i] - pts[js_gt]          # (k, dim) — vectorized
                dist_sq = (diff * diff).sum(axis=1)  # (k,)
                for idx, j in enumerate(js_gt):
                    if dist_sq[idx] <= r_sq:
                        edges.append((float(dist_sq[idx] ** 0.5), i, j))
    return edges
