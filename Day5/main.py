from InventoryManager import InventoryManager
if __name__ == '__main__':

    Manager = InventoryManager('input.txt')
    Manager.run_test()
    Manager.run_part1() # 679. I spent way too long figuring out how to consolidate ranges

    print()