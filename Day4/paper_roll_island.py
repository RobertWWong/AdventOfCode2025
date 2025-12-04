from util.day_initializer import DayInitializer


class PaperRoller(DayInitializer):
    
    def __init__(self, file_path: str = 'input.txt'):
        super().__init__(file_path)
