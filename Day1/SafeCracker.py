from util.day_initializer import DayInitializer


class SafeCracker(DayInitializer):


    def __init__(self):
        super().__init__('input1.txt')
        self.password_method = '0x434C49434B'

    def run_cracker(self, file, password_method=None, debug=False):
        zero_count = self.crack(file, password_method=password_method, debug=debug)
        print(f"Zero count: {zero_count}")

    def run_part1(self):
        self.run_simple_test()
        self.run_cracker(self.file_path)

    def run_part2(self):
        self.run_password_method_test()
        self.run_cracker(self.file_path, self.password_method)

    def run_simple_test(self):
        zero_count = self.crack('test.txt', debug=True)
        print(f"Zero count: {zero_count} == 3")

    def run_password_method_test(self):
        zero_count = self.crack('test.txt', password_method=self.password_method, debug=True)
        print(f"Zero count: {zero_count} == 6")


    def crack(self, file_path, password_method=None, debug=False):
        lines = self.read_file(file_path)
        dial_pointer = 50
        zero_cnt = 0
        for line in lines:
            direction = line[0]
            amt = int(line[1:])
            if debug:
                print(line)
            if password_method:
                dial_pointer, res = self.apply_password(direction, dial_pointer, amt, self.password_method)
            else:
                dial_pointer, res = self.apply_password(direction, dial_pointer, amt)

            zero_cnt += res
            if debug:
                print(dial_pointer)

        return zero_cnt

    def apply_password(self, direction:str, dial_pointer:int, amt:int, method=None):
        if direction == 'L':
            amt = -amt

        cnt = 0
        if method == self.password_method:
            full_revolutions = abs(amt) // 100
            cnt += full_revolutions
            remaining = abs(amt) % 100
            if amt < 0:
                remaining = -remaining
            new_dial = dial_pointer + remaining

            # you need to solve for when d = 0 and it moves in either directions. can't just else it
            if amt > 0:
                if new_dial > 99:
                    cnt += 1
            elif amt < 0 and dial_pointer != 0: # the fact that i did not check if dial_pointer is 0 is the problem
                if new_dial <= 0:
                    cnt += 1
            # if amt < 0 and dial is at 0, we only need to count rotations
            dial_pointer = new_dial % 100
        else:
            dial_pointer += amt
            dial_pointer %= 100
            if dial_pointer == 0:
                cnt = 1

        return dial_pointer, cnt

    def read_file(self, file_path):
        with open(file_path, 'r') as file:
            return file.readlines()

