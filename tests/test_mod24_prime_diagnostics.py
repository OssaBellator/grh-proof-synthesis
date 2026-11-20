import unittest
from math import gcd

from tools.mod24_prime_diagnostics import (
    EXPONENTS,
    mod24_value,
    ppset_exp,
    primitive_inducer,
    twisted_character,
    units,
)


class Mod24DiagnosticsTests(unittest.TestCase):
    def test_all_characters(self):
        residues = units(24)
        self.assertEqual(residues, (1, 5, 7, 11, 13, 17, 19, 23))
        self.assertEqual(len({tuple(mod24_value(e, n) for n in residues) for e in EXPONENTS}), 8)
        conductors = []
        for e in EXPONENTS:
            with self.subTest(exponents=e):
                for a in range(24):
                    for b in range(24):
                        self.assertEqual(mod24_value(e, a * b), mod24_value(e, a) * mod24_value(e, b))
                f, induced = primitive_inducer(24, lambda n: mod24_value(e, n))
                self.assertEqual(set(induced), set(units(f)))
                self.assertEqual(f, primitive_inducer(f, induced.__getitem__)[0])
                conductors.append(f)
        self.assertEqual(conductors, [1, 8, 4, 8, 3, 24, 12, 24])
        self.assertEqual(sorted(conductors), [1, 3, 4, 8, 8, 12, 24, 24])

    def test_primitive_twists_and_ind_relation(self):
        for q in (11, 19):
            level = 24 * q
            for e in EXPONENTS:
                with self.subTest(prime=q, exponents=e):
                    f, _ = primitive_inducer(24, lambda n: mod24_value(e, n))
                    value = twisted_character(e, q)
                    d, induced = primitive_inducer(level, value)
                    self.assertEqual(d, f * q)
                    self.assertEqual(set(induced), set(units(d)))
                    self.assertEqual(d, primitive_inducer(d, induced.__getitem__)[0])
                    for n in range(level):
                        legendre = 0 if n % q == 0 else (1 if pow(n, (q - 1) // 2, q) == 1 else -1)
                        self.assertEqual(value(n), mod24_value(e, n) * legendre)
                        if gcd(n, level) == 1:
                            self.assertEqual(induced[n % d], value(n))

    def test_coprimality_and_nonunit_controls(self):
        with self.assertRaisesRegex(ValueError, "coprime"):
            twisted_character((1, 0, 0), 3)
        # With q=3 the two signs cancel on every unit of the product level.
        def shared_factor_twist(n):
            return mod24_value((1, 0, 0), n) * (1 if n % 3 == 1 else -1)

        self.assertEqual(primitive_inducer(72, shared_factor_twist)[0], 1)
        value = twisted_character((0, 0, 0), 11)
        d, induced = primitive_inducer(264, value)
        self.assertEqual((value(2), induced[2 % d]), (0, -1))

    def test_prime_windows(self):
        self.assertEqual(ppset_exp(2), (3,))
        self.assertEqual(ppset_exp(3), (11, 19))
        self.assertEqual(ppset_exp(4), (11, 19, 43))
        self.assertEqual(ppset_exp(3, modulus=16), (19,))
        self.assertEqual(ppset_exp(0), ())
        self.assertEqual(len(ppset_exp(3)) // 4, 0)


if __name__ == "__main__":
    unittest.main()
