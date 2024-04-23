import threading
from queue import Queue
import time


def search_in_file(file_path, keywords, result_queue):
    matches = {}
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
            for keyword in keywords:
                if keyword in content:
                    matches[keyword] = True
                else:
                    matches[keyword] = False
        result_queue.put({file_path: matches})
    except FileNotFoundError:
        print(f"Файл {file_path} не знайдено.")


def main_threading(files, keywords):
    start_time = time.perf_counter()
    result_queue = Queue()

    threads = []
    for file_path in files:
        thread = threading.Thread(
            target=search_in_file, args=(file_path, keywords, result_queue)
        )
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    results = []
    while not result_queue.empty():
        results.append(result_queue.get())

    print(
        f"Час багатопотокового виконання: {time.perf_counter() - start_time: .5f} секунд"
    )
    return results


if __name__ == "__main__":
    files = ["./text1.txt", "./text2.txt", "./text3.txt"]
    keywords = ["Find", "Word", "Please"]
    results = main_threading(files, keywords)
    for result in results:
        print(result)