"""Solves an instance.

Modify this file to implement your own solvers.

For usage, run `python3 solve.py --help`.
"""

import argparse
import math
from pathlib import Path
from typing import Callable, Dict

from instance import Instance
from solution import Solution
from file_wrappers import StdinFileWrapper, StdoutFileWrapper
import numpy as np
from scipy.optimize import minimize
from scipy.optimize import LinearConstraint
from scipy.optimize import NonlinearConstraint


def solve_naive(instance: Instance) -> Solution:
    return Solution(
        instance=instance,
        towers=instance.cities,
    )

def penalty(x_list):
    w_list = generate_w(x_list)
    return sum([x_list[i] * 170 * (math.e ** (0.17 * w_list[i])) for i in range(len(x_list))]) 

def generate_w(x_list):
    w_list = []
    for i in range(len(x_list)):
        x = x_list[i]


def solve(instance: Instance) -> Solution:
    r_s = instance.R_s()
    r_p = instance.R_p()
    d = instance.D()
    n = instance.N()

    def penalty(x_list):
        w_list = generate_w(x_list)
        return sum([x_list[i] * 170 * (math.e ** (0.17 * w_list[i])) for i in range(len(x_list))])  

    
    def generate_w(x_list):
        w_list = []
        tower_list = []
        for i in range(len(x_list)):
            x = x_list[i] 
            r_pos = i // d
            r_col = i % d
            if x >= 0.5:
                tower_list.append((r_pos, r_col))
        
        for tower in tower_list:
            x = tower[0]
            y = tower[1]
            count = 0
            for neighbor in tower_list:
                n_x = neighbor[0]
                n_y = neighbor[1]
                if x != n_x and y != n_y:
                    dist = ((n_x - x) ** 2 + (n_y - y) ** 2) ** (1/2)
                    if dist <= r_p:
                        count += 1
            w_list.append(count)

        return w_list
    
    x0 = [0 for i in range(d ** 2)]
    return Solution(
        instance=instance, 
        towers=minimize(penalty, x0, method=)
    )


# constraints
 sum(dist(city_a, tower_b) for all b) >= 1
 


SOLVERS: Dict[str, Callable[[Instance], Solution]] = {
    "naive": solve_naive
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
