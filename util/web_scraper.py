from pathlib import Path
import requests
import os

class WebScraper:

    def __init__(self):
        pass

    def retrieve_input(self, day:int):
        '''
        Create new day repo and retrieve problem input based on day.
        :param day:
        :return:
        '''
        directory = f"Day{day}"

        Path(directory).mkdir(parents=True, exist_ok=True)

        # Download input file
        url = f"https://adventofcode.com/2025/day/{day}/input"

        response = requests.get(url)

        # Save to input.txt in the new directory
        input_path = os.path.join(directory, "input.txt")
        with open(input_path, "w") as f:
            f.write(response.text)
