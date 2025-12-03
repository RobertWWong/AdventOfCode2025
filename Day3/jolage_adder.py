
class JoltageAdder:
    '''
    Part1: Given an array of strings ints ('12345'), find the largest 2 digit value in one pass.
    Sum up all those largest value at the end of the array
    '''

    def __init__(self, file_path=None):
        self.file_path = file_path if file_path else "input.txt"


    def read_file(self, file_path=None) -> list[str]:
        if file_path:
            self.file_path = file_path
        with open(self.file_path, "r") as f:
            return [line.strip() for line in f]

    def run_test_1(self) -> int:
        joltage_list = self.read_file("test.txt")
        res = self.process_joltage(joltage_list)
        return res

    def run_part_1(self) -> int:
        joltage_list = self.read_file()
        res = self.process_joltage(joltage_list)
        return res

    def process_joltage(self, joltage_list:list[str]):
        '''
        Things you need to process.
        9 111 9 (both ends)
        2 5565444   (somewhere middle)
        2 111 911 9  (right half)
        175 3333    (left half)
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