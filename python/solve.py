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
# import pyomo.environ as pyo
# from pyomo.environ import *
# from pyomo.opt import SolverFactory

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

    grid = [[0 for _ in range(instance.D)] for _ in range(instance.D)]
    for city in instance.cities:
        grid[city.x][city.y] = 1

    while num_cities > 0:
        # get all valid towers
        num_cities_covered = []
        for i in range(instance.D):
            for j in range(instance.D):
                heappush(num_cities_covered, (-count_neighbors(instance, grid, i, j, towers), (i, j)))
        
        # choose a tower
        top_towers = [heappop(num_cities_covered) for _ in range(instance.D // 10)]
        top_tower = random.choice(top_towers)
        tower_pos = top_tower[1]
        tower_x = tower_pos[0]
        tower_y = tower_pos[1]
        towers.append(Point(tower_x, tower_y))
        grid[tower_x][tower_y] = 2

        # process tower (edit grid, edit instance.cities)
        for i in range(tower_x - instance.R_s, tower_x + instance.R_s + 1):
            for j in range(tower_y - instance.R_s, tower_y + instance.R_s + 1):
                # print("lee")
                if 0 <= i < instance.D and 0 <= j < instance.D and euclid_distance(tower_x, i, tower_y, j) <= instance.R_s:
                    # print("colette")
                    if grid[i][j] == 1:
                        # print("for hkn officer")
                        grid[i][j] = 0
                        num_cities -= 1
    
    return towers

def count_neighbors(instance, grid, x, y, towers):
    count = 0  
    for i in range(x - instance.R_p, x + instance.R_p + 1):
        for j in range(y - instance.R_p, y + instance.R_p + 1):
            if 0 <= i < instance.D and 0 <= j < instance.D:
                if euclid_distance(x, i, y, j) <= instance.R_p: 
                    if grid[i][j] == 2:
                        count -= 0.5
                if euclid_distance(x, i, y, j) <= instance.R_s:
                    if grid[i][j] == 1:
                        count += 1
                        # if (i, j) is on border
                        if min(i, instance.D - i - 1) == 0 or min(j, instance.D - j - 1) == 0:
                            count += instance.R_s
                            # if (i, j) is corner, add even more weight
                            if min(i, instance.D - i - 1) == 0 and min(j, instance.D - j - 1) == 0: 
                                count += 2    
    return count

# def generate_w(instance, m):
#     w = [[0 for _ in range(instance.D)] for _ in range(instance.D)]
#     for i in m.I:
#         for j in m.J:
#             if m.x.extract_values()[(i, j)] == 1:
#                 counter = 0
#                 for x in m.I:
#                     for y in m.J:
#                         if x != i and y != j:
#                             if m.x.extract_values()[(x, y)] == 1 and euclid_distance(i, x, j, y) <= m.rp:
#                                 counter += 1
#                 w[i][j] = counter
#     return w

# def generate_cities(instance):
#     grid = [[0 for _ in range(instance.D)] for _ in range(instance.D)]
#     for city in instance.cities:
#         i = city.x
#         j = city.y
#         grid[i][j] = 1
#     return grid

def euclid_distance(x1, x2, y1, y2):
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** (1/2)

# def solve_minlp(instance: Instance) -> Solution:
#     def obj_expression(m):
#         penalty = 0
#         # w is 2D array with entry count of towers <= rp for tower at (i, j)
#         w = generate_w(instance, m)
#         for i in m.I:
#             for j in m.J:
#                 penalty += 170 * m.x.extract_values()[(i, j)] * math.e ** (0.17 * w[i][j]) 
#         print('Penalty:', penalty)
#         return penalty

#     def cities_covered_rule(m, i, j):
#         # return the expression for the constraint for (i, j)
#         print('city:', m.c[i][j])
#         if m.c[i][j] == 1:
#             counter = 0
#             for x in m.I:
#                 for y in m.J:
#                     if m.x.extract_values()[(x, y)] == 1 and euclid_distance(i, x, j, y) <= m.rs:
#                         counter += 1
#             print('counter:', counter)
#             if counter < 1:
#                 print('infeasible')
#                 return Constraint.Infeasible
#         print('feasible')
#         return Constraint.Feasible

#     model = pyo.AbstractModel()

#     model.I = pyo.RangeSet(0, instance.D - 1, 1)
#     model.J = pyo.RangeSet(0, instance.D - 1, 1)
#     # model.I  = pyo.Set(initialize=range(instance.D))
#     # model.J  = pyo.Set(initialize=range(instance.D))
#     # model.IJ = pyo.Set(within=model.I * model.J, initialize =[(i, j) for i in range(instance.D) for j in range(instance.D)])

#     # VARIABLES
#     # m.x is 1 if tower at (i, j)
#     model.x = pyo.Var(model.I, model.J, domain=pyo.Binary, initialize=1)
#     # model.x = pyo.Var(model.IJ, domain=pyo.Binary)

#     # PARAMETERS
#     model.rs = instance.R_s
#     model.rp = instance.R_p
#     # m.c is 2D array with entry 1 if city at (i, j)
#     model.c = generate_cities(instance)

#     # OBJECTIVE
#     model.OBJ = pyo.Objective(rule=obj_expression, sense=pyo.minimize)
    
#     # CONSTRAINTS
#     model.citiesConstraint = pyo.Constraint(model.I, model.J, rule=cities_covered_rule)

#     inst = model.create_instance()
#     results = SolverFactory('mindtpy')
#     results.solve(inst, tee=True)
#     print(results)

#     # results.display()
#     # results.print()

#     # m = pyo.build_model(model)
#     # results = SolverFactory('glpk').solve(m)

#     # results = SolverFactory('mindtpy').solve(model, mip_solver='glpk', nlp_solver='ipopt', tee=True, iteration_limit=1000000)


SOLVERS: Dict[str, Callable[[Instance], Solution]] = {
    "naive": solve_naive,
    # "cococo": solve_minlp,
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
