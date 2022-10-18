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

    file_path = RESOURCES / 'ass3_log_conf.json'   # Create full filepath
    with open(file_path, 'r') as file:   # Open file
        logger = json.load(file)   # Create logger for jsonfile
        logging.config.dictConfig(logger)   # Load logger configs from JSON
    logger = logging.getLogger('ass_3_logger')   # Creating object of the logging
    return logger


def measurements_decorator(func):
    """Function decorator, used for time measurements."""
    @wraps(func)
    def wrapper(nth_nmb: int) -> tuple:

        value = []
        LOGGER.info('Starting measurements...')
        start = timeit.default_timer()   # Start timer
        for i in reversed(range(nth_nmb +1)):  # +1 so it start at nth_nmb and not nth_nmb -1
            result = func(i)   # Get fibonacci value from methods
            value.append(result)   # Add fibonacci values to container
            if i % 5 == 0:   # for each 5th iteration log information
                LOGGER.debug('%s: %s', i, result)

        duration = timeit.default_timer() - start   # Get duration
        return duration, tuple(value)   # Return duration and container as tuple
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
        if _n not in memory:   # Check if value doesn't exist in dict
            memory[_n] = fib(_n - 1) + fib(_n - 2)  # If value doesn't exist its calculated
            return memory[_n]
        return memory[_n]   # Return value in dict
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
    print(f"DURATION FOR EACH APPROACH WITHIN INTERVAL: {nth_value}-0".center(75)+f"{line}")   # Print line and header
    values = ['Seconds', 'Milliseconds', 'Microseconds', 'Nanoseconds']
    print(f"{values[0].rjust(27)}{values[1].rjust(16)}{values[2].rjust(16)}{values[3].rjust(16)}")   # Print column headers
    for key, val in fib_details.items():   # Get data from fib_details and declare it as key and val
        duration = (val[0])   # Get duration
        sec = duration_format(duration, values[0])   # Get seconds from duration_format
        millisec = duration_format(duration, values[1])   # Get milliseconds from duration_format
        microsec = duration_format(duration, values[2])   # Get microseconds from duration_format
        nanosec = duration_format(duration, values[3])   # Get nanoseconds from duration_format
        print(f"{key.title().ljust(20)}{sec.rjust(0)}{millisec.rjust(16)}{microsec.rjust(16)}{nanosec.rjust(16)}")


def write_to_file(fib_details: dict):
    """Function to write information to file."""

    for key, val in fib_details.items():   # Get data from fib_details and declare it as key and val
        file_path = RESOURCES / (key.replace(' ', '_') + '.txt')   # Modify name for textfiles
        f = open(f"{file_path}", "w+")   # Create new textfiles
        new_value = val[1]  # Get values from fib_details and reverse list
        seq_and_value = tuple(zip(itertools.count(30, -1), new_value))   # Add sequence to tuple of values
        for data in seq_and_value:   # Get each item in tuple
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
