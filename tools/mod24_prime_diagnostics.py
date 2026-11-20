"""Exact finite character and PPset calculations for the Stage 1 audit."""

from fractions import Fraction
from itertools import product
from math import factorial, gcd, isqrt


EXPONENTS = tuple(product(range(2), repeat=3))


def is_prime(n):
    return n >= 2 and all(n % d for d in range(2, isqrt(n) + 1))


def units(level):
    return tuple(n for n in range(level) if gcd(n, level) == 1)


def mod24_value(exponents, n):
    if gcd(n, 24) != 1:
        return 0
    basis = (
        1 if n % 3 == 1 else -1,
        1 if n % 4 == 1 else -1,
        1 if n % 8 in (1, 7) else -1,
    )
    value = 1
    for sign, exponent in zip(basis, exponents, strict=True):
        value *= sign ** exponent
    return value


def primitive_inducer(level, character):
    """Return the least divisor with a well-defined character on its units."""
    if level < 1:
        raise ValueError("expected a positive level")
    values = {n: character(n) for n in units(level)}
    for divisor in range(1, level + 1):
        if level % divisor:
            continue
        reduced = {}
        for n, value in values.items():
            if reduced.setdefault(n % divisor, value) != value:
                break
        else:
            return divisor, reduced


def twisted_character(exponents, q):
    """Return the product at level 24q for an odd prime coprime to 24."""
    if gcd(q, 24) != 1 or not is_prime(q):
        raise ValueError("q must be a prime coprime to 24")
    squares = {n * n % q for n in range(1, q)}

    def value(n):
        residue = n % q
        jacobi = 0 if residue == 0 else (1 if residue in squares else -1)
        return mod24_value(exponents, n) * jacobi

    return value


def ppset_exp(z, modulus=8, residue=3):
    """Compute PPset(modulus, residue, exp(z)) for integers 0 through 4."""
    if not isinstance(z, int) or not 0 <= z <= 4 or modulus < 1:
        raise ValueError("expected integer 0 <= z <= 4 and positive modulus")
    lower = sum(Fraction(z ** k, factorial(k)) for k in range(17))
    # From the first omitted term on, consecutive term ratios are at most z/18.
    upper = lower + Fraction(z ** 17, factorial(17)) / (1 - Fraction(z, 18))
    cutoff = int(lower)
    if cutoff != int(upper):
        raise ArithmeticError("exponential enclosure straddles an integer")
    # floor(sqrt(U)) = isqrt(floor(U)) for U >= 0.
    return tuple(q for q in range(isqrt(cutoff) + 1, cutoff + 1)
                 if q % modulus == residue % modulus and is_prime(q))


def main():
    print("Exponents (mod 3, 4, 8) | conductor | twist at 11 | twist at 19")
    for exponents in EXPONENTS:
        f, _ = primitive_inducer(24, lambda n: mod24_value(exponents, n))
        twisted = [primitive_inducer(24 * q, twisted_character(exponents, q))[0]
                   for q in (11, 19)]
        print(f"{exponents} | {f} | {twisted[0]} | {twisted[1]}")
    for z in (3, 4):
        primes = ppset_exp(z)
        print(f"z={z}, candidates={list(primes)}, size={len(primes)}, "
              f"quarter-bound integer cap={len(primes) // 4} (conditional)")


if __name__ == "__main__":
    main()
