"""
This file contains examples that illustrate iterators and iterable in python.

An iterator has a __next__() method that returns the next element in its sequence.

An iterable has a __iter__() method that returns an iterator suitable for iterating over the members of its collection.

Neither of the above methods is called in practice by application code. They are only called by the python interpreter's
internals. (In general, any method with double underscores on either side, e.g. __next__(), __init__(), etc., is only to be used by
python's internals, or by metaprogramming code that you might want to write.)

Instead, application code invokes them implicitly using python's "for" language construct. When you do:

    for x in y:
        do_something(x)

python expects y to be an iterable object, and compile the above code in such a way that y's __iter__() method is called to
yield an iterator whose __next__() method is then called to yield its successive elements. The python for loop also takes care
of automatically handling the StopIteration exception that is raised when the iteration is done.

You don't need to use "for" to access iterables, although this is the most common way. You can explicitly turn an iterable y into
an iterator by calling iter(y), which returns an iterable for y. You can also explicitly as an iterator it for its next element
by doing next(it). Both of these are acceptable application-level calls.
"""

from examples.primes.prime_utils import is_prime

# This is the fundamental way to create an iterable in python. Any object that responds to the __iter__() message is an iterable.
# This is also the fundamental way to create an iterator in python. Any object that responds to the __next_() message, raising a
# StopIteration exception when done, is an iterator. This class defines both messages, which means its instances are both iterables
# and iterators. This is a very typical way to do things.
#    That said, the "fundamental" way to create iterators is not used much. Instead, the generator method, illustrated
# farther below in this file, is usually clearer and easier.
class PrimesInRange(object):
    """
    Represents the sequence of primes between integers start (inclusive) and finish (exclusive).
    Instances of this class are iterables, which means they respond to the standard python interface protocol for iteration.
    """
    def __init__(self, start = 2, finish = None):
        """
        :param start: the lower bound (inclusive) for the sequence of primes to represent.
        :param finish: The upper bound (exclusive) for the sequence of primes to represent.
        """
        self.start = start
        self.finish = finish
        self.next_to_test = start # This member variable keeps track of the next integer we will test for primality.

    def __iter__(self):
        """
        All iterables in python must define this method. An iterable is an object that knows how to return an iterator version of itself.
        For example, a list is not an iterator, but it knows how to turn itself into an iterator. Since instances of this class
        are also iterators, the __iter__() method just needs to return self.
        :return:
        """
        return self

    def __next__(self):
        """
        Return the next prime in the specified range, or raise a StopIteration exception if we've already returned the last prime in range.
        :return:
        """
        found_prime = None
        while self.next_to_test < self.finish:
            if is_prime(self.next_to_test):
                found_prime = self.next_to_test
            self.next_to_test += 1
            if found_prime:
                return found_prime
        raise StopIteration



# This is the generator method for creating an iterator. It exactly duplicates the implementation above.
def generate_primes_in_range(start, finish):
    """
    Return an iterator that returns each prime in the range of start (inclusive) to finish (exclusive).
    :param start: the lower bound (inclusive) for the sequence of primes to represent.
    :param finish: The upper bound (exclusive) for the sequence of primes to represent.
    """
    for x in range(start, finish):
        if is_prime(x):
            yield x


# This shows how to usefully combine both design types above. We create a class whose __iter__ method is defined using "yield", which
# makes it a generator
class PrimesInRange2(object):
    """
    Represents the sequence of primes between start (inclusive) and finish (exclusive).
    Instances of this class are iterables, which means they respond to the standard python interface protocol for iteration.
    """
    def __init__(self, start = 2, finish = None):
        """
        :param start: the lower bound (inclusive) for the sequence of primes to represent.
        :param finish: The upper bound (exclusive) for the sequence of primes to represent.
        """
        self.start = start
        self.finish = finish

    def __iter__(self):
        """
         Here we dutifully return an iterator over our primes. Note that we don't return self, which means that we are truly
         an iterable, but not an iterator. The iterator is what gets returned by this method.
        """
        for x in range(self.start, self.finish):
            if is_prime(x):
                yield x

# =============================================================================
#                           TESTING
# =============================================================================

def test1():
    for x in PrimesInRange(2,20):
        print(x)


def test2():
    for x in generate_primes_in_range(2,20):
        print(x)


def test3():
    for x in PrimesInRange2(2,20):
        print(x)

if __name__ == '__main__':
    test1()
    test2()
    test3()