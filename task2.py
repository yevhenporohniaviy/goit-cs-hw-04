from multiprocessing import Pool, Manager
import time


def search_in_file(args):
    file_path, keywords, result_dict = args

    matches = {}
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
            for keyword in keywords:
                if keyword in content:
                    matches[keyword] = True
                else:
                    matches[keyword] = False
        result_dict[file_path] = matches
    except FileNotFoundError:
        print(f"Файл {file_path} не знайдено.")
    except Exception as e:
        print(f"Помилка при обробці файлу {file_path}: {e}")


def main_multiprocessing(files, keywords):
    start_time = time.perf_counter()

    with Manager() as manager:
        result_dict = manager.dict()

        args = [(file_path, keywords, result_dict) for file_path in files]

        with Pool(processes=None) as pool:
            pool.map(search_in_file, args)

        print(
            f"Час багатопроцесорного виконання: {time.perf_counter() - start_time: .5f} секунд"
        )
        return dict(result_dict)


if __name__ == "__main__":
    files = ["./text1.txt", "./text2.txt", "./text3.txt"]
    keywords = ["Find", "Word", "Please"]
    results = main_multiprocessing(files, keywords)
    for result in results:
        print(result, results[result])
    