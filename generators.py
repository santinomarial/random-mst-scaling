import math
import random
from typing import List, Tuple, Dict

Edge = Tuple[int, int, float]

def gen_edges_dim0_sparse(n: int, t: float, rng: random.Random) -> List[Edge]:
    """
    Complete graph with i.i.d. U[0,1] weights, but we keep only edges with weight <= t.
    Equivalent: include each pair with prob p=t, and assign weight uniform in [0,t].
    We generate edges in expected O(m) time using geometric skipping for Bernoulli(p).
    """
    if t <= 0.0:
        return []
    p = min(max(t, 0.0), 1.0)
    log_q = math.log(1.0 - p)  # negative

    edges: List[Edge] = []
    for i in range(n - 1):
        j = i + 1
        while j < n:
            # geometric skip: number of failures before next success
            u = rng.random()
            skip = int(math.floor(math.log(u) / log_q))  # >= 0
            j += skip
            if j < n:
                w = rng.random() * t
                edges.append((i, j, w))
                j += 1
    return edges

def gen_edges_dim1_hypercube(n: int, rng: random.Random) -> List[Edge]:
    """
    Graph on vertices 0..n-1 with edges (a,b) iff |a-b| is a power of 2.
    Undirected: we add each edge once with a < b.
    Weight ~ U[0,1].
    """
    edges: List[Edge] = []
    max_pow = int(math.floor(math.log2(max(n - 1, 1))))
    for a in range(n):
        for k in range(max_pow + 1):
            step = 1 << k
            b = a + step
            if b < n:
                edges.append((a, b, rng.random()))
    return edges

def gen_edges_euclid_sparse(n: int, dim: int, r: float, rng: random.Random) -> List[Edge]:
    """
    Points uniform in [0,1]^dim, complete graph with weights as Euclidean distance.
    We keep only edges with distance <= r using grid bucketing with cell size r.
    """
    pts = [[rng.random() for _ in range(dim)] for _ in range(n)]
    if r <= 0.0:
        return []

    cell = r
    # Map from integer cell coords to list of point indices
    buckets: Dict[Tuple[int, ...], List[int]] = {}

    def cell_id(p):
        return tuple(int(p[d] // cell) for d in range(dim))

    for i, p in enumerate(pts):
        cid = cell_id(p)
        buckets.setdefault(cid, []).append(i)

    # Neighboring cells: all offsets in {-1,0,1}^dim
    offsets = []
    def gen_offsets(curr):
        if len(curr) == dim:
            offsets.append(tuple(curr))
            return
        for v in (-1, 0, 1):
            curr.append(v)
            gen_offsets(curr)
            curr.pop()
    gen_offsets([])

    edges: List[Edge] = []
    for cid, idxs in buckets.items():
        for off in offsets:
            nid = tuple(cid[d] + off[d] for d in range(dim))
            if nid not in buckets:
                continue
            js = buckets[nid]
            # To avoid double counting, only generate edges (i,j) with i < j
            for i in idxs:
                for j in js:
                    if j <= i:
                        continue
                    # compute distance
                    dist2 = 0.0
                    pi = pts[i]
                    pj = pts[j]
                    for d in range(dim):
                        diff = pi[d] - pj[d]
                        dist2 += diff * diff
                    if dist2 <= r * r:
                        edges.append((i, j, math.sqrt(dist2)))
    return edges
