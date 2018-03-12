"""
This file explains iterables, iterators, and generators in python and contains
executable examples of the same. Execute the file via "python iterable_example.py" at the command-line
to watch the examples run.

========== ITERABLES AND ITERATORS ==========
OVERVIEW
An iterable represents a collection of items that is capable of being iterated over. Iteration occurs by assigning one element at a time
from the collection to a local variable using python's built-in "for x in y" language construct. The actual execution of
such an iteration is carried out by using an object called an iterator, which encapsulates the logic of a one-time loop over the
iterable's elements.

Lists, dicts, and numpy arrays are all iterables, because you can say "for x in my_list:" or "for x in my_dict:",
or "for x in my_array:", and python will establish a loop that automatically binds x to the successive elements of
these collections. Such functionality is not limited to built-in types.

Any class in python can become an iterable simply by defining an __iter__() method for the class. The __iter__() method is called
implicitly by the python interpreter when the interpreter sees a for-loop, and it expects the method to return an object
called an iterator, which is responsible for doing the actual work of returning the elements of the container. The iterator
does its job by defining a __next__() method, which returns successive elements from the collection each time it is called,
raising a StopIteration exception when there are no more elements to return.

Below is a simple example of an iterable and an illustration of its usage. Take a look at the code, and then we'll discuss how it works.
"""

class SimpleIterable(object):
    """
    A collection of the integers between 0 and num_elements exclusive. When iterated over,
    the elements are returned in descending order.
    """
    def __init__(self, num_elements):
        self.num_elements = num_elements

    # Notice that this method leaves the job of returning elements in descending order to the iterator object .
    def __iter__(self):
        return SimpleIterator(self.num_elements)


class SimpleIterator(object):
    """
    An iterator over the integers num_elements (exclusive) down to 0.
    """
    def __init__(self, num_elements):
        self.x = num_elements

    # This returns the next element in the container, keeping track of where we are in the iteration, and raises
    # a StopIteration exception when we're all done.
    def __next__(self):
        self.x -= 1
        if self.x < 0:
            raise StopIteration
        return self.x

print("Running SimpleIterator Example")
container = SimpleIterable(5)  # Create a collection of the integers 0 through 4 inclusive.

# Loop through the successive elements in the container in descending order.
for element in container:
    print(element)

"""
EXECUTION DETAILS
Let's go through the details of how the for-loop above works. When the python interpreter sees the expression "for element in container",
it automatically expects that container is an iterable. The object "container" is an instance of class SimpleIterable, and it 
is indeed an iterable, by virtue of defining an __iter__() method. *Any* class that defines an __iter__() method makes its instances 
iterables. This is an example of "duck typing". The type is determined not by inheriting from a particular class, but just by virtue of 
implementing a specified interface. In this case, the interface consists of a single method: the __iter__() method.

The python interpreter duly calls the iterable's __iter__() method and duly receives back an instance of SimpleIterator. Just as
container is an iterable by virtue of defining an __iter__() method, the SimpleIterator instance this method returns is an iterator
by virtue of defining a __next__() method, again by duck typing. The purpose of the __next__() method is to return successive elements
of the original container each time __next__() is called.

The python interpreter implements the for-loop by repeatedly calling the iterator's __next__() method and binding its returned values
to the variable "element". It expects the iterator to raise a StopIteration exception when it has returned the last element
of the container. Python arranges to automatically trap this exception and exits from the loop when it occurs.

SUMMARY
In sum, an iterable is a container that knows how to loop through its elements by returning an iterator to do the job. Python
establishes the interfaces that iterables and iterators must respect. Any object that defines an __iter__() method is an iterable. 
Any object that defines a __next__() method and raises a StopIteration exception is an iterator.

There are lots of ways the above protocols can go wrong. Here are some of them. If you write the expression "for x in my_obj:", but
my_obj does not define an __iter__() method, then this will crash with an error message saying that __iter__() is undefined for my_obj.
If the __iter__() method exists, but the object it returns does not have a __next__() method, then this will crash with an error
message saying that __next__() is not defined for the returned object. If the returned object never raises a StopIteration exception,
then the for-loop will never terminate, unless it contains an explicit return or break within its body. There are times when this
is exactly the desired behavior, i.e., when the iterable being looped over is intended to represent an infinite collection.

There is actually a preferable short-cut to explicitly creating an iterator class as we did above. That is illustrated below when
we talk about generators.

BUILTIN FUNCTIONS RELATED TO ITERABLES AND ITERATORS
There are some built-ins in python you should know about that relate to iterables and iterators, allowing you to deal with them
explicitly outside of the context of a for-loop. Even though 90% of the time you'll just invoke them implicitly via a for-loop, there are 
definitely times when it is desirable to have more control over the iteration, and this is the primary advantage
one gains by using iterators.

The iter() function calls the __iter__() method of an iterable and returns an iterator over the iterable. 
For example, "iter(my_list)" returns an iterator over the
elements of my_list. Similarly "iter(my_dict)" returns an iterator over the keys in my_dict. In like manner, the next() function 
invokes the __next__() method of an iterator. So, if my_iterator is an iterator, the pythonic way to call its next method explicitly is via
"next(my_iterator)". Also, if my_iterator is an iterator, you can turn it into a list by calling list() on it. Here is an example:
"""
print()
print()
print("Running examples illustrating builtin functions on iterators")
x = [1,3,5,7]
my_iterator = iter(x)
print(next(my_iterator))  # -> 1
print(next(my_iterator))  # -> 3
y = list(my_iterator)     # -> [5,7]
print(y)
try:
    next(my_iterator)         # -> raises StopIteration exception. my_iterator had all its elements exhausted when list() was called on it.
except StopIteration:
    print("my_iterator is now empty!")


"""
Note that if you decide to handle iterators yourself by calling next() explicitly, then you also have to handle the StopIteration 
exception yourself by sitting up the appropriate try/except block.

DIFFERENCE BETWEEN ITERABLES AND ITERATORS
It might seem as though iterables and iterators are too close together in purpose to require they be distinct kinds of objects. 
They seem like they're almost the same thing. Wouldn't it have been better if they actually *were* the same thing? In fact, you
can make them so that they *are* the same thing--which I will mentioned in a moment--but there is actually an important distinction 
between them that can be maintained *if you keep them distinct*: after an iterator has returned its last element, it is
empty and forever empty (under normal use cases). Successive calls to its __next__() method always raise a 
StopIteration exception. 

By contrast, the iterable from which it was derived still has all its elements if you have kept it distinct from the iterable. 
In this scenario, the iterable represents something that is *capable of being iterated over*, while
the iterator represents a single iteration through its elements. For example, consider the list x = [1,3,5]. Every time you do
"for e in x:..." python creates a *new* iterator to iterate over the list's elements, yet the iterable itself remains unchanged.

As mentioned, you needn't do things this way. You can merge the concepts of iterable and iterator simply by defining a class
whose __iter__() method returns self AND which also defines a __next__() method. Following the rule of duck typing, since such
a class defines both __iter__() and __next__(), it is both an iterable and an iterator. By returning "self" in response to __iter__(),
the iterable is telling the python interpreter to use this same object as its own iterator. Notice, though, when you do this, that 
the iterable loses its elements as it is iterated through and eventually becomes empty. This organization creates "one-shot" iterables
whose behavior is essentially just that of an iterator. There is nothing wrong with this organization; however, as you will see in a
section or two, you normally don't have to worry about the distinction between these two architectures, because generators offer a 
superior method of creating iterators.

ADVANTAGES OF ITERABLES
One of the important advantages of creating a custom iterable in preference to merely using a list is *lazy calculation*. 
In order to instantiate a list, the list must
calculate all its elements first and store them all in memory. If the list is a long one, this can be intensive in both time and space.
By contrast, an iterator only ever need allocate enough memory to calculate the __next__() element in the iteration, and it only
ever need expend enough computational effort to calculate that next element. It doesn't waste time calculating all the elements
at once. For example, in the SimpleIterable example above, suppose we had set num_elements to
a large number such as one billion. This doesn't allocate any more memory than if we set num_elements to a small number such as 5,
because the collection is represented abstractly and the iterator only ever calculates the next element from the previous element.
By contrast, representing a list of one billion elements would take a few gigabytes.

What if the collection we want to represent is infinite? Then it would be impossible to create a list containing all the elements.
There are use cases for this. For example, the number of primes is infinite. 
If you want to loop through all the primes while searching for the first one that satisfies some property, the most elegant way
to do this is just to create an iterable that represents all primes.

Another advantage of iterables is filtering. The set of primes can be thought of as what you get when you filter out from the 
set of integers everything that is not prime. By wrapping up the filtering logic in an iterable, client code can ignore all the logic that
goes into doing the filtering and concentrate on just the elements (primes) that pass the filter. This makes client code simpler. You
can see this clarity illustrated in the examples below.

Related to filtering is data re-organization. If one has an iterable whose elements are not ideally organized for the task at hand,
a second iterable can be interposed that restructures them so that the task at hand can be expressed more clearly, again allowing
client code to hide the cumbersome details that don't really relate to the meat of the problem. For example, if one's application
is interested in pairs of consecutive primes, an iterable can be created that returns pairs of consecutive primes. This is also illustrated
in the examples below.

The examples below illustrate all of the above advantages of iterables. Our first goal is to find the first prime greater than
100 whose remainder when divided by 7 is 1.
"""


from examples.primes.prime_utils import is_prime

# This example doesn't use custom iterables. It is clunkier because the
# filtering logic has to be made explicit *inside client code*
def find_primes_klunky_example1():
    """
    Find the first prime greater than 100 equal to 1 mod 7.
    :return:
    """
    x = 100
    while True:
        if is_prime(x):
            if x % 7 == 1:
                return x
        x += 1

print()
print()
print("Running clunky example1")
print(find_primes_klunky_example1())


# This example uses a custom iterable that hides all the logic necessary to prepare the collection
# of primes greater than 100. The client-code can focus on its central purpose without getting bogged down
# by the details of filtering integers to just the primes.
def find_primes_elegant_example1():
    """
    Find the first prime greater than 100 equal to 1 mod 7.
    :return:
    """
    for prime in PrimesInRange(start = 100):
        if prime % 7 == 1:
            return prime

# Here we define the iterable and iterator objects necessary to allow the above elegant code to work.
# It's more work than the "clunky" example, but it has two advantages: it creates a reusable iterable over primes,
# and it hides all the logic so that it doesn't need to be part of client code.
class PrimesInRange(object):
    """
    Represents the collection of primes between integers start (inclusive) and finish (exclusive).
    If finish is not supplied, it is taken to be infinity.
    """
    def __init__(self, start = 2, finish = float('inf')):
        """
        :param start: the lower bound (inclusive) for the sequence of primes to represent.
        :param finish: The upper bound (exclusive) for the sequence of primes to represent.
        """
        self.start = start
        self.finish = finish

    def __iter__(self):
        """
        All iterables in python must define this method. An iterable is an object that knows how to return an iterator version of itself.
        For example, a list is not an iterator, but it knows how to turn itself into an iterator. Since instances of this class
        are also iterators, the __iter__() method just needs to return self.
        :return:
        """
        return PrimeIterator(self)


class PrimeIterator(object):
    """
    Represents a single iteration through all primes between start (inclusive) and finish (exclusive)
    of our primes_in_range iterable.
    """
    def __init__(self, primes_in_range_iterable):
        self.iterable = primes_in_range_iterable
        self.next_to_test = self.iterable.start  # This member variable keeps track of the next integer we will test for primality.

    def __next__(self):
        """
        Return the next prime in the specified range, or raise a StopIteration exception if we've already returned the last prime in range.
        :return:
        """
        found_prime = None
        while self.next_to_test < self.iterable.finish:
            if is_prime(self.next_to_test):
                found_prime = self.next_to_test
            self.next_to_test += 1
            if found_prime:
                return found_prime
        raise StopIteration

print()
print()
print("Running elegant example1")
print(find_primes_elegant_example1())

"""
We now complicate matters a little bit. In this example our goal is to find the first two *consecutive* primes greater than 100
whose difference is precisely 8. The elegant way to do this is to build another iterable on top of the first. This second iterable
will represent the sequence of consecutive prime pairs.

Note that we don't absolutely need to create this second iterable. We could find what we want just by using the first iterable.
However, notice how elegant the top-level client code becomes when we create the second iterable. None of the cumbersome logic
involving caching the previous prime is visible in the client code. It concentrates solely on the logic it is interested in.
"""


# This example doesn't use custom iterables. It is clunkier because the
# filtering logic has to be made explicit *inside client code*
def find_primes_clunky_example2():
    """
    Find the first two successive primes greater than 100 whose difference is precisely 8.
    :return:
    """
    x1 = 100
    while not is_prime(x1):
        x1 += 1

    while True:
        x2 = x1 + 1
        while not is_prime(x2):
            x2 += 1
        if x2 - x1 == 8:
            return x1, x2
        x1 = x2

print()
print()
print("Running clunky example 2")
print(find_primes_clunky_example2())

# This elegant implementation allows the client level logic to focus just on its central purpose, and hides all
# the nitty-gritty details of filtering integers to prime pairs.
def find_primes_elegant_example2():
    """
    Find the first two successive primes greater than 100 whose difference is precisely 8.
    :return:
    """
    for prime1, prime2 in ConsecutivePrimePairs(start = 100):
        if prime2 - prime1 == 8:
            return prime1, prime2


class ConsecutivePrimePairs(object):
    """
    Represents the sequence of consecutive prime pairs from start (inclusive) to finish (exclusive).
    The sequence is conceived of like this: (2,3), (3, 5), (5, 7), (7, 11), ...
    """

    def __init__(self, start = 2, finish = float('inf')):
        self.iterable = PrimesInRange(start = start, finish = finish)

    def __iter__(self):
        return PrimePairIterator(self.iterable)


class PrimePairIterator(object):
    """
    Represents an iteration over the prime pairs implied by our primes_in_range iterable.
    """
    def __init__(self, primes_in_range_iterable):
        self.primes_iterator = iter(primes_in_range_iterable)
        try:
            self.last_prime = next(self.primes_iterator)  # Represents the last prime returned by the iterator.
        except StopIteration:
            self.last_prime = None

    def __next__(self):
        """
        Return the next successive prime pair
        :return:
        """
        prime = next(self.primes_iterator)
        result = self.last_prime, prime
        self.last_prime = prime
        return result

print()
print()
print("Running elegant example2")
print(find_primes_elegant_example2())

"""
FINAL THOUGHTS ON ITERABLES
Here is a final thought about iterables. One way to think of them is that they formalize the concept of iteration by creating
an object that represents the iteration, one that can be manipulated programmatically, and there is power inherent in this ability.
By contrast, when you create a normal loop in python, the code that represents the loop is *not* an object that can be manipulated.
It can't be passed around to other methods, and you can't programmatically ask it to run its body just once. But you *can* do this
with an iterable. Calling the __next__() method of an iterator is equivalent to asking it to run the body of a loop just once. You can
pass this loop body around to other methods, each of which might ask it to run the loop body one or more times. This is very powerful
control. Whenever you have a normal loop, you could consider turning it into an iterable instead. Most of the time, you won't need
to do this, but sometimes you will find that doing so gives you extra flexibility that you can take advantage of. Here's a typical
example: suppose you have a main loop that embodies the functioning of some complex system whose inner workings you would like to 
"instrument", which means you want to print out some status information about the system each time through its main loop. 
Rather than embedding your instrumentation code throughout the system code, you can embody the system code in an iterable and 
put the instrumentation code in *client* code that calls next() on the iterable, followed by the instrumentation code. This allows you to 
completely separate the system-level code from the instrumentation code. Here's an outline of an example:

class MySystem(object):
  def __init__(self):
    self.foo = 0 # member variable of interest whose value changes each time through the main loop.
    self.bar = 0 # member variable of interest whose value changes each time through the main loop.
    self.baz = 0 # member variable of interest whose value changes each time through the main loop.
  def __iter__(self):
    return self
    
  def __next__(self):
    if self.time_to_stop():
      raise StopIteration()
      
    <implement the body of our main loop>
    
    return self
    
    
# Here we instrument the system by printing out relevant member variables.
# The instrumentation is contained in client code that is wholly isolated from the implementation
# of the system itself.
def my_instrumented_client_code():
  for sys in MySystem():
    print(sys.foo)
    print(sys.bar)
    print(sys.baz)

========== GENERATORS ==========
Despite the elegance and flexibility achieved by using iterables, we must admit that, up to now, they have seemed rather cumbersome
to implement. Up till now, for each iterable you have needed to define an iterable calss, and usually, a separate iterator class
as well. As it turns out, you don't actually need to do all this. There's a cleaner, more concise way to implement iterators
using something called a *generator*.

You'll notice that any iterator class we created above needed to have a member variable that cached some state to remember where it had
left off at the end of the previous __next__() call. Generators take this idea one step further: they *automically* cache *all* the state
of a computation, and they do this for you implicitly, so that you don't have to worry about it. The language construct that
allows this to happen is the "yield" expression. When "yield" is encountered in a function or method, all the internal state 
of the computation is *saved* so that the computation can be continued at a later time *exactly where it left off*. 

Below is a simple generator example. Take a look at the code and then we'll discuss in detail how it works.
"""


def generate_primes_in_range(start, finish = float('inf')):
    """
    Return an iterator that yields primes in the range of start (inclusive) to finish (exclusive).
    :param start: the lower bound (inclusive) for the sequence of primes to represent.
    :param finish: The upper bound (exclusive) for the sequence of primes to represent.
    """
    x = start
    while x < finish:
        if is_prime(x):
            yield x
        x += 1


print()
print()
print("Running generator example")
primes_generator = generate_primes_in_range(4, 15)  # A generator of the primes between 4 (inclusive) and 15 (exclusive)

# Loop through the primes between 4 and 15, printing them.
for prime in primes_generator:
    print(prime)

"""
When generate_primes_in_range() is called above on line 426, the python interpreter notices that the function contains a yield expression
within its function body on line 419. The presence of the "yield" expression tells the interpreter to treat the function as a 
generator. The interpreter therefore handles the function call specially. It evaluates the arguments to the function and assigns
their values to the function's parameters, but it then suspends execution of the function and immediately returns
without executing any of the code that is in its body. The object that it returns is called a generator object, and this is assigned 
to be the value of the variable "primes_generator". This generator object represents the state of execution of the function.
It is both an iterable and an iterator. It returns itself in response to the __iter__()
message, and in response to the __next__() message, it runs its code just up to next occurrence of the yield expression. When it
encounters a yield expression, the argument(s) to yield are returned as the value(s) of the __next__() message.

Let's see how this plays out in line 429 above. They python interpreter notices the for-loop and therefore treats primes_generator as
an iterable. It asks the iterable to give up an iterator for itself by calling __iter__() on it, and, as mentioned above, 
the iterable just returns itself as the iterator.

Treating the generator as an iterator now, python then asks the generator to return its "next" element by sending it a 
__next__() message. This resumes execution of the
generate_primes_in_range() function from the point where it last left off, which was just assigning values to its parameters. 
The initial value of x is 4, but 4 is not
prime, so the yield expression on line 419 is not evaluated. The next time through the loop, the value of x is 5. This *is* prime,
so the yield expression is reached. This causes suspension of the execution of the function and the number 5 is returned as the
value of the __next__() method.

The python interpreter, in executing the for-loop, continues sending __next__() messages to the generator. Every time the 
generator is sent a __next__() message, it resumes execution where it last left off, and keeps executing until
one of two things happens: either it evaluates a yield expression, in which case the argument(s) to yield are returned as the value(s) of 
__next__(), or it evaluates a return expression (which includes "falling off" the end of the function), in which case, instead of
returning from __next__(), it raises a StopIteration exception. In the example above, there is no explicit return statement in the function
body. However, when x hits the value of "finish" (which is set to 15), the while loop exits and the function "falls off" the end
of its code body, which implicitly results in a return, which raises a StopIteration exception and causes the interpreter to terminate
the for-loop. 

The example above didn't use any classes. It just used the function generate_primes_in_range() to return a generator. Often, this is all
you need. But there are limitations to not having a class. For example, the resulting generator object is good
only as an iterator. You can't ask it what its "start" or "finish" are. But, if you use an instance of a class that stores these values
as member variables then you can always interrogate it about its start and finish. The example below shows how this is done.
"""


# This shows how to usefully combine classes with generators. We create a class whose __iter__ method is defined using "yield", which
# makes it a generator
class PrimesInRange2(object):
    """
    Represents the collection of primes between start (inclusive) and finish (exclusive).
    Instances of this class are iterables, since they respond to the __iter__() message.
    """
    def __init__(self, start = 2, finish = float('inf')):
        """
        :param start: the lower bound (inclusive) for the sequence of primes to represent.
        :param finish: The upper bound (exclusive) for the sequence of primes to represent.
        """
        self.start = start
        self.finish = finish

    def __iter__(self):
        """
         Here we dutifully return an iterator over our primes, implemented as a generator.
         Note that we don't return self, which means that we are truly
         just an iterable, but not an iterator. The iterator is what gets returned by this method.
        """
        x = self.start
        while x < self.finish:
            if is_prime(x):
                yield x
            x += 1


print()
print()
print("Running generator from class example")
primes_collection = PrimesInRange2(4, 15)  # An iterable of the primes between 4 (inclusive) and 15 (exclusive)

print(primes_collection.start)   # -> 4
print(primes_collection.finish)  # -> 15

# Loop through the primes between 4 and 15, printing them.
for prime in primes_collection:
    print(prime)
