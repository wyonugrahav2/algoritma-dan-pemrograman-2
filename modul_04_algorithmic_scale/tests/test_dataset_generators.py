"""
test_dataset_generators.py
Memastikan generator data sintetis menghasilkan jumlah sampel N
yang akurat serta karakteristik data yang benar (terurut, terbalik, dsb).
"""

import unittest

from src.datasets.generators import (
    generate_random_integers,
    generate_sorted_integers,
    generate_reversed_integers,
    generate_random_string,
    generate_random_string_list,
    generate_key_value_pairs,
)
from src.datasets.data_cases import (
    build_best_case,
    build_average_case,
    build_worst_case,
    build_all_cases,
    CaseType,
)


class TestGenerators(unittest.TestCase):
    def test_random_integers_length(self):
        data = generate_random_integers(100)
        self.assertEqual(len(data), 100)

    def test_random_integers_zero(self):
        data = generate_random_integers(0)
        self.assertEqual(data, [])

    def test_random_integers_negative_raises(self):
        with self.assertRaises(ValueError):
            generate_random_integers(-5)

    def test_sorted_integers_is_sorted(self):
        data = generate_sorted_integers(500)
        self.assertEqual(data, sorted(data))
        self.assertEqual(len(data), 500)

    def test_reversed_integers_is_descending(self):
        data = generate_reversed_integers(500)
        self.assertEqual(data, sorted(data, reverse=True))
        self.assertEqual(len(data), 500)

    def test_random_string_length(self):
        s = generate_random_string(20)
        self.assertEqual(len(s), 20)

    def test_random_string_list_length(self):
        strings = generate_random_string_list(50, string_length=8)
        self.assertEqual(len(strings), 50)
        self.assertTrue(all(len(s) == 8 for s in strings))

    def test_key_value_pairs_length(self):
        pairs = generate_key_value_pairs(30)
        self.assertEqual(len(pairs), 30)

    def test_reproducibility_with_seed(self):
        a = generate_random_integers(100, seed=123)
        b = generate_random_integers(100, seed=123)
        self.assertEqual(a, b)


class TestDataCases(unittest.TestCase):
    def test_best_case_is_sorted(self):
        case = build_best_case(200)
        self.assertEqual(case.case_type, CaseType.BEST)
        self.assertEqual(case.data, sorted(case.data))
        self.assertEqual(case.n, 200)

    def test_worst_case_is_reversed(self):
        case = build_worst_case(200)
        self.assertEqual(case.case_type, CaseType.WORST)
        self.assertEqual(case.data, sorted(case.data, reverse=True))

    def test_average_case_length(self):
        case = build_average_case(150, seed=1)
        self.assertEqual(case.case_type, CaseType.AVERAGE)
        self.assertEqual(len(case.data), 150)

    def test_build_all_cases_returns_three(self):
        cases = build_all_cases(100, seed=1)
        self.assertEqual(len(cases), 3)
        types = {c.case_type for c in cases}
        self.assertEqual(types, {CaseType.BEST, CaseType.AVERAGE, CaseType.WORST})


if __name__ == "__main__":
    unittest.main()
