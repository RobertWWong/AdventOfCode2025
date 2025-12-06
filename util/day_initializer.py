class DayInitializer:
    def __init__(self, file_path: str = 'input.txt'):
        self.file_path = file_path

    def read_file(self, file_path) -> list[str]:
        with open(file_path, 'r') as file:
            return file.readlines()
