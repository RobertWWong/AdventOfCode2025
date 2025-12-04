from collections import Counter

from mako.util import read_file
from util.day_initializer import DayInitializer


class IDChecker(DayInitializer):
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
        super().__init__(file_path)

    def use_regex(self):
        res = self.read_file(self.file_path)
        intervals = []
        for i in res:
            start, end = i.split('-')
            start = int(start)
            end = int(end)
            intervals.append((start, end))


        dupes = self.the_easy_solution(intervals)
        print(sum(dupes))



    def the_easy_solution(self, intervals:["first_id-second_id"]):
        '''
        One problem. Slows as mud. About 10x slower
        :param intervals:
        :return:
        '''
        import re
        invalid_patterns = set()
        invalid_numbers = set()
        pattern = r'(.+?)\1$'

        part2_pattern = r'(.+?)\1+$'    # don't check the set when using this

        repeating_pattern = re.compile(pattern)
        # repeating_pattern = re.compile(part2_pattern)

        for interval in intervals:
            for num in range(interval[0], interval[1] + 1):
                repeats = repeating_pattern.match(str(num))
                if repeats and not repeats.group(1) in invalid_patterns:
                # if repeats:
                    invalid_patterns.add(repeats.group(1))
                    invalid_numbers.add(num)
        return [i for i in invalid_numbers]

    def run_test(self, file_path=None, part_2=False):
        if not file_path:
            file_path = 'test.txt'
        res = self.check_ids(file_path, part_2=part_2)
        return res

    def run_part_1(self):
        t1 = self.run_test()
        print(f'expected: 1227775554 got:{t1}')

        self.check_ids(self.file_path)
    
    def run_part_2(self):
        t2 = self.run_test(part_2=True)
        print(f'expected: 4174379265 got:{t2}    {t2 == 4174379265}')
        self.check_ids(self.file_path, True)
    def run_custom(self):
        # Sub 800ms
        self.check_ids('test_custom.txt')   #let's find sum from 1 up to one digit place less of max int size

    def check_ids(self, file_path, part_2=False):
        res = self.process_ids(file_path, part_2)
        total = self.sum_invalid_sequences(res)
        print(total, 'is this the right answer? ', total == 48778605167)
        return total

    def read_file(self, file_path):
        with open(file_path, 'r') as file:
            return file.read().split(',')

    def check_num_ranges(self):
        # seems num range is between 10^0 and 10^10
        res = self.read_file(self.file_path)
        num_space = {}
        counter = Counter()
        smallest_start = largest_start = None
        smallest_end = largest_end = None
        for range in res:
            start, end = range.split('-')
            start = int(start)
            end = int(end)
            num_space[start] = end
            counter[start] += 1
            counter[end] += 1

            if smallest_end is None:
                smallest_end = end
            else:
                smallest_end = min(smallest_end, end)
            if smallest_start is None:
                smallest_start = start
            else:
                smallest_start = min(smallest_start, start)
            if largest_end is None:
                largest_end = end
            else:
                largest_end = max(largest_end, end)
            if largest_start is None:
                largest_start = start
            else:
                largest_start = max(largest_start, start)
        print(f'smallest start: {smallest_start} largest start: {largest_start}')
        print(f'smallest end: {smallest_end} largest end: {largest_end}')
        print()



    def process_ids(self, file_path:str=None, part_2=False) -> list[int]:
        if not file_path:
            file_path = self.file_path
        ids = self.read_file(file_path)
        dupe_list = []
        for id_tag in ids:
            start, end = id_tag.split('-')
            dupe_set = set()
            if not part_2:
                self.validate_id_range(start, end, dupe_list)
            else:
                self.valid_twice(start, end, dupe_list, dupe_set)
        return dupe_list

    # can we memoize this? over-engieneered at this moment
    def valid_twice(self,begin:str, end:str, dupe_list:list[int], dupe_set:set):
        '''
        Now duplicates are considered any numbers that are repeated more than once.
        Now we do repeating subsequences. is it even still subsequences?
        And now, we consider odd lengthed digits as valid dupes aka 111 is valid

        0 - 100 -> 11 .. 99
        0 - 1000 -> ^ + 111 ... 999
        12_12_12 is now valid (12 x 3)
        so can we simply just add previous solution on top of this?
        if digit % 2  == 1:
        then generate valid?
        but how to handle even odds? (12 x 3) or (1234 x 5)
        Where will we get unwanted dupes?
        111 111 -> 11 11 11 (111 x 2 vs 11 x 3 since we can do 2digits x repeating)?
        121 121 -> 12 12 12 (121 x 2 vs 12 x 3) note only start at digit length 6
        121 121 121 -> (121 x 3 and is pattern for 9 digits)

        so a lil possible options of things you could do
        1 x 2 -> 22
        1 x 3 -> 666
        2 x 2 -> 41 41
        1 x 5 -  5555 5
        3 x 2 -> 678 678    note dupe when all digit equal one another (111 111, 11 11 11)
        2 x 3 -> 69 69 69
        7 x 1 -> 777 7 777
        4 x 2 -> 1234 1234 and all its permutations
        2 x 4 -> 22 22 22 22
        3 x 3 -> 123 ... but also need to take care of 1 x 9.       IN FACT I HAVEN'T DONE THAT FOR THE OTHERS
        2 x 5                                                       PROBABLY SHOULD USE A SET TO HANDLE ACTUAL DUPES
        5 x 2
        1 x 10
        Honestly this feels like a common factor up to digit thing or im over complicating it
        I have an idea.
        Take digit, divide by one. the two terms are number of time it'll repeat and by how much
        increase divisor up to half of digit, making sure divisor is a whole number
        max is 10 digits
        digit / divisor = amt to repeat (and whole number)
        divisor is amount of digits to use

        start = 345     end = 65 432
        works in stages
        find all dupes between 0, 99
        then 100 -> 999
        then 1000 -> 9999
        and so on
        for i in range(1 to 10^(divisor - 1)     assume divisor is 4 range is 1 - 10 000

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
        # an awful idea that im dreaming of. Store all possible values between these ranges. I would have to update it
        # number_bucket = {i:set() for i in number_ranges}

        # wow this work jesus this feel sub optimal. I should try that regex solution
        for digits in number_ranges:
            if digits < 2: # only start on valid ranges
                continue
            divisor = 1
            while divisor < digits:
                type_to_check = digits / divisor
                amt_to_repeat = digits // divisor
                if amt_to_repeat != type_to_check:  # we aren't adding half a digit, need your
                    divisor += 1
                    continue
                # still need to do some sort of low and high thing
                # start digit -> divisor?
                high = int(10**(divisor))
                low = int(10**(divisor - 1))
                for i in range(low, high): # divison always >= 2, so start 1 - 10 (exclude 10)
                    num = int(str(i) * amt_to_repeat)   # 1 -> 11, 2 -> 22, 3 -> 33, 4 -> 44

                    # oh yeah this will definitely produce dupe. just use a set at this point
                    if begin <= num <= end and num not in dupe_set:
                        dupe_list.append(num)
                        dupe_set.add(num)
                    elif num > end:
                        break

                divisor += 1


        return dupe_list
    
    def validate_id_range(self, begin:str, end:str, dupe_list:list[int]) -> list[int]:
        '''
        Given number ranges, generate all possible duplicates.
        We'll only generate valid numbers for each given half.
        The final number is always of even digit length.

        works in stages
        find all dupes between 0, 99
        then 100 -> 999
        then 1000 -> 9999
        and so on if num is within range

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