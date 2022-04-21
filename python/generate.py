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
    pairs = "17 11 22 12 13 14 15 19 18 11 21 9 11 18 22 17 21 12 22 13 19 9 16 15 22 8 17 10 11 14 10 18 20 11 9 20 19 18 14 14 12 22 11 17 0 0 29 29 0 7"
    nums_list = pairs.split(" ")
    for i in range(0, len(nums_list) - 1, 2):
        cities.append(Point(int(nums_list[i]), int(nums_list[i + 1])))
    return Size.SMALL.instance(cities)


def make_medium_instance() -> Instance:
    """Creates a medium problem instance.

    Size.MEDIUM.instance() handles setting instance constants. Your task is to
    specify which cities are in the instance by constructing Point() objects,
    and add them to the cities array. The skeleton will check that the instance
    is valid.
    """
    cities = []
    pairs = "34 49 43 30 24 35 49 42 11 20 40 9 0 25 46 11 41 22 40 12 27 46 25 10 26 17 19 26 26 12 18 8 46 32 27 16 43 23 41 28 18 39 28 15 48 38 3 9 7 40 24 14 8 44 4 17 41 11 4 10 33 22 6 38 39 33 1 31 12 26 47 21 40 26 12 48 35 45 47 19 11 26 27 21 34 28 28 20 2 40 9 18 39 29 16 27 22 9 25 40 5 41 7 17 0 27 16 11"
    nums_list = pairs.split(" ")
    for i in range(0, len(nums_list) - 1, 2):
        cities.append(Point(int(nums_list[i]), int(nums_list[i + 1])))
    return Size.MEDIUM.instance(cities)


def make_large_instance() -> Instance:
    """Creates a large problem instance.

    Size.LARGE.instance() handles setting instance constants. Your task is to
    specify which cities are in the instance by constructing Point() objects,
    and add them to the cities array. The skeleton will check that the instance
    is valid.
    """
    cities = []
    pairs = "55 40 8 84 38 9 10 73 34 56 88 29 74 93 55 67 58 56 78 8 10 20 2 19 32 98 53 21 9 11 49 74 60 73 47 90 17 92 66 83 64 40 67 48 5 18 21 38 96 23 43 89 72 16 86 12 54 91 38 80 6 8 5 78 74 82 0 16 80 84 94 73 65 33 70 26 85 50 31 79 91 88 7 45 91 13 86 15 80 60 54 30 77 70 78 16 15 96 94 12 32 72 29 24 51 52 79 92 63 50 24 18 7 73 39 30 82 19 90 9 3 48 49 38 39 25 96 65 80 97 74 12 69 12 73 26 4 43 39 49 56 87 9 80 83 43 97 58 41 45 29 21 36 93 97 84 46 52 12 24 26 75 73 54 39 89 26 68 89 89 64 96 61 75 52 75 58 65 60 11 39 9 86 30 65 64 22 60 73 55 15 30 73 36 25 12 83 38 30 67 73 39 16 24 50 22 71 74 66 11 10 39 52 25 33 40 26 78 93 19 66 10 27 74 93 91 36 71 16 63 17 83 88 61 44 20 18 65 98 59 16 31 63 49 50 19 98 84 85 44 4 84 85 88 78 18 59 80 5 86 60 32 22 40 69 8 61 26 2 31 59 77 45 80 96 90 68 68 25 29 40 25 61 45 50 20 11 25 75 38 79 30 83 58 94 28 49 43 14 75 40 87 90 72 63 71 35 72 74 48 11 76 5 58 24 62 85 58 29 61 64 50 80 47 58 69 68 26 97 23 10 94 9 41 41 14 20 32 96 51 63 78 32 90 9 97 85 42 50 75 95 59 88 92 42 37 25 62 98 81 95 53 66 75 61 49 86 26 83 39 35 82 74 96 6 55 30 29 82 74 69 23 26 93 62 78 73 69 57 74 65 10 28 51 96 35 77 9 83 92 42 95 2 60"
    nums_list = pairs.split(" ")
    for i in range(0, len(nums_list) - 1, 2):
        cities.append(Point(int(nums_list[i]), int(nums_list[i + 1])))
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
