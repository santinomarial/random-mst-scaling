import unittest

from numpy.random import default_rng

from mst import DSU, kruskal_mst_weight
from generators import (
    gen_edges_dim0_sparse,
    gen_edges_dim1_hypercube,
    gen_edges_euclid_sparse,
)


# ---------------------------------------------------------------------------
# DSU
# ---------------------------------------------------------------------------

class TestDSU(unittest.TestCase):

    def test_union_by_rank_and_path_compression(self):
        dsu = DSU(5)
        self.assertEqual(dsu.n_components, 5)
        dsu.union(0, 1)
        dsu.union(2, 3)
        dsu.union(1, 2)                       # merges {0,1} with {2,3}
        self.assertEqual(dsu.n_components, 2)
        self.assertEqual(dsu.find(0), dsu.find(3))
        self.assertNotEqual(dsu.find(0), dsu.find(4))

    def test_union_same_component_returns_false(self):
        dsu = DSU(3)
        dsu.union(0, 1)
        self.assertFalse(dsu.union(0, 1))
        self.assertEqual(dsu.n_components, 2)


# ---------------------------------------------------------------------------
# kruskal_mst_weight
# ---------------------------------------------------------------------------

class TestKruskal(unittest.TestCase):

    def test_triangle(self):
        # MST picks the two cheapest edges: 1.0 + 2.0 = 3.0
        edges = [(1.0, 0, 1), (2.0, 1, 2), (3.0, 0, 2)]
        self.assertAlmostEqual(kruskal_mst_weight(3, edges), 3.0)

    def test_four_node_graph(self):
        # Kruskal picks (0-1, 1.0), (1-2, 2.0), (0-3, 3.0) = 6.0
        edges = [
            (1.0, 0, 1), (4.0, 0, 2), (3.0, 0, 3),
            (2.0, 1, 2), (5.0, 1, 3), (6.0, 2, 3),
        ]
        self.assertAlmostEqual(kruskal_mst_weight(4, edges), 6.0)

    def test_n_equals_1(self):
        self.assertEqual(kruskal_mst_weight(1, []), 0.0)

    def test_linear_chain(self):
        # A path graph has exactly one spanning tree — itself.
        edges = [(0.1 * (i + 1), i, i + 1) for i in range(4)]  # 0.1+0.2+0.3+0.4
        self.assertAlmostEqual(kruskal_mst_weight(5, edges), 1.0)

    def test_disconnected_returns_none(self):
        edges = [(1.0, 0, 1), (1.0, 2, 3)]   # two components, n=4
        self.assertIsNone(kruskal_mst_weight(4, edges))

    def test_deterministic_and_non_mutating(self):
        edges = [(1.0, 0, 1), (2.0, 1, 2), (3.0, 0, 2)]
        result = kruskal_mst_weight(3, edges)
        self.assertEqual(kruskal_mst_weight(3, edges), result)
        self.assertEqual(edges, [(1.0, 0, 1), (2.0, 1, 2), (3.0, 0, 2)])


# ---------------------------------------------------------------------------
# generators — helpers
# ---------------------------------------------------------------------------

def _check_edge_format(tc: unittest.TestCase, edges: list, n: int) -> None:
    """Verify every edge is (float, int, int) with valid indices and weight in [0,1]."""
    for e in edges:
        tc.assertIsInstance(e, tuple)
        tc.assertEqual(len(e), 3)
        w, u, v = e
        tc.assertIsInstance(w, float)
        tc.assertIsInstance(u, int)
        tc.assertIsInstance(v, int)
        tc.assertGreaterEqual(w, 0.0)
        tc.assertLessEqual(w, 1.0)
        tc.assertGreaterEqual(u, 0)
        tc.assertLess(v, n)
        tc.assertLess(u, v)   # generators always emit u < v


# ---------------------------------------------------------------------------
# generators — return type and weight range (all five models)
# ---------------------------------------------------------------------------

class TestGeneratorFormat(unittest.TestCase):

    def test_dim0_format(self):
        _check_edge_format(self, gen_edges_dim0_sparse(6, 1.0, default_rng(0)), 6)

    def test_dim1_format(self):
        _check_edge_format(self, gen_edges_dim1_hypercube(6, default_rng(0)), 6)

    def test_dim2_format(self):
        # r=0.5 keeps distances ≤ 0.5, so all weights stay within [0,1].
        _check_edge_format(self, gen_edges_euclid_sparse(20, 2, 0.5, default_rng(0)), 20)

    def test_dim3_format(self):
        _check_edge_format(self, gen_edges_euclid_sparse(20, 3, 0.5, default_rng(0)), 20)

    def test_dim4_format(self):
        _check_edge_format(self, gen_edges_euclid_sparse(20, 4, 0.5, default_rng(0)), 20)


# ---------------------------------------------------------------------------
# generators — edge counts
# ---------------------------------------------------------------------------

class TestGeneratorEdgeCount(unittest.TestCase):

    def test_dim0_complete_graph(self):
        # t=1.0 includes every pair.
        n = 7
        edges = gen_edges_dim0_sparse(n, 1.0, default_rng(0))
        self.assertEqual(len(edges), n * (n - 1) // 2)

    def test_dim1_hypercube_n4(self):
        # n=4, max_pow=1: step-1 gives 3 pairs, step-2 gives 2 pairs = 5 total.
        edges = gen_edges_dim1_hypercube(4, default_rng(0))
        self.assertEqual(len(edges), 5)

    def test_dim2_all_pairs_large_r(self):
        # r=2.0 > sqrt(2): every pair in [0,1]^2 is within range.
        n = 6
        edges = gen_edges_euclid_sparse(n, 2, 2.0, default_rng(0))
        self.assertEqual(len(edges), n * (n - 1) // 2)

    def test_dim3_all_pairs_large_r(self):
        # r=2.0 > sqrt(3): every pair in [0,1]^3 is within range.
        n = 6
        edges = gen_edges_euclid_sparse(n, 3, 2.0, default_rng(0))
        self.assertEqual(len(edges), n * (n - 1) // 2)

    def test_dim4_all_pairs_large_r(self):
        # r=2.0 = sqrt(4): dist_sq <= r_sq covers all pairs in [0,1]^4.
        n = 6
        edges = gen_edges_euclid_sparse(n, 4, 2.0, default_rng(0))
        self.assertEqual(len(edges), n * (n - 1) // 2)


# ---------------------------------------------------------------------------
# generators — seeding
# ---------------------------------------------------------------------------

class TestGeneratorSeeding(unittest.TestCase):

    def test_dim0_same_seed_same_output(self):
        e1 = gen_edges_dim0_sparse(8, 1.0, default_rng(42))
        e2 = gen_edges_dim0_sparse(8, 1.0, default_rng(42))
        self.assertEqual(e1, e2)

    def test_dim1_same_seed_same_output(self):
        e1 = gen_edges_dim1_hypercube(8, default_rng(42))
        e2 = gen_edges_dim1_hypercube(8, default_rng(42))
        self.assertEqual(e1, e2)

    def test_dim2_same_seed_same_output(self):
        e1 = gen_edges_euclid_sparse(10, 2, 0.4, default_rng(42))
        e2 = gen_edges_euclid_sparse(10, 2, 0.4, default_rng(42))
        self.assertEqual(e1, e2)


if __name__ == "__main__":
    unittest.main()
