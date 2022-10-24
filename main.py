import json
import base64
import queue
import requests
import numpy as np
from threading import Thread
import matplotlib.pyplot as plt
import urllib.parse as urlparse
from queue import Queue
import time
import copy

from wolfram_parser import WolframInputGenerator
from evaluate_solutions import eval_all
    
    
class Worker(Thread):
    def __init__(self, q: Queue, solutions: list, *args, **kwargs) -> None:
        self.q = q
        self.solutions = solutions
        super().__init__(*args, **kwargs)
        
        self.daemon = True
    
    def run(self):
        while True:
            try:
                work = self.q.get(timeout=3)  # 3s timeout
            except queue.Empty:
                return

            parameter, n, url, search_term = work

            # Get and parse data
            data = requests.get(url).text
            data = data.replace("jQuery36108552903897608751_1666553041562", "")
            data = data[1:-2]
            data = json.loads(data)

            # Get solution
            solution = None
            for pod in data["queryresult"]["pods"]:
                if pod["title"] == search_term:
                    solution = pod["subpods"][0]["plaintext"]
                    break

            if solution == None:
                for pod in data["queryresult"]["pods"]:
                    if pod["title"] == "Result":
                        solution = pod["subpods"][0]["plaintext"]
                        break

            self.solutions[parameter][n] = solution
            self.q.task_done()


def make_requests(equation:str, variables: dict):
    # Threads
    n_threads = 5
    threads = []

    # Work
    wolfram = WolframInputGenerator()
    request_errors = wolfram.gaussian_error(equation, variables)
    request_functions = wolfram.function_eval(equation, variables)

    solutions = {
        "functions": {},
        "errors": {}
    }

    queue = Queue()

    for n, url in enumerate(request_errors[0]):
        queue.put(("errors", n, url, request_errors[1]))

    for n, url in enumerate(request_functions[0]):
        queue.put(("functions", n, url, request_functions[1]))

    for i in range(n_threads):
        threads.append(Worker(queue, solutions))
    
    for thread in threads:
        thread.start()        
        
    for thread in threads:
        thread.join()
        
    return solutions
    

def main():
    equation = "ln(x)"
    variables = {
        "x": {
            "value": [1, 3, 500, 10, 1, 3, 5],
            "error": 0.1
        },
    }
    solution = make_requests(equation, variables)
    function_values = eval_all(solution)

    for i in function_values:
        print(i)
if __name__ == "__main__":
    main()

# for x_n in variables:
    


# print(x, y)   

# plt.plot(x, y, color="red", marker=".", linestyle="-")
# plt.xlabel("$\infty$")
# plt.ylabel("Lol2")
# plt.show()