from util import fn_time
from paper_roll_island import PaperRoller

'''
Problem size 140 x 140
'''

if __name__ == "__main__":
    Collector = PaperRoller()
    # # ~ .2 ms
    # fn_time(Collector.run_test)()
    #
    # # ~ 33.3 ms
    fn_time(Collector.run_collection)(True)  #Total paper rolls:1523 but by god that feels kinda slow

    # fn_time(Collector.run_test)(True)
    Collector.run_collection(True, run_part2=True)  # Total paper = 9290 good
