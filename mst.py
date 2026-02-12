from typing import List, Tuple, Optional

Edge = Tuple[int, int, float]  # (u, v, w)

class DSU:
    __slots__ = ("p", "r", "count")

    def __init__(self, n: int):
        self.p = list(range(n))
        self.r = [0] * n
        self.count = n

    def find(self, x: int) -> int:
        p = self.p
        while p[x] != x:
            p[x] = p[p[x]]
            x = p[x]
        return x

    def union(self, a: int, b: int) -> bool:
        ra = self.find(a)
        rb = self.find(b)
        if ra == rb:
            return False
        if self.r[ra] < self.r[rb]:
            ra, rb = rb, ra
        self.p[rb] = ra
        if self.r[ra] == self.r[rb]:
            self.r[ra] += 1
        self.count -= 1
        return True

def kruskal_mst_weight(n: int, edges: List[Edge]) -> Optional[float]:
    """
    Returns total weight if graph is connected enough to build an MST,
    else returns None.
    """
    edges_sorted = sorted(edges, key=lambda e: e[2])
    dsu = DSU(n)
    total = 0.0
    picked = 0
    for u, v, w in edges_sorted:
        if dsu.union(u, v):
            total += w
            picked += 1
            if picked == n - 1:
                return total
    return None
