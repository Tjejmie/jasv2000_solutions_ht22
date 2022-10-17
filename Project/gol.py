#!/usr/bin/env python
"""
The universe of the Game of Life is an infinite two-dimensional orthogonal grid of square cells,
each of which is in one of two possible states, alive or dead (populated or unpopulated).
Every cell interacts with its eight neighbours, which are the cells that are horizontally,
vertically, or diagonally adjacent.

At each step in time, the following transitions occur:

****************************************************************************************************
   1. Any live cell with fewer than two live neighbours dies, as if caused by underpopulation.
   2. Any live cell with two or three live neighbours lives on to the next generation.
   3. Any live cell with more than three live neighbours dies, as if by overpopulation.
   4. Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
****************************************************************************************************

The initial pattern constitutes the seed of the system.

The first generation is created by applying the above rules simultaneously to every cell in the
seed—births and deaths occur simultaneously, and the discrete moment at which this happens is
sometimes called a tick. The rules continue to be applied repeatedly to create further generations.

You run this script as a module:
    python -m Project.gol.py
"""

import argparse
import random
import json
import logging
import itertools
from pathlib import Path
from ast import literal_eval
from time import sleep
from itertools import product
import Project.code_base as cb

__version__ = '1.0'
__desc__ = "A simplified implementation of Conway's Game of Life."

RESOURCES = Path(__file__).parent / "../_Resources/"


# -----------------------------------------
# IMPLEMENTATIONS FOR HIGHER GRADES, C - B
# -----------------------------------------

def load_seed_from_file(_file_name: str) -> tuple:
    """ Load population seed from file. Returns tuple: population (dict) and world_size (tuple). """
    pass


def create_logger() -> logging.Logger:
    """ Creates a logging object to be used for reports. """
    pass


def simulation_decorator(func):
    """ Function decorator, used to run full extent of simulation. """
    pass


# -----------------------------------------
# BASE IMPLEMENTATIONS
# -----------------------------------------

def parse_world_size_arg(_arg: str) -> tuple:
    """ Parse width and height from command argument. """

    values = list(filter(None, _arg.split('x')))   # Split string and add items to list. Filter none

    try:
        values = [int(num) for num in values]   # Convert value in list to int
        if len(values) != 2:   # Check if list has two items
            raise AssertionError("World size should contain width and height, seperated by 'x'. Ex: '80x40'")

        for num in values:
            if num <= 0:   # Check that list contain positive number above zero
                raise ValueError("Both width and height needs to have positive values above zero.")

    except (ValueError, AssertionError) as myError:
            print(myError)   # Print error
            values = [80, 40]   # set default value
            print("Using default world size: 80x40")

    return tuple(values)

def populate_world(_world_size: tuple, _seed_pattern: str = None) -> dict:
    """ Populate the world with cells and initial states. """

    int1, int2 = _world_size
    height = list(range(0, int1))
    width = list(range(0, int2))
    coordinates = (tuple(product(height, width)))

    pattern = cb.get_pattern(_seed_pattern, (int2, int1))

    population = {}

    for cell in coordinates:
        if 0 in cell or cell[0] == int1-1 or cell[1] == int2-1:   # Get all values that's on the "edge"
            population[cell] = None
            continue

        if _seed_pattern is not None:    # Fixa att den går igenom loopen innan den går till neighbour

            if cell in pattern:
                population[cell] = {'state': cb.STATE_ALIVE}

            else:
                population[cell] = {'state': cb.STATE_DEAD}


        else:
            random_number = random.randint(0, 20)
            #population[cell] = {}
            if random_number > 16:
                population[cell] = {'state': cb.STATE_ALIVE}
                #population[cell]['state'] = cb.STATE_ALIVE
            else:
                population[cell] = {'state': cb.STATE_DEAD}



        neighbours = calc_neighbour_positions(cell)

        population[cell]['neighbours'] = neighbours

    return population

def calc_neighbour_positions(_cell_coord: tuple) -> list:
    """ Calculate neighbouring cell coordinates in all directions (cardinal + diagonal).
    Returns list of tuples. """

    coords = [(-1, -1), (0, -1), (1, -1), (-1, 0),
               (1, 0), (-1, 1), (0, 1), (1, 1)]

    x, y = _cell_coord

    neighbours = {(x + x_add, y + y_add) for x_add, y_add in coords}
    return list(neighbours)

def run_simulation(_nth_generation: int, _population: dict, _world_size: tuple):
    """ Runs simulation for specified amount of generations. """


    cb.clear_console()

    _population = update_world(_population, _world_size)
    sleep(0.100)

    True if _nth_generation <= 1 else run_simulation(_nth_generation - 1, _population, _world_size)
    #   Runs simulation if needed





def update_world(_cur_gen: dict, _world_size: tuple) -> dict:
    """ Represents a tick in the simulation. """
    int1, int2 = _world_size
    nextGen = {}

    for cell in _cur_gen:
        if _cur_gen[cell] is None:
            _cur_gen[cell] = {}
            _cur_gen[cell]['state'] = cb.STATE_RIM

        res = list(_cur_gen[cell].values())[0]
        color = cb.get_print_value(res)

        if cell[1] == int2-1:
            cb.progress(f"{color}\n")
        else:
            cb.progress(f"{color}")


    for cell in _cur_gen:
        if '#' not in _cur_gen[cell].values():
            neighbours = calc_neighbour_positions(cell)
            count = count_alive_neighbours(neighbours ,_cur_gen)
            if _cur_gen[cell]['state'] == 'X' and count == 2 or count == 3:

                nextGen[cell] = {'state': 'X'}
            elif _cur_gen[cell]['state'] == '-' and count == 3:
                nextGen[cell] = {'state': 'X'}
            else:
                nextGen[cell] = {'state': '-'}
        if _cur_gen[cell]['state'] == '#':
            nextGen[cell] = {}
            nextGen[cell]['state'] = cb.STATE_RIM


    return nextGen



def count_alive_neighbours(_neighbours: list, _cells: dict) -> int:
    """ Determine how many of the neighbouring cells are currently alive. """

    count = 0
    for i in _neighbours:
        if _cells[i]['state'] == 'X':
            count +=1
    return count


def main():
    """ The main program execution. YOU MAY NOT MODIFY ANYTHING IN THIS FUNCTION!! """
    epilog = "DT179G Project v" + __version__
    parser = argparse.ArgumentParser(description=__desc__, epilog=epilog, add_help=True)
    parser.add_argument('-g', '--generations', dest='generations', type=int, default=2,
                        help='Amount of generations the simulation should run. Defaults to 50.')
    parser.add_argument('-s', '--seed', dest='seed', type=str,
                        help='Starting seed. If omitted, a randomized seed will be used.')
    parser.add_argument('-ws', '--worldsize', dest='worldsize', type=str, default='10x20',
                        help='Size of the world, in terms of width and height. Defaults to 80x40.')
    parser.add_argument('-f', '--file', dest='file', type=str,
                        help='Load starting seed from file.')

    args = parser.parse_args()

    try:
        if not args.file:
            raise AssertionError
        population, world_size = load_seed_from_file(args.file)
    except (AssertionError, FileNotFoundError):
        world_size = parse_world_size_arg(args.worldsize)
        population = populate_world(world_size, args.seed)

    run_simulation(args.generations, population, world_size)


if __name__ == "__main__":
    main()
