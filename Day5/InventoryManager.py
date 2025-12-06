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

    def run_part1(self, file_path=None):
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

        Huh... what if bucket is only have largest digit but its min range begins at 10^3 or lower. Just doing max
        range on bucket might not work. Might actually just keep a single heap and process it at the end then bin search

        Problem, what is the problem range? 0 - 10 ^ 15?        ooooo
        :param file_path:
        :return:
        '''
        if not file_path:
            file_path = self.file_path
        ingredient_list = self.read_file(file_path)

        # Bucket should keep max digit of current range aka b[5] = [ (1, 10_000), (5432, 54_321), (54321, 98765) ]
        # should i have min_digit bucket and max digit bucket?

        range_bucket = [[] for _ in range(17)] # 0 - 16] assuming max input ranges, no array notation
        # freshness_heap = [] # have it per bucket? Yeah it'll be within the bucket itself
        # only have 182 ranges to process
        # oh oooo smallest range are still in the 10^10 range. ooo

        amount_fresh = 0
        for valid_ranges in ingredient_list:
            item = valid_ranges.strip().split('-')
            if not item[0]: # Empty line before having to begin verification
                self.process_heap(range_bucket)
            elif len(item) > 1:
                start, end = item
                max_digit = len(end)
                start, end = int(start), int(end)
                current_bucket = range_bucket[max_digit]

                # Process at end or right here? Here would be most optimal but lazy
                heappush(current_bucket, (start, end))
            else:   # begin verification
                if self.is_fresh(int(item[0]), range_bucket):
                    amount_fresh += 1
        print(f'Amount of fresh ingredients {amount_fresh}')

    def process_heap(self, range_bucket:list[list[tuple[int, int]]]):
        '''
        Problem. What if our id is digit len 3 but nothing or invalid range is in that bucket
        and some max bucket later actually contain a starting min < id.
        id = 213;     bucket = [ 0, (50-99), [111-211, 214-999], 0, 0, (212 - 222_222) <- valid]
        :param range_bucket:
        :return:
        '''
        for idx, bucket in enumerate(range_bucket):
            if not bucket:
                continue
            # heapify(bucket)
            smallest = bucket[0][0]
            largest = bucket[0][1]
            # i need some way to accumulate this
            res = []
            while bucket:   # ranges start and end can be the same number
                start, end = heappop(bucket)
                smallest = min(smallest, start)
                largest = max(largest, end)
                if not bucket:
                    res += [(start, end)]
                    break
                next_start, next_end = bucket[0]
                if next_start <= end:
                    # Combine
                    end = max(end, next_end)
                    heappop(bucket)
                    heappush(bucket, (start, end))
                else:
                    res += [(start, end)]
            print(f'Bucket {idx} smallest {smallest} largest {largest}')
            range_bucket[idx] = res

    def is_fresh(self, ingredient_id, range_bucket: list[list[tuple[int, int]]]):
        '''
        Binary sort on range bucket till you find valid ranges
        :param ingredient_id:
        :param range_bucket:
        :return:
        '''
        max_digit = len(str(ingredient_id))
        bucket = range_bucket[max_digit]
        if not bucket:
            return False
        start, end = 0, len(bucket) - 1
        while start <= end:
            mid = start + (end - start) // 2
            start_range, end_range = bucket[mid]
            if start_range <= ingredient_id <= end_range:
                return True
            elif ingredient_id < start_range:
                end = mid - 1
            else:
                start = mid + 1
        return False

        pass
