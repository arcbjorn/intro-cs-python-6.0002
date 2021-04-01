###########################
# 6.0002 Problem Set 1a: Space Cows
# Name: Oleg Luganskiy <arcbjorn>
# Collaborators: None
# Time spent: 10101000110000 sec

from ps1_partition import get_partitions
import time
from collections import OrderedDict
from pprint import pprint
from typing import Callable, Dict, List, Tuple


Cow = Tuple[str, int]
Cows = Dict[str, int]
Trips = List[List[str]]
Transport = Callable[[Cows], Trips]

# ================================
# Part A: Transporting Space Cows
# ================================

# Problem 1


def load_cows(filename) -> Cows:
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """
    def parse_line(line: str) -> Cows:
        name, weight = line.split(',')
        return name, int(weight)

    with open(filename) as file:
        return dict(map(parse_line, file))

# Problem 2


def greedy_cow_transport(cows: Cows, limit: int = 10) -> Trips:
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)

    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    trips = []

    cows_copy = cows.copy()

    # sort by weight, descending
    cows_sorted = OrderedDict(
        sorted(cows_copy.items(), reverse=True, key=lambda x: x[1]))
    total_weight = 0

    cow_number = 0

    while len(cows_sorted) > 0:
        total_weight = 0
        trips.append([])
        for (cow, weight) in cows_sorted.copy().items():
            # check if weight of each cow + current total < limit
            if total_weight + weight <= limit:
                trips[cow_number].append(cow)
                total_weight = total_weight + weight
                # remove the cow from sorted list
                del cows_sorted[cow]
        cow_number += 1

    return trips

# Problem 3


def is_valid(cows: Cows, limit: int, trips_allocation: Trips) -> bool:
    """
    Check if trips allocation is valid
    """
    return all(
        sum(map(cows.get, trip)) <= limit
        for trip in trips_allocation
    )


def brute_force_cow_transport(cows: Cows, limit: int = 10) -> Trips:
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips 
        Use the given get_partitions function in ps1_partition.py to help you!
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)

    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """

    valid_trip_allocations = (
        allocation
        for allocation in get_partitions(cows)
        if is_valid(cows, limit, allocation)
    )
    return min(valid_trip_allocations, key=len)

# Problem 4


def record_time(func: Transport, arg: Cows, algorithm_name: str) -> None:
    """
    Give the time it takes to print data
    """

    start = time.time()
    pprint(func(arg))
    end = time.time()
    print(f'{algorithm_name}: {end - start:.5f} seconds', '\n')


def compare_cow_transport_algorithms(cow_file: str) -> None:
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.

    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """

    cows = load_cows(cow_file)

    record_time(greedy_cow_transport, cows, 'Greedy')
    record_time(brute_force_cow_transport, cows, 'Brute force')


if __name__ == '__main__':
    cow_file = "ps1_cow_data.txt"

    # pprint(load_cows(cow_file))

    # pprint(greedy_cow_transport(load_cows(cow_file)))

    # pprint(brute_force_cow_transport(load_cows(cow_file)))

    compare_cow_transport_algorithms(cow_file)
