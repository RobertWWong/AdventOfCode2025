from InventoryManager import InventoryManager
if __name__ == '__main__':

    Manager = InventoryManager('input.txt')
    # Manager.run_test()
    # Manager.collect_ingredients()  # 679. I spent way too long figuring out how to consolidate ranges

    Manager.run_test(True)
    Manager.collect_ingredients(part_2=True)    # 358155203664116 yippie
    print()