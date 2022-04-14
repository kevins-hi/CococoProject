"""Generates instance inputs of small, medium, and large sizes.

Modify this file to generate your own problem instances.

For usage, run `python3 generate.py --help`.
"""

import argparse
from pathlib import Path
from typing import Callable, Dict

from instance import Instance
from size import Size
from point import Point
from file_wrappers import StdoutFileWrapper


def make_small_instance() -> Instance:
    """Creates a small problem instance.

    Size.SMALL.instance() handles setting instance constants. Your task is to
    specify which cities are in the instance by constructing Point() objects,
    and add them to the cities array. The skeleton will check that the instance
    is valid.
    """
    cities = []
    pairs = "12 20 19 9 20 22 19 18 8 9 22 22 8 18 14 19 13 12 18 17 22 11 12 8 22 16 21 12 17 15 18 10 11 13 9 15 12 9 15 9 11 15 9 21 12 14 21 8 9 10 19 20 13 22 17 9 8 14 15 8 22 15 19 10 17 17 15 17 15 22 10 22 9 17 11 12 13 20 16 11 9 20 9 9 12 12 14 10 16 14 21 14 15 18 0 0 30 30 0 7"
    nums_list = pairs.split(" ")
    for i in range(0, len(nums_list) - 1, 2):
        cities.append(Point(nums_list[i], nums_list[i + 1]))
    return Size.SMALL.instance(cities)


def make_medium_instance() -> Instance:
    """Creates a medium problem instance.

    Size.MEDIUM.instance() handles setting instance constants. Your task is to
    specify which cities are in the instance by constructing Point() objects,
    and add them to the cities array. The skeleton will check that the instance
    is valid.
    """
    cities = []
    pairs = "2 19 17 24 19 1 30 1 0 29 41 13 0 44 17 29 25 41 50 21 49 45 34 50 39 43 24 26 27 15 50 48 22 33 33 44 31 14 43 1 42 13 19 3 19 50 4 12 21 16 33 45 16 21 17 20 7 29 40 7 47 31 36 21 5 32 32 40 10 3 22 28 6 46 42 12 24 38 12 18 50 17 27 4 9 30 37 18 1 2 24 31 50 19 10 41 35 22 43 48 9 0 20 25 44 19 41 1 15 21 14 11 6 39 26 9 5 8 19 38 46 15 40 14 16 26 5 44 17 15 21 40 16 10 6 14 26 13 5 5 27 17 28 36 17 4 34 43 47 0 43 25 32 49 17 5 46 16 20 40 36 2 39 5 7 5 32 44 17 44 2 17 12 21 11 33 20 39 47 5 11 50 36 44 35 45 9 14 46 46 22 21 21 15"
    nums_list = pairs.split(" ")
    for i in range(0, len(nums_list) - 1, 2):
        cities.append(Point(nums_list[i], nums_list[i + 1]))
    return Size.MEDIUM.instance(cities)


def make_large_instance() -> Instance:
    """Creates a large problem instance.

    Size.LARGE.instance() handles setting instance constants. Your task is to
    specify which cities are in the instance by constructing Point() objects,
    and add them to the cities array. The skeleton will check that the instance
    is valid.
    """
    cities = []
    pairs = "7 94 49 6 73 26 24 32 36 3 14 1 97 39 22 28 43 88 46 74 75 9 100 28 78 97 2 24 26 30 33 61 34 16 49 83 23 56 37 42 96 70 14 84 40 92 82 48 9 71 6 91 41 76 20 10 43 90 47 62 44 25 77 36 71 82 77 88 85 19 57 25 37 23 78 95 63 19 60 84 36 91 93 36 97 47 54 1 4 86 9 56 20 49 21 16 97 8 54 57 53 87 24 19 66 41 83 25 31 14 85 63 93 93 98 52 37 82 61 41 28 15 62 67 70 17 88 57 0 25 84 50 14 99 28 100 25 44 12 62 89 64 65 25 2 79 79 38 21 98 22 61 40 15 27 88 29 58 77 64 41 18 56 31 30 52 66 27 72 100 67 7 70 8 28 65 58 81 4 6 13 14 16 33 76 69 92 4 12 58 61 71 80 11 92 45 50 31 48 47 76 75 55 31 3 47 57 84 2 83 15 89 58 36 57 73 88 26 59 33 98 55 12 31 65 15 95 0 89 63 16 51 88 36 68 47 58 23 35 9 97 77 95 27 98 76 62 50 48 22 17 36 13 57 31 57 70 20 52 51 67 63 19 62 58 70 76 91 16 71 17 41 30 66 53 33 0 18 26 73 41 85 93 99 28 75 85 29 100 9 17 4 14 96 41 73 24 26 88 64 6 38 0 89 58 16 14 81 35 0 14 49 1 16 25 88 19 98 36 97 7 38 67 40 79 46 98 47 58 80 91 87 55 98 37 26 10 8 79 60 93 54 70 58 61 39 3 81 68 25 11 9 24 71 98 79 63 99 16 34 46 0 87 23 89 99 3 44 75 60 16 4 53 16 20 63 97 10 44 29 76 51 38 24 59 13 84 13 20 32 87 43"
    nums_list = pairs.split(" ")
    for i in range(0, len(nums_list) - 1, 2):
        cities.append(Point(nums_list[i], nums_list[i + 1]))
    return Size.LARGE.instance(cities)


# You shouldn't need to modify anything below this line.
SMALL = 'small'
MEDIUM = 'medium'
LARGE = 'large'

SIZE_STR_TO_GENERATE: Dict[str, Callable[[], Instance]] = {
    SMALL: make_small_instance,
    MEDIUM: make_medium_instance,
    LARGE: make_large_instance,
}

SIZE_STR_TO_SIZE: Dict[str, Size] = {
    SMALL: Size.SMALL,
    MEDIUM: Size.MEDIUM,
    LARGE: Size.LARGE,
}

def outfile(args, size: str):
    if args.output_dir == "-":
        return StdoutFileWrapper()

    return (Path(args.output_dir) / f"{size}.in").open("w")


def main(args):
    for size, generate in SIZE_STR_TO_GENERATE.items():
        if size not in args.size:
            continue

        with outfile(args, size) as f:
            instance = generate()
            assert instance.valid(), f"{size.upper()} instance was not valid."
            assert SIZE_STR_TO_SIZE[size].instance_has_size(instance), \
                f"{size.upper()} instance did not meet size requirements."
            print(f"# {size.upper()} instance.", file=f)
            instance.serialize(f)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate problem instances.")
    parser.add_argument("output_dir", type=str, help="The output directory to "
                        "write generated files to. Use - for stdout.")
    parser.add_argument("--size", action='append', type=str,
                        help="The input sizes to generate. Defaults to "
                        "[small, medium, large].",
                        default=None,
                        choices=[SMALL, MEDIUM, LARGE])
    # action='append' with a default value appends new flags to the default,
    # instead of creating a new list. https://bugs.python.org/issue16399
    args = parser.parse_args()
    if args.size is None:
        args.size = [SMALL, MEDIUM, LARGE]
    main(args)
