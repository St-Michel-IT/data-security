from math import gcd


def order_mod(a, N) -> int:
    """
    Compute the smallest `r > 0` such that `a^r ≡ 1 (mod N)`.

    :param a: Base integer.
    :type a: int
    :param N: Modulus integer.
    :type N: int
    :return: The smallest period `r`.
    :rtype: int
    :raises ValueError: If `gcd(a, N) != 1`.
    """
    x, r = 1, 0
    while True:
        r += 1
        x = (x * a) % N
        if x == 1:
            return r


def shor_step(N) -> tuple:
    """
    Perform a classical demonstration of Shor's algorithm number-theory step.

    - Pick a random-ish base `a`.
    - Find the period `r` of `a^x mod N`.
    - If `r` is even and `a^(r/2) ≠ -1 (mod N)`, return non-trivial factors.

    :param N: The integer to factorize.
    :type N: int
    :return: A tuple containing the base `a`, the period `r`, and the factors `(p, q)`.
             Returns `(None, None, None)` if no factors are found.
    :rtype: tuple
    """
    for a in range(2, min(N, 20)):
        if gcd(a, N) != 1:
            print("Lucky: we already found a non-trivial factor")
            return a, None, (gcd(a, N), N // gcd(a, N))
        r = order_mod(a, N)
        if r % 2 == 0:
            print("r is even")
            ar2 = pow(a, r // 2, N)
            if ar2 != N - 1:  # i.e., a^(r/2) ≠ -1 (mod N)
                p = gcd(ar2 - 1, N)
                q = gcd(ar2 + 1, N)
                if 1 < p < N:
                    return a, r, (p, N // p)
                if 1 < q < N:
                    return a, r, (q, N // q)
    return None, None, None  # failed for this N with our small search


def show_periodicity(a, N, upto=20) -> None:
    """
    Print the sequence `f(x) = a^x mod N` and highlight its repeating period.

    :param a: Base integer.
    :type a: int
    :param N: Modulus integer.
    :type N: int
    :param upto: Number of values to compute in the sequence.
    :type upto: int
    :return: None
    """
    vals = [pow(a, x, N) for x in range(upto)]
    r = order_mod(a, N) if gcd(a, N) == 1 else None
    print(f"f(x) = {a}^x mod {N}  (first {upto} values)")
    print(vals)
    if r:
        print(f"Period r = {r} since {a}^{r} ≡ 1 (mod {N})")


def is_prime(n: int) -> bool:
    """
    Check if a number is prime.

       :param n: The integer to check.
       :type n: int
       :return: True if n is prime, False otherwise.
    """
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


if __name__ == "__main__":
    # --- Demo with small semiprimes ---
    for N in [4157521]:  # 15=3*5, 21=3*7, 33=3*11
        a, r, factors = shor_step(N)
        print(f"N = {N}")
        if factors:
            print(f"Found base a = {a}")
            if r: print(f"Order (period) r = {r}")
            print(f"Non-trivial factors of {N}: {factors[0]} × {factors[1]}")
            # Check bot factors are prime numbers
            print("First factor is prime:", is_prime(factors[0]))
            print("Second factor is prime:", is_prime(factors[1]))
            # Show the periodicity for intuition
            show_periodicity(a, N, upto=100)
        else:
            print("No factors found with this small search (try different N or expand search).")

        print("\n")

    # Print the the biggest prime number inferior 2**12
    print("The biggest prime number inferior 2**12 is:", max(i for i in range(2 ** 11) if is_prime(i)))
