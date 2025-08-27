from shor import is_prime

if __name__ == "__main__":
    N = 4157521

    for x in range(2, N):
        if N % x == 0:
            p = x
            q = N // x
            break

    if is_prime(p) and is_prime(q):
        print(f"Factors of {N} are {p} and {q} and both are prime.")
