"""Solves an instance.

Modify this file to implement your own solvers.

For usage, run `python3 solve.py --help`.
"""

import argparse
from ast import Constant
import math
from pathlib import Path
from re import M
from typing import Callable, Dict, List

from instance import Instance
from solution import Solution
from point import Point
from file_wrappers import StdinFileWrapper, StdoutFileWrapper

from heapq import *
import random

def solve_naive(instance: Instance) -> Solution:
    return Solution(
        instance=instance,
        towers=instance.cities,
    ) 

def solve_greedy(instance: Instance) -> Solution:
    return Solution(
        instance = instance,
        towers = greedy(instance),
    )

def greedy(instance: Instance) -> List[Point]:
    towers = []
    num_cities = instance.N
    cities = set(instance.cities)
    counted_but_zero = set()

    while num_cities > 0:
        # get all valid towers
        num_cities_covered = []
        for i in range(instance.D):
            for j in range(instance.D):
                if (i, j) not in counted_but_zero:
                    colette = count_neighbors(instance, cities, towers, i, j)
                    if colette[0] == 0:
                        counted_but_zero.add((i, j))
                    heappush(num_cities_covered, (-colette[1], (i, j)))
        
        # choose a tower
        top_towers = [heappop(num_cities_covered) for _ in range(min(instance.D // 10, len(num_cities_covered)))]
        top_tower = random.choice(top_towers)
        tower_pos = top_tower[1]
        tower_x = tower_pos[0]
        tower_y = tower_pos[1]
        towers.append(Point(tower_x, tower_y))

        for city in set(cities):
            if euclid_distance(tower_x, city.x, tower_y, city.y) <= instance.R_s:
                cities.remove(city)
                num_cities -= 1

    return towers

def count_neighbors(instance, cities, towers, x, y):
    weight = count = 0
    for city in cities:
        if euclid_distance(x, city.x, y, city.y) <= instance.R_s:
            weight += 1
            count += 1

        if min(city.x, instance.D - city.x - 1) == 0 or min(city.y, instance.D - city.y - 1) == 0:
            weight += instance.R_s
            if min(city.x, instance.D - city.x - 1) == 0 and min(city.y, instance.D - city.y - 1) == 0: 
                weight += 2

    for tower in towers:
        if euclid_distance(x, tower.x, y, tower.y) <= instance.R_p:
            weight -= 0.5
    return (count, weight)

def euclid_distance(x1, x2, y1, y2):
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** (1/2)

SOLVERS: Dict[str, Callable[[Instance], Solution]] = {
    "naive": solve_naive,
    "greedy": solve_greedy,
}

# You shouldn't need to modify anything below this line.
def infile(args):
    if args.input == "-":
        return StdinFileWrapper()

    return Path(args.input).open("r")


def outfile(args):
    if args.output == "-":
        return StdoutFileWrapper()

    return Path(args.output).open("w")


def main(args):
    with infile(args) as f:
        instance = Instance.parse(f.readlines())
        solver = SOLVERS[args.solver]
        solution = solver(instance)
        assert solution.valid()
        with outfile(args) as g:
            print("# Penalty: ", solution.penalty(), file=g)
            solution.serialize(g)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Solve a problem instance.")
    parser.add_argument("input", type=str, help="The input instance file to "
                        "read an instance from. Use - for stdin.")
    parser.add_argument("--solver", required=True, type=str,
                        help="The solver type.", choices=SOLVERS.keys())
    parser.add_argument("output", type=str,
                        help="The output file. Use - for stdout.",
                        default="-")
    main(parser.parse_args())
