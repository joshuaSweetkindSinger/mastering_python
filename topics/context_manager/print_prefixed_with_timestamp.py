"""
This file illustrates the use of the decorator @contextmanager by creating
a context that alters the way the built-in print() behaves. The full exercise is stated below:

Small Exercise to test your understanding of "with"
--------------------------------------------------
Create a context manager that prefixes all print statements with the current date and time using a format specified by the client.  I recommend using the @contextmanager decorator to do this. An example of usage of the new context would be:

with print_prefixed_by_timestamp("%m/%d/%Y--%H %M %S"):

print("hello world")

print("goodbye world")

print("hello again")



The output of the above program would be:

02/07/2017--10:05:32–hello world

02/07/2017--10:05:32–goodbye world

hello again



Several notes to make the above easier:

The "print" function is not normally available as a built-in in python 2.7 (but it is in python 3.6) since the name print is recognized as the print statement. To disable the statement and use the print()function, use this future statement at the top of your module:

from __future__ import print_function
To get the current date and time represented as a readable string, do this:

    import datetime
    datetime.datetime.now().strftime(date_format_string),

where date_format_string is a string like

    "%m/%d/%Y -- %H %M %S"

You're going to want to "bash" the print function in order to make the context manager work,
temporarily replacing print with your own function. For example:

    global print # This is necessary to be able to reassign the value of the global print().
    old_print = print
    def new_print(string):
        old_print(datetime.datetime.now().strftime(date_format_string), end = '–')
        old_print(string)
        print = new_print

In order to restore the original print function when you're done, you can just do "print = old_print"
There is no need to create tests for this exercise or to worry about coding best practices too much.
The main point is just to get practice with context managers.
"""
from contextlib import contextmanager
import datetime


@contextmanager
def print_prefixed_by_timestamp(date_time_format):
    """
    Prefix any print statement within our context by the current date and time,
    formatting it as specified by date_time_format.
    :param date_time_format: A string that specifies the format for the date and time,
                             whose syntax is dictated by the strftime() method of datetime.datime.
    :return: None
    """
    global print

    old_print = print # Save the old print() so we can restore it later.

    # Define a new print function that prefixes the formatted time when printing.
    def new_print(s, *args, **kwds):
        """
        Print the string s, prefixed by the current time.
        :param s:
        :return: None
        """
        old_print(datetime.datetime.now().strftime(date_time_format), end = '--')
        old_print(s, *args, **kwds)


    print = new_print  # Bash the built-in print() to use our new print function
    yield              # yield the context: all print() calls done here will use new_print()
    print = old_print  # Restore the original print function


def test():
    with print_prefixed_by_timestamp("%m/%d/%Y--%H %M %S"):
        print("hello world")
        print("goodbye world")
    print("hello again")

if __name__ == '__main__':
    test()