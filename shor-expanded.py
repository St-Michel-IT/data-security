import random
from math import gcd
from typing import Optional, Tuple, List


def order_mod(a: int, N: int, max_steps: Optional[int] = None) -> Optional[int]:
    """
    Compute the smallest `r > 0` such that `a^r ≡ 1 (mod N)`.

    :param a: Base integer.
    :type a: int
    :param N: Modulus integer.
    :type N: int
    :param max_steps: Maximum number of steps to avoid long loops. Defaults to `None`.
    :type max_steps: Optional[int]
    :return: The smallest period `r` or `None` if no period is found.
    :rtype: Optional[int]
    """
    if gcd(a, N) != 1:
        return None
    x: int = 1
    r: int = 0
    if max_steps is None:
        max_steps = 2 * N.bit_length() * N.bit_length()
    while r < max_steps:
        r += 1
        x = (x * a) % N
        if x == 1:
            return r
    return None


def shor_try_once(N: int, a: int) -> Optional[Tuple[int, int]]:
    """
    Attempt to find non-trivial factors of `N` using a single base `a`.

    :param N: The integer to factorize.
    :type N: int
    :param a: The base integer.
    :type a: int
    :return: A tuple of non-trivial factors `(p, q)` or `None` if no factors are found.
    :rtype: Optional[Tuple[int, int]]
    """
    g: int = gcd(a, N)
    if g != 1:
        return (g, N // g) if 1 < g < N else None
    r: Optional[int] = order_mod(a, N)
    if not r or r % 2 == 1:
        return None
    ar2: int = pow(a, r // 2, N)
    if ar2 == 1 or ar2 == N - 1:
        return None
    p: int = gcd(ar2 - 1, N)
    if 1 < p < N:
        return (p, N // p)
    q: int = gcd(ar2 + 1, N)
    if 1 < q < N:
        return (q, N // q)
    return None


def shor_expand(N: int, max_tries: int = 2000) -> Optional[Tuple[int, int]]:
    """
    Attempt to find non-trivial factors of `N` using multiple random bases.

    :param N: The integer to factorize.
    :type N: int
    :param max_tries: Maximum number of random bases to try. Defaults to 2000.
    :type max_tries: int
    :return: A tuple of non-trivial factors `(p, q)` or `None` if no factors are found.
    :rtype: Optional[Tuple[int, int]]
    """
    bases: List[int] = list(range(2, min(N - 1, 200))) + \
                       [random.randrange(2, N - 1) for _ in range(max_tries)]
    for a in bases:
        res: Optional[Tuple[int, int]] = shor_try_once(N, a)
        if res:
            return tuple(sorted(res))
    return None


def pollards_rho(n: int) -> int:
    """
    Perform Pollard's Rho algorithm to find a factor of `n`.

    :param n: The integer to factorize.
    :type n: int
    :return: A non-trivial factor of `n`.
    :rtype: int
    """
    if n % 2 == 0:
        return 2
    if n % 3 == 0:
        return 3
    while True:
        y: int = random.randrange(1, n - 1)
        c: int = random.randrange(1, n - 1)
        m: int = random.randrange(1, n - 1)
        g: int = 1
        r: int = 1
        q: int = 1
        while g == 1:
            x: int = y
            for _ in range(r):
                y = (y * y + c) % n
            k: int = 0
            while k < r and g == 1:
                ys: int = y
                for _ in range(min(m, r - k)):
                    y = (y * y + c) % n
                    q = (q * abs(x - y)) % n
                g = gcd(q, n)
                k += m
            r <<= 1
        if g == n:
            g = 1
            while g == 1:
                ys = (ys * ys + c) % n
                g = gcd(abs(x - ys), n)
        if g != n:
            return g


def is_probable_prime(n: int) -> bool:
    """
    Check if a number is a probable prime using trial division and Miller-Rabin.

    :param n: The integer to check.
    :type n: int
    :return: `True` if `n` is a probable prime, `False` otherwise.
    :rtype: bool
    """
    if n < 2:
        return False
    small: List[int] = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    for p in small:
        if n == p:
            return True
        if n % p == 0:
            return n == p
    d: int = n - 1
    s: int = 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in [2, 7, 61]:
        if a % n == 0:
            continue
        x: int = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = (x * x) % n
            if x == n - 1:
                break
        else:
            return False
    return True


def factor_full(n: int, use_shor: bool = True) -> List[int]:
    """
    Perform full factorization of `n` into its prime factors.

    :param n: The integer to factorize.
    :type n: int
    :param use_shor: Whether to use Shor's algorithm for factorization. Defaults to `True`.
    :type use_shor: bool
    :return: A sorted list of prime factors of `n`.
    :rtype: List[int]
    """
    if n == 1:
        return []
    if is_probable_prime(n):
        return [n]
    if use_shor:
        res: Optional[Tuple[int, int]] = shor_expand(n, max_tries=3000)
        if res:
            p, q = res
            return sorted(factor_full(p, use_shor=True) + factor_full(q, use_shor=True))
    d: int = pollards_rho(n)
    return sorted(factor_full(d, use_shor=True) + factor_full(n // d, use_shor=True))


if __name__ == "__main__":
    N: int = 4157521
    print("N bit length is:", int(N).bit_length())
    print("Expanded Shor attempt:", shor_expand(N, max_tries=5000))
    print("Full factorization    :", factor_full(N))