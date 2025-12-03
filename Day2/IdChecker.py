from mako.util import read_file


class IDChecker:
    '''
        Didn't understand problem prompt at first. You are to go through
        a range of numbers starting from the first id and ending at the second (all inclusive).
        You must find all repeating subsequence where only some sequence of digits are
        repeated twice.

        Edge cases: odd length id are not considered.
        i.e. 131 (no dupes here), 13131 (again, can't make a dupe of this)

        This is assumed to be half of the length of the total digit that is to be considered for
        validation.
        i.e. 123123 is a duplicate. 123 repeats twice
        It appears we do not count 23 in 123123 to be a duplicate while validating

        for a 2 digit range, from 0 - 100, there are 9 dupes possible: 11,22,33 .. 99 (1-9) 9 total dupes
        so for even digit range, we now must consider half dupes:
        (1000) -> 1212, 1313,1414 .. 1919 (2-9) 8 total dupes

        However, odd length digit ranges past 3 yield no dupes
        (10000) -> can't be dupe if both halves are of diff length
        So it can be said odd lengthed range can't contain duplicates

        so 6 digits includes dupes of prev even range, a 3rd digit an order of magnitude more dupes:
        (100 000) -> (112 -> 119) 8 dupes * (range 2-9) 64 more dupes
        so
        111... = 9 dupes
        112..119 = 8 dupes per last 2 digit range
            -> 112..199 = 8 * 8 = 64 for range(100_000 to 199_999)
        total dupes is 64 + 9 = 75
        
        no, this is too iterative. Only generate valid halves of an id based on the amount of digits
        you are allowed to start with. And only start on digit divisible by 2.
        
    '''
    def __init__(self, file_path="input1.txt"):
        self.file_path = file_path


    def run_test(self, file_path=None, part_2=False):
        if not file_path:
            file_path = 'test.txt'
        res = self.check_ids(file_path)

    def run_part_1(self):
        t1 = self.run_test()
        print(f'expected: 1227775554 got:{t1}')

        self.check_ids(self.file_path)
    
    def run_part_2(self):
        t2 = self.run_test(part_2=True)
        print(f'expected: 1227775554 got:{t2}')
        self.check_ids(self.file_path, True)

    def check_ids(self, file_path, part_2=False):
        res = self.process_ids(file_path, part_2)
        total = self.sum_invalid_sequences(res)
        print(total)
        return total

    def read_file(self, file_path):
        with open(file_path, 'r') as file:
            return file.read().split(',')

    def process_ids(self, file_path:str=None, part_2=False) -> list[int]:
        if not file_path:
            file_path = self.file_path
        ids = self.read_file(file_path)
        dupe_list = []
        for id_tag in ids:
            start, end = id_tag.split('-')
            if not part_2:
                self.validate_id_range(start, end, dupe_list)
            else:
                self.valid_twice(start, end, dupe_list)
        return dupe_list
    
    def valid_twice(self,begin:str, end:str, dupe_list:list[int]):
        '''
        Now duplicates are considered any numbers that are repeated more than once.
        Now we do repeating subsequences. is it even still subsequences?
        And now, we consider odd lengthed digits as valid dupes aka 111 is valid

        :param begin:
        :param end:
        :param dupe_list:
        :return:
        '''
        min_num = len(begin)
        max_num = len(end)

        begin = int(begin)
        end = int(end)
        number_ranges = range(min_num, max_num+1)

        return 
    
    def validate_id_range(self, begin:str, end:str, dupe_list:list[int]) -> list[int]:
        '''
        Given number ranges, generate all possible duplicates.
        We'll only generate valid numbers for each given half.
        The final number is always of even digit length.
        :param begin
        :param end
        :param dupe_list
        :return:
        '''
        min_num = len(begin)
        max_num = len(end)

        begin = int(begin)
        end = int(end)
        number_ranges = range(min_num, max_num+1)
        for digit_range in number_ranges:   #O(N)   based on diff between max and min digit length
            if digit_range % 2 != 0:
                continue
            
            # Only valid dupes start with an even amount of digits
            half_num = digit_range // 2
            low = 10**(half_num - 1)
            high = 10**half_num

            # We now must generate duplicates so that the first half = second half within the range
            # start 100,000 , end with 150,000 -> 6 digits 
            # we'll generate valid halves of the id that are within the actual boundaries
            for n in range(low, high):  # number is always half of N, so range is log2(n) or is this constant?
                num = int(str(n) + str(n))  
                if begin <= num <= end:
                    dupe_list.append(num)
        return dupe_list
    
    def sum_invalid_sequences(self, ids:list[int]) -> int:
        sum = 0
        for id in ids:
            sum += id
        return sum