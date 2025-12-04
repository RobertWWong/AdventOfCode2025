from jolage_adder import JoltageAdder
from util import fn_time


if __name__ == "__main__":
    joltage_adder = JoltageAdder("input.txt")

    # joltage_adder.run_test_1()
    res = fn_time(joltage_adder.run_test_1)()
    # res = joltage_adder.run_part_1()    # 17067 too low, 17144 is right
    res = fn_time(joltage_adder.brute_force)(joltage_adder.read_file()) # .555 sec  O(n*(m^2))
    res = fn_time(joltage_adder.run_part_1)()                           # .012 sec how nice 50x O(n * (3*m)) with 2m space

