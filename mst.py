from __future__ import annotations

Edge = tuple[float, int, int]  # (weight, u, v)


class DSU:
    __slots__ = ("_parent", "_rank", "n_components")

    def __init__(self, n: int) -> None:
        self._parent: list[int] = list(range(n))
        self._rank: list[int] = [0] * n
        self.n_components: int = n

    def find(self, x: int) -> int:
        parent = self._parent
        while parent[x] != x:
            parent[x] = parent[parent[x]]  # path halving
            x = parent[x]
        return x

    def union(self, a: int, b: int) -> bool:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self._rank[ra] < self._rank[rb]:
            ra, rb = rb, ra
        self._parent[rb] = ra
        if self._rank[ra] == self._rank[rb]:
            self._rank[ra] += 1
        self.n_components -= 1
        return True


def kruskal_mst_weight(n: int, edges: list[Edge]) -> float | None:
    """Return MST weight, or None if the graph is disconnected."""
    if n <= 1:
        return 0.0
    dsu = DSU(n)
    total = 0.0
    picked = 0
    for w, u, v in sorted(edges, key=lambda e: e[0]):
        if dsu.union(u, v):
            total += w
            picked += 1
            if picked == n - 1:
                return total
    return None
