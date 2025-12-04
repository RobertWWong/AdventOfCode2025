from .web_scraper import WebScraper
from time import perf_counter


def fn_time(func):
    def wrapper(*args, **kwargs):
        start = perf_counter()
        result = func(*args, **kwargs)
        end = perf_counter()
        print(f"Time taken: {end - start:.6f} seconds")
        return result
    return wrapper