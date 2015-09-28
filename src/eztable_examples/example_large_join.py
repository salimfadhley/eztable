from eztable import Table
import itertools
import random
import cProfile


def do_cprofile(func):
    def profiled_func(*args, **kwargs):
        profile = cProfile.Profile()
        try:
            profile.enable()
            result = func(*args, **kwargs)
            profile.disable()
            return result
        finally:
            profile.print_stats(sort='tottime')
    return profiled_func

STRINGS1 = ['Pikachu', 'Charmander', 'Bulbasaur', 'Oshawatt']
NUMBERS1 = [-1, 0, 2, 3]

ENDLESS = itertools.cycle(STRINGS1)

right = Table([('B', str), ('V', int)])
right.extend(zip(STRINGS1, NUMBERS1))

t = Table([('A', int), ('B', str), ('C', str)])

for i in range(100000):
    rnd = random.choice(STRINGS1)
    cyc = next(ENDLESS)

    t.append([i, rnd, cyc])


@do_cprofile
def main():

    j = t.left_join(
        ('B',),
        other=right
    )


if __name__ == '__main__':
    main()
