"""
Functions related to finding primes. This file does not contain examples. It just contains utility functions related to primality
that are used by iterable_example.py in the iterables directory.
"""
import math


def find_primes(n):
    """
    Find and return all primes less than n.
    :param n: an integer.
    :return: a list of primes.
    """
    return [i for i in range(n) if is_prime(i)]


def is_prime(x):
    """
    Return True if x is prime, else False
    :param x: an integer to test for primality.
    :return: True if x is prime, else False.

    PROGRAMMER's NOTE:
    A number is prime if it has no divisors except 1 and itself.
    We only need to check the numbers between 2 and sqrt(x) inclusive as
    candidate divisors. If nothing less than sqrt(x) divides x, then the only
    divisors of x must be greater than sqrt(x). But if m and n are both greater than sqrt(x),
    then their product must exceed x.
    """
    return (x >= 2) and not any(is_divisor(i, x) for i in range(2, int(math.sqrt(x)) + 1))


def is_divisor(i, x):
    """
    :return: true if i is a divisor of x, else False
    :param i: an integer
    :param x: an integer
    """
    return x % i == 0


# =========================== Testing
def test():
    result = find_primes(10)
    if result == [2, 3, 5, 7]:
        print("Test passed")
    else:
        print("Test FAILED")


if __name__ == '__main__':
    test()
