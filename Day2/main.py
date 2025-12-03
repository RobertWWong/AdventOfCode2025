import time
from IdChecker import IDChecker
if __name__ == '__main__':

    Checker = IDChecker()
    t1s = time.perf_counter()
    Checker.run_part_1()
    t1e = time.perf_counter()
    print(f'part 1 took {t1e-t1s} seconds\n')

    t2s = time.perf_counter()
    Checker.run_part_2()
    t2e = time.perf_counter()
    print(f'part 2 took {t2e-t2s} seconds\n')   # surprisingly... this is the fastest by 3 x previous solution

    t3s = time.perf_counter()
    Checker.use_regex()
    t4e = time.perf_counter()
    print(f'part 2 regex took {t4e-t3s} seconds')