from util.day_initializer import DayInitializer


class PaperRoller(DayInitializer):
    '''
    Oh hey, an DFS/BFS Graph problem with restriction. We want to
    find the maximum amount of paper rolls we can grab so long as there
    less than 4 adjacent rolls in the 8 cardinal directions

    I think I had a similar problem on leetcode, Find max island size
    given one tile flip? We're gonna mark the arrays to first identify
    islands then dfs through it oooo maybe not. I'd probably have to
    check if for the current tile how many adjacent rolls are there and
    mark it as valid if < 4 nearby rolls.

    Recursion + memoization?
    '''

    def __init__(self, file_path: str = 'input.txt'):
        super().__init__(file_path)
        self.directions = []  # 8 cardinal directions
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                self.directions.append((i, j))

    def read_file(self, file_path) -> list[list[str]]:
        with open(file_path, 'r') as file:
            return [list(line) for line in file.read().splitlines()]

    def run_test(self, part_2=False):
        file_path = 'test.txt'
        paper_rolls = self.read_file(file_path)
        if part_2:
            max_rolls = self.collect_max_rolls(paper_rolls, part_2)
            print(f'expected: 43 got:{max_rolls}')
        else:
            max_rolls = self.collect_max_rolls(paper_rolls)
            print(f'expected: 13 got:{max_rolls}')


    def run_collection(self, run_test=True, run_part2=False):
        if run_test:
            self.run_test(run_part2)

        paper_rolls = self.read_file(self.file_path)
        max_rolls = self.collect_max_rolls(paper_rolls, run_part2)
        print(f'Total paper rolls:{max_rolls}')

    def collect_max_rolls(self, paper_rolls: list[list[str]], part_2 = False) -> int:
        '''
        Iterate through the 2D NxN matrix and mark current cell with amount of
        surrounding roll before determining if it should be added to the tally.

        Time complexity = O(N x N x (8 direction to check))
        where N is row/col length of the matrix
        :param paper_rolls:
        :return:
        '''
        row_len, col_len = len(paper_rolls), len(paper_rolls[0])
        papers_collected = 0

        def main_logic() -> int:
            papers_collected = 0
            for r in range(row_len):
                for c in range(col_len):
                    adj_count = 0
                    cell = paper_rolls[r][c]
                    if part_2 and cell.isnumeric():  # reset for next process and visual id
                        paper_rolls[r][c] = '.'

                    for nr, nc in self.directions:
                        row = r + nr
                        col = c + nc
                        if self.within_boundary(row, col, paper_rolls, row_len, col_len, part_2):
                            adj_count += 1
                    if adj_count < 4 and cell == '@':
                        paper_rolls[r][c] = str(adj_count)
                        papers_collected += 1
            return papers_collected

        if not part_2:
            papers_collected = main_logic()
        res = -1
        while res != 0: # keep processing until nothing is left
            res = main_logic()
            papers_collected += res

        return papers_collected

    def collect_max_roll_after_removal(self, paper_rolls: list[list[str]]) -> int:
        '''
        Same as collect_max_rolls but now we can work in stages. We are able to
        reprocess the entire matrix after every removal until there no longer
        exist rolls that cannot be removed.

        If reusing old example,
        Time complexity = O(M x (N x N x (8) ) ) ->8 MxN^2
        M is the amount of time it is reprocessed
        N is still length of row/col for matrix

        Wonder if we can can optimize it?

        :param paper_rolls:
        :return:
        '''
        return

    def within_boundary(self, row, col, paper_rolls: list[str], row_len, col_len, part_2=False):
        if 0 <= row < row_len and 0 <= col < col_len:
            cell = paper_rolls[row][col]
            if cell == '.':
                return False
            if part_2:  # do i even need it? no
                if cell.isnumeric():
                    return False

            # For part 1 if @ or number, it's valid
            # For part 2 we'll only consider @ since numbers ARE to be removed in this current iteration
            return True
        return False
