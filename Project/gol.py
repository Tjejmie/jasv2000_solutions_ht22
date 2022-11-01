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
import pathlib
import ast
from functools import wraps
__version__ = '1.0'
__desc__ = "A simplified implementation of Conway's Game of Life."

RESOURCES = Path(__file__).parent / "../_Resources/"


# -----------------------------------------
# IMPLEMENTATIONS FOR HIGHER GRADES, C - B
# -----------------------------------------

def load_seed_from_file(_file_name: str) -> tuple:
    """ Load population seed from file. Returns tuple: population (dict) and world_size (tuple). """

    _file_name = f"{_file_name}.json" if ".json" not in _file_name else _file_name
    file_path = pathlib.Path(RESOURCES / _file_name)
    population = {}

    with open(file_path, 'r') as file:
        data = json.load(file)
        for element in data.values():
            if isinstance(element, dict):
                for key, value in element.items():
                    # Add key as int and value to population
                    population.setdefault(ast.literal_eval(key), value)
            if isinstance(element, list):
                # Get world size from json and save as tuple
                world_size = tuple(element)
    # Return tuple containing population and world size
    return_value = population, (world_size[1], world_size[0])
    return tuple(return_value)


def create_logger() -> logging.Logger:
    """ Creates a logging object to be used for reports. """
    log_path = RESOURCES / 'gol.log'
    logger = logging.getLogger('gol_logger')
    logger.setLevel(logging.INFO)
    file_handler = logging.FileHandler(log_path, mode='w')
    file_handler.setLevel(logging.INFO)
    logger.addHandler(file_handler)

    return logger


def simulation_decorator(func):
    """ Function decorator, used to run full extent of simulation. """

    @wraps(func)
    def wrapper(_generation: int, _population: dict, _world_size: tuple):
        logger = create_logger()

        for i in range(_generation):
            count_alive, count_dead, count_rim = 0,0,0

            cb.clear_console()
            for key, value in _population.items():
                if value is not None and value['state'] != '#':
                    if value['state'] == 'X':
                        count_alive +=1
                    if value['state'] == '-':
                        count_dead +=1
                else:
                    count_rim +=1

            logger.info(f"GENERATION {i}")
            logger.info(f"  Population: {len(_population) - count_rim}")
            logger.info(f"  Alive: {count_alive}")
            logger.info(f"  Dead: {count_dead}")

            _population = func(_generation, _population, _world_size)
            sleep(0.200)

    return wrapper


# -----------------------------------------
# BASE IMPLEMENTATIONS
# -----------------------------------------

def parse_world_size_arg(_arg: str) -> tuple:
    """ Parse width and height from command argument. """

    # Split string and add items to list. Filter none
    values = list(filter(None, _arg.split('x')))
    try:
        values = [int(num) for num in values]   # Convert value in list to int
        if len(values) != 2:   # Check if list has two items
            raise AssertionError("World size should contain width and height, "
                                 "seperated by 'x'. Ex: '80x40'")
        for num in values:
            if num <= 0:   # Check that list contain positive number above zero
                raise ValueError("Both width and height needs to have "
                                 "positive values above zero.")
    except (ValueError, AssertionError) as myError:
            print(myError)   # Print error
            values = [80, 40]   # set default value
            print("Using default world size: 80x40")

    return tuple(values)


def populate_world(_world_size: tuple, _seed_pattern: str = None) -> dict:
    """ Populate the world with cells and initial states. """

    height = list(range(0, _world_size[0]))
    width = list(range(0, _world_size[1]))
    # Get all coordinates on world
    coordinates = (tuple(product(height, width)))
    pattern = cb.get_pattern(_seed_pattern, (_world_size[1], _world_size[0]))
    population = {}

    for cell in coordinates:
        # Get all rim-cells
        if 0 in cell or cell[0] == _world_size[0]-1 or cell[1] == _world_size[1]-1:
            population[cell] = None
            continue
        # Check if pattern exist and determine cell state
        if pattern is not None:
            if cell in pattern:
                population[cell] = {'state': cb.STATE_ALIVE}
            else:
                population[cell] = {'state': cb.STATE_DEAD}
        # Randomize cell state
        else:
            random_number = random.randint(0, 20)
            if random_number > 16:
                population[cell] = {'state': cb.STATE_ALIVE}
            else:
                population[cell] = {'state': cb.STATE_DEAD}
        neighbours = calc_neighbour_positions(cell)   # Get neighbours for cell
        population[cell]['neighbours'] = neighbours   # Add neighbors in dict

    return population


def calc_neighbour_positions(_cell_coord: tuple) -> list:
    """ Calculate neighbouring cell coordinates in all directions (cardinal + diagonal).
    Returns list of tuples. """

    coords = [(-1, -1), (0, -1), (1, -1), (-1, 0),
               (1, 0), (-1, 1), (0, 1), (1, 1)]
    x, y = _cell_coord
    # Calculate neighbours in all directions
    neighbours = {(x + x_add, y + y_add) for x_add, y_add in coords}
    return list(neighbours)

@simulation_decorator
def run_simulation(_generation: int, _population: dict, _world_size: tuple):
    """ Runs simulation for specified amount of generations. """
    return update_world(_population, _world_size)


def update_world(_cur_gen: dict, _world_size: tuple) -> dict:
    """ Represents a tick in the simulation. """

    next_gen = {}
    for cell in _cur_gen:
        if _cur_gen[cell] is None: # Value '#' for rim-cells
            _cur_gen[cell] = {'state': cb.STATE_RIM}
            #   Get cell-state and color
        color = cb.get_print_value(list(_cur_gen[cell].values())[0])
        #   Each row ends with line break
        cb.progress(f"{color}\n") if cell[1] == _world_size[1]-1 \
            else cb.progress(f"{color}")

        # Control that it's not a rim-cell and update state
        if '#' not in _cur_gen[cell].values():
            neighbours = calc_neighbour_positions(cell)
            count = count_alive_neighbours(neighbours ,_cur_gen)
            if _cur_gen[cell]['state'] == 'X' and count == 2 or count == 3:
                next_gen[cell] = {'state': 'X'}
            elif _cur_gen[cell]['state'] == '-' and count == 3:
                next_gen[cell] = {'state': 'X'}
            else:
                next_gen[cell] = {'state': '-'}
        else:
            next_gen[cell] = {'state': cb.STATE_RIM}

    return next_gen


def count_alive_neighbours(_neighbours: list, _cells: dict) -> int:
    """ Determine how many of the neighbouring cells are currently alive. """

    count = 0
    #  Check if it's an ordinary cell and is alive
    for i in _neighbours:
        if _cells[i] is not None and _cells[i]['state'] == 'X':
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
