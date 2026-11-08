from collections.abc import Callable, Iterable, Sequence
from typing import Any, List, Dict, Tuple # hay que añadir list y dict
import time  # Proporciona temporizadores de alta resolución.
from random import randint
import numpy as np
from random import randint, seed as semilla

import matplotlib.pyplot as plt  # Biblioteca utilizada para crear gráficas.


def job_scheduling(jobs: List[Tuple[str, int, int]]
)-> Tuple[List[Optional[Tuple[str, int, int]]], int]:
    if not jobs :
        return ([],0)
    profit_sum = 0
    max_deadline = max(job[2] for job in jobs)
    #orden de ordenacion -profit(así reverse=True no ordena al revés con otro criterio),deadline, id
    jobs_prof = sorted(jobs, key=lambda x: (-x[1],x[2],x[0]))
    #La longitud de schedule será igual al máximo deadline
    schedule = [None] * max_deadline
    for job in jobs_prof:
        (id,profit,deadline) = job
    #desde fecha límite hasta primer hueco que encuentre
        for day in range(deadline-1, -1, -1):
            if schedule[day] is None:
                schedule[day] = job
                profit_sum += profit
                break
    return schedule, profit_sum

def generate_jobs(n: int, seed: int = 42) -> List[Tuple[str, int, int]]:
    semilla(seed)
    jobs = []
    max_deadline = max(1, n // 10)
    for i in range(n):
            name = f"J{i}"
            profit = randint(0, 1000)
            deadline = randint(1, max_deadline)
            jobs.append((name,profit ,deadline))

    return jobs

print(job_scheduling(generate_jobs(100)))