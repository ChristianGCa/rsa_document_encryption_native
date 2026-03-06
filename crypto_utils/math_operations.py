import random


def mdc(a, b):
    while b != 0:
        a, b = b, a % b
    print(f"\nMDC calculado: {a}\n")
    return a


def modular_inverter(e, phi):
    """Calculate d (private key) such that (d * e) % phi == 1"""
    m0 = phi
    y = 0
    x = 1

    if phi == 1:
        return 0

    while e > 1:
        q = e // phi
        t = phi
        phi = e % phi
        e = t
        temp = y
        y = x - q * y
        x = temp

    if x < 0:
        x = x + m0

    print(f"\nValor de d calculado: {x}\n")
    return x


def miller_rabin(n, k=5):
    """
    Test whether a number n is prime.
    k: number of attempts (the higher k, the greater the certainty).
    """
    if n < 2:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False

    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)

        if x == 1 or x == n - 1:
            continue

        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False

    return True


def generate_prime(bits):
    while True:
        p = random.getrandbits(bits) | (1 << bits - 1) | 1
        if miller_rabin(p):
            print(f"\nPrimo gerado: {p}\n")
            return p
