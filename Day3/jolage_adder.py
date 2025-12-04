from util.day_initializer import DayInitializer


class JoltageAdder(DayInitializer):
    '''
    Part1: Given an array of strings ints ('12345'), find the largest 2 digit value in one pass.
    Sum up all those largest value at the end of the array.

    Smart way would to keep an array of largest number seen past this index for left and right side.

    Part 2 is recursion with memoizations
    '''

    def __init__(self, file_path=None):
        super().__init__(file_path if file_path else "input.txt")


    def read_file(self, file_path=None) -> list[str]:
        if not file_path:
            file_path = self.file_path
        with open(file_path, "r") as f:
            return [line.strip() for line in f]

    def run_test_1(self) -> int:
        joltage_list = self.read_file("test.txt")
        # res = self.process_joltage(joltage_list)
        # res = self.brute_force(joltage_list)
        res = self.process_jolt_largest_seen(joltage_list)

        return res

    def run_part_1(self) -> int:
        joltage_list = self.read_file()
        # res = self.process_joltage(joltage_list)
        # res = self.brute_force(joltage_list)
        res = self.process_jolt_largest_seen(joltage_list)
        return res

    def run_part_2(self):
        joltage_list = self.read_file()
        res = self.process_joltage_memoize_p2(joltage_list)
        return res

    def brute_force(self, joltage_list:list[str]):
        '''
        I could do better :(
        :param joltage_list:
        :return:
        '''
        total = 0
        for jolt in joltage_list:
            max_num = 0
            for i in range(len(jolt) - 1):
                for j in range(i + 1, len(jolt)):
                    d1 = int(jolt[i])
                    d2 = int(jolt[j])
                    num = int(f"{d1}{d2}")

                    max_num = max(num, max_num)
            total += max_num
        print(total)
        return total

    def process_jolt_largest_seen(self, joltage_list:list[str]):
        '''
        Thanks sum.
        You should keep track of the largest number you have seen on the left and right side of this index.
        This will allow you to know  what the next largest digits could choose given your current index and + 1
        :param joltage_list:
        :return:
        '''
        total = 0
        jolt_len = len(joltage_list[0])
        for jolt in joltage_list:
            big_left = ['0'] * jolt_len
            big_right = ['0'] * jolt_len
            big_left[0] = jolt[0]
            big_right[-1] = jolt[-1]
            for idx in range(len(jolt) - 2, -1, -1):
                rval = jolt[idx]
                r_right = big_right[idx + 1]
                big_right[idx] = max(rval, r_right)
            for idx in range(1, len(jolt)):
                lval = jolt[idx]
                l_left = big_left[idx - 1]
                big_left[idx] = max(lval, l_left)
            largest = 0

            for idx in range(len(jolt) - 1):
                num = int(f"{big_left[idx]}{big_right[idx + 1]}")
                largest = max(largest, num)
            # print(f'{big_left}\n{big_right}\nLargest is: {largest}')

            total += largest

        print(total)
        return total

    def process_joltage_iterative(self, joltage_list:list[str]):
        '''
        Things you need to process.
        9 111 9 (both ends)
        2 5565444   (somewhere middle)
        2 111 911 9  (right half)
        175 3333    (left half)

        Nah my iterative tracking skills are wack.
        :param joltage_list:
        :return:
        '''
        output = 0
        res = []
        for jolt in joltage_list:
            d1 = d2 = 0 # track largest digit

            # for d1_idx, d1_val in enumerate(jolt):
            for d1_idx in range(len(jolt) - 1):
                d1_val = jolt[d1_idx]
                d1_val = int(d1_val)

                # should stop once we land on 9 and finished checking for other digits
                # add this at the end
                # if d1_idx == len(jolt) - 1: # we've reached the end. Should just truncate it tbh
                #     break
                if d1 < d1_val:
                    d1 = d1_val
                elif d1 > d1_val:
                    continue

                # for d2_idx, d2_val in enumerate(jolt[d1_idx + 1:]):
                for d2_idx in range(d1_idx + 1, len(jolt)):
                    d2_val = jolt[d2_idx]
                    d2_val = int(d2_val)
                    # need to deal with 8 1111 9 888    have to reset d2 if d1 > d2 at that point
                    if d1_idx == d2_idx + 1:    # how to deal with 9888889?
                        d2 = 0
                        continue
                    if d1_idx == d2_idx - 1:
                        if d1 >= d2:
                            d2 = d2_val
                        else:
                            d2 = max(d2, d2_val)
                        continue

                    if d2 < d2_val:
                        d2 = d2_val

                    if d2 > d1:
                        break
                if d1 == 9:
                    break
            num = int(f"{d1}{d2}")
            res.append(num)
            output += num
        # print(res)
        print(output)
        return output

    def process_joltage_memoize_p2(self, joltage_list):
        '''
        Will have to recursively process each jolt, choosing to take each digit or not, then memoize the results.
        Somehow.
        Need to figure out how to create cutoff to stop processing once past a certain amount. Somehow.
        This is going to be O(N * 2^12) kinda work. It's disgusting.
        :param joltage_list:
        :return:
        '''
        # todo come back and finish later
        pass