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
import pyomo.environ as pyo
from pyomo.environ import *



def solve_naive(instance: Instance) -> Solution:
    return Solution(
        instance=instance,
        towers=instance.cities,
    ) 

def generate_w(instance, m):
    w = [[0 for j in instance.D()] for i in instance.D()]
    for i in m.I:
        for j in m.J:
            if m.x[i, j] == 1:
                counter = 0
                for x in m.I:
                    for y in m.J:
                        if x != i and y != j:
                            if m.x[x, y] == 1 and euclid_distance(i, x, j, y) <= m.rp:
                                counter += 1
                w[i][j] = counter
    return w

def generate_cities(instance):
    grid = [[0 for j in instance.D()] for i in instance.D()]
    for city in instance.cities:
        i = city.x
        j = city.y
        grid[i][j] = 1
    return grid


def euclid_distance(x1, x2, y1, y2):
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** (1/2)

def solve(instance: Instance) -> Solution:
    model = pyo.AbstractModel()

    model.I = pyo.RangeSet(1, instance.D(), 1)
    model.J = pyo.RangeSet(1, instance.D(), 1)

    # PARAMETERS
    model.rs = instance.R_s()
    model.rp = instance.R_p()
    # m.c is 2D array with entry 1 if city at (i, j)
    model.c = generate_cities(instance)
    # m.w is 2D array with entry count of towers <= rp for tower at (i, j)
    model.w = generate_w(instance, model)

    # VARIABLES
    # m.x is 1 if tower at (i, j)
    model.x = pyo.Var(model.I, model.J, domain=pyo.Binary)


    # OBJECTIVE
    def obj_expression(m):
        penalty = 0
        for i in m.I:
            for j in m.J:
                penalty += 170 * m.x[i, j] * math.e ** (0.17 * w[i][j]) 
        return penalty

    model.OBJ = pyo.Objective(rule=obj_expression, sense=minimize)

    # CONSTRAINTS
    model.citiesConstraint = pyo.Constraint(model.I, model.J, rule=cities_covered_rule)

    def cities_covered_rule(m, i, j):
        # return the expression for the constraint for (i, j)
        if m.c[i][j] == 1:
            counter = 0
            for x in m.I:
                for y in m.J:
                    if m.x[x, y] == 1 and euclid_distance(i, x, j, y) <= m.rs:
                        counter += 1
            if counter < 1:
                return False
        return True

    SolverFactory('mindtpy').solve(model, mip_solver='glpk', nlp_solver='ipopt')


SOLVERS: Dict[str, Callable[[Instance], Solution]] = {
    "naive": solve_naive,
    "cococo": solve
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
