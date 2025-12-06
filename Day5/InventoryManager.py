from util import DayInitializer
from heapq import heappush, heappop, heapify
class InventoryManager(DayInitializer):
    def __init__(self, file_path: str = 'input.txt'):
        super().__init__(file_path)


    def run_test(self, part_2=False):
        file_path = 'test.txt'
        if part_2:
            self.run_part2(file_path)
        else:
            self.run_part1(file_path)

    def run_part1(self, file_path):
        '''
        First part is to parse and record valid fresh int ranges.
        Then we must determine if the item is fresh or not.
        Reminds me of interval meeting room. Similar logic to have a min heap, process each item range, update
        and combine valid ranges when possible.
        Then go through inventory to see what hasn't spoiled.

        I might want to actually sort this in a bucket, where bucket idx is length of the digit. But how do
        i maintain start = 0 to end = 10^15 in array notation? Keep a map as well to map valid ranges?
        Space: O(15 * M -> amount of ranges)

        Bucket = [ [int...], [...] ]
        RangeRecords = { (start, end) : (bucket_idx, bucket_idx) }  -> hmm almost there. Should actually repr digit len

        updated:
        ingredient_id -> check against bucket -> bucket will contain list of all ranges that lies within that digit.
        -> binary search across ranges until valid range is found or not at all.

        Problem, what is the problem range? 0 - 10 ^ 15?        ooooo
        :param file_path:
        :return:
        '''
        ingredient_list = self.read_file(file_path)
        idx = 0
        # Bucket should keep max digit of current range aka b[5] = [ (1, 10_000), (5432, 54_321), (54321, 98765) ]
        range_bucket = [[] for _ in range(16)] # 0 - 15] assuming max input ranges
        freshness_heap = [] # have it per bucket?

        for valid_ranges in ingredient_list:
            item = valid_ranges.strip().split('-')
            if not item[0]:
                self.process_heap(freshness_heap)
                continue
            elif len(item) > 1:
                start, end = item
                start, end = int(start), int(end)
                freshness_heap.append((start, end)) # Process at end or right here?
            else:   # begin checking
                pass
            idx += 1
            print(f'Ingredient {idx} valid ranges: {valid_ranges}')

    def process_heap(self, freshness_heap: list[tuple[int, int]]):
        pass

    def is_fresh(self, ingredient_id, freshness_heap):
        pass
