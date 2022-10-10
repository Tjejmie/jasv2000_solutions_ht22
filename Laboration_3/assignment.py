#!/usr/bin/env python

""" DT179G - LAB ASSIGNMENT 3
You find the description for the assignment in Moodle, where each detail regarding requirements
are stated. Below you find the inherent code, some of which fully defined. You add implementation
for those functions which are needed:

 - create_logger()
 - measurements_decorator(..)
 - fibonacci_memory(..)
 - print_statistics(..)
 - write_to_file(..)
"""

from pathlib import Path
from functools import wraps
import argparse
import logging
import logging.config
import json
import timeit
import itertools

__version__ = '1.1'
__desc__ = "Program used for measuríng execution time of various Fibonacci implementations!"

RESOURCES = Path(__file__).parent / "../_Resources/"


def create_logger() -> logging.Logger:
    """Create and return logger object."""
    print("entering function create_logger")



    file_path = RESOURCES / 'ass3_log_conf.json'
    with open(file_path, 'r') as file:
        config = json.load(file)
        logging.config.dictConfig(config)

        #logger = logging.getLogger('ass_3_logger')
        #logger.info('This is a test')


    print("exiting function create_logger")

def measurements_decorator(func):
    """Function decorator, used for time measurements."""

    @wraps(func)
    def wrapper(nth_nmb: int) -> tuple:

        container = []

        logger = logging.getLogger('ass_3_logger')
        logger.info('Starting measurements...')
        start = timeit.default_timer()
        for i in reversed(range(nth_nmb +1)):  # +1 so it start at nth_nmb and not nth_nmb -1
            result = func(i)
            container.append(result)
            if i % 5 == 0:
                logger.debug('%s: %s', i, result)

        duration = timeit.default_timer() - start


        return duration, tuple(container)


    return wrapper


@measurements_decorator
def fibonacci_iterative(nth_nmb: int) -> int:
    """An iterative approach to find Fibonacci sequence value.
    YOU MAY NOT MODIFY ANYTHING IN THIS FUNCTION!!"""

    old, new = 0, 1
    if nth_nmb in (0, 1):
        return nth_nmb
    for __ in range(nth_nmb - 1):
        old, new = new, old + new


    return new


@measurements_decorator
def fibonacci_recursive(nth_nmb: int) -> int:
    """An recursive approach to find Fibonacci sequence value.
    YOU MAY NOT MODIFY ANYTHING IN THIS FUNCTION!!"""

    def fib(_n):
        return _n if _n <= 1 else fib(_n - 1) + fib(_n - 2)


    return fib(nth_nmb)


@measurements_decorator
def fibonacci_memory(nth_nmb: int) -> int:
    """An recursive approach to find Fibonacci sequence value, storing those already calculated."""

    memory = {0: 0, 1: 1}
    def fib(_n):
        if _n in memory:
            return memory[_n]
        memory[_n] = fib(_n - 1) + fib(_n - 2)
        return memory[_n]
    return fib(nth_nmb)




def duration_format(duration: float, precision: str) -> str:
    """Function to convert number into string. Switcher is dictionary type here.
    YOU MAY NOT MODIFY ANYTHING IN THIS FUNCTION!!"""
    switcher = {
        'Seconds': "{:.5f}".format(duration),
        'Milliseconds': "{:.5f}".format(duration * 1_000),
        'Microseconds': "{:.1f}".format(duration * 1_000_000),
        'Nanoseconds': "{:d}".format(int(duration * 1_000_000_000))
    }

    # get() method of dictionary data type returns value of passed argument if it is present in
    # dictionary otherwise second argument will be assigned as default value of passed argument

    return switcher.get(precision, "nothing")


def print_statistics(fib_details: dict, nth_value: int):
    """Function which handles printing to console."""

    line = '\n' + ("---------------" * 5)

    print(line)
    print(f"DURATION FOR EACH APPROACH WITHIN INTERVAL: {nth_value}-0".center(75)+f"{line}")

    values = ['Seconds', 'Milliseconds', 'Microseconds', 'Nanoseconds']
    print(f"{values[0].rjust(27)}{values[1].rjust(16)}{values[2].rjust(16)}{values[3].rjust(16)}")
    for key, val in fib_details.items():
        duration = (val[0])
        sec = duration_format(duration, values[0])
        millisec = duration_format(duration, values[1])
        microsec = duration_format(duration, values[2])
        nanosec = duration_format(duration, values[3])
        print(f"{key.title().ljust(20)}{sec.rjust(0)}{millisec.rjust(16)}{microsec.rjust(16)}{nanosec.rjust(16)}")

def write_to_file(fib_details: dict):
    """Function to write information to file."""

    for key, val in fib_details.items():   # Get data from fib_details and declare it as key and val
        result = key.replace(' ', '_') + '.text'   # Modify name for textfiles
        file_path = RESOURCES / result
        f = open(f"{file_path}", "w+")   # Create new textfiles
        value = (val[1])   # Get value from fib_details
        newValue = reversed(value)   # Reverse list of values so it starts at 0
        #result = tuple(result)
        seqAndValue = tuple(zip(itertools.count(), newValue))   # Add sequence to tuple of values

        result = reversed(seqAndValue)  # Reverse tuple of sequence and value
        #result = tuple(result)
        for data in result:   # Get each item in tuple
            f.write("%s: %s \n" % data)   # Write item in file


def main():
    """The main program execution. YOU MAY NOT MODIFY ANYTHING IN THIS FUNCTION!!"""

    epilog = "DT179G Assignment 3 v" + __version__
    parser = argparse.ArgumentParser(description=__desc__, epilog=epilog, add_help=True)
    parser.add_argument('nth', metavar='nth', type=int, nargs='?', default=30,
                        help="nth Fibonacci sequence to find.")

    global LOGGER  # ignore warnings raised from linters, such as PyLint!
    LOGGER = create_logger()

    args = parser.parse_args()
    nth_value = args.nth  # nth value to sequence. Will fallback on default value!

    fib_details = {  # store measurement information in a dictionary
        'fib iteration': fibonacci_iterative(nth_value),
        'fib recursion': fibonacci_recursive(nth_value),
        'fib memory': fibonacci_memory(nth_value)
    }

    print_statistics(fib_details, nth_value)    # print information in console
    write_to_file(fib_details)                  # write data files

if __name__ == "__main__":
    main()
