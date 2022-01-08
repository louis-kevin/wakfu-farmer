import time
from random import random


def add_randomness(n, random_factor_size=None):
    """Returns n with randomness
    Parameters:
        n (int): A decimal integer
        random_factor_size (int): The maximum value+- of randomness that will be
            added to n
    Returns:
        int: n with randomness
    """

    if random_factor_size is None:
        randomness_percentage = 0.1
        random_factor_size = randomness_percentage * n

    random_factor = 2 * random() * random_factor_size
    if random_factor > 5:
        random_factor = 5
    without_average_random_factor = n - random_factor_size
    randomized_n = int(without_average_random_factor + random_factor)
    return int(randomized_n)


def timeDiff(method):
    start = time.time()
    method()
    end = time.time()
    result_time = end - start
    print('Finished in ' + str(result_time) + 's')
