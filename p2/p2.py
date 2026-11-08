from collections.abc import Callable, Iterable, Sequence
from typing import Any, List, Dict, Tuple # hay que añadir list y dict
import time  # Proporciona temporizadores de alta resolución.
from random import randint
import numpy as np

import matplotlib.pyplot as plt  # Biblioteca utilizada para crear gráficas.




#Medición de tiempos de ejecución
def time_measure(
    f: Callable[[Any], Any],
    dataprep: Callable[[int], Any],
    Nlist: Sequence[int],
    Nrep: int = 1000,
    Nstat: int = 100,
) -> list[tuple[float, float]]:
    """Mide el tiempo medio y la varianza de una función.

    Para cada tamaño ``n`` de ``Nlist``:

    1. Se genera un conjunto de datos mediante ``dataprep(n)``.
    2. Se ejecuta ``f(data)`` varias veces.
    3. Se repite la medición para obtener varias observaciones estadísticas.
    4. Se calcula la media y la varianza de esas observaciones.

    Args:
        f: Función que se desea medir. Debe aceptar un único argumento.
        dataprep: Función que genera los datos de prueba a partir de ``n``.
        Nlist: Secuencia de tamaños de entrada que se van a estudiar.
        Nrep: Número de ejecuciones de ``f`` en cada medición parcial.
        Nstat: Número de mediciones parciales para cada tamaño de entrada.

    Returns:
        Una lista de tuplas ``(media, varianza)``. Cada posición corresponde
        al tamaño de entrada situado en la misma posición de ``Nlist``.

    Raises:
        ValueError: Si ``Nrep`` o ``Nstat`` no son positivos.
    """
    # Validar los parámetros evita realizar mediciones sin sentido, como
    # dividir entre cero o no recoger ninguna observación.
    if Nrep <= 0 or Nstat <= 0:
        raise ValueError("Nrep y Nstat deben ser mayores que cero")

    # Esta lista almacenará un resultado para cada tamaño de entrada.
    results: list[tuple[float, float]] = []

    # Recorremos cada tamaño de entrada que queremos estudiar.
    for n in Nlist:
        # Aquí se guardará una medición media por cada repetición estadística.
        partial_times: list[float] = []

        for _ in range(Nstat):
            # Generar los datos fuera del intervalo medido evita incluir en el
            # tiempo de la función el coste de preparar la entrada.
            data: Any = dataprep(n)

            # perf_counter() es apropiado para medir intervalos de tiempo
            # porque utiliza un reloj de alta resolución.
            start_time: float = time.perf_counter()

            # Ejecutar varias veces reduce el efecto de pequeñas variaciones
            # del sistema operativo y permite obtener un tiempo medio.
            for _ in range(Nrep):
                f(data)

            end_time: float = time.perf_counter()

            # El tiempo total se convierte en tiempo medio por ejecución.
            time_per_execution: float = (end_time - start_time) / Nrep
            partial_times.append(time_per_execution)

        # Media aritmética de las mediciones parciales.
        mean_value: float = sum(partial_times) / Nstat

        # Varianza poblacional: se divide entre el número total de mediciones.
        variance_value: float = sum(
            (value - mean_value) ** 2 for value in partial_times
        ) / Nstat

        # Asociamos la media y la varianza al tamaño de entrada actual.
        results.append((mean_value, variance_value))

    return results


#Se supondrá que existe un número ilimitado de monedas de cada moneda, que las monedas son enteros positivos no repetidas y que el sistema no contiene necesariamente una moneda de valor 1.

def greedy_change(coins: List[int], amount: int) -> Tuple[List[int], int]:

    coins.sort(reverse=True)

    #coins selected
    selected = []

    #remainder after using the coins
    remainder = amount

    for coin in coins:
        if coin > remainder:
            continue

        #mientras que la coin seleccionada sea menor o igual que lo que queda
        while coin <= remainder:
            remainder = remainder - coin
            selected.append(coin)

    return selected, remainder

def optimal_change(coins: List[int], amount: int) -> List[int] | None:

    dp = {}
    dp[0] = []

    #la mejor forma de llegar a 2 es con una moneda de 2
    for coin in coins:
        dp[coin] = [coin]

    return optimal_change_recursive(coins, amount, dp)

#funcion auxiliar para hacer recursión
def optimal_change_recursive(coins: List[int], amount: int, dp: Dict) -> List[int] | None:
    if amount in dp:
        return dp[amount]
    
    if amount < 0:
        return None

    best = None

    for coin in coins:        
        sub = optimal_change_recursive(coins, amount-coin, dp)

        
        if sub is not None:
            candidato = sorted(sub + [coin], reverse=True)
            
            #si es mas corto que el mejor se convierte en el nuevo mejor
            if (best is None or len(candidato) < len(best) or (len(candidato) == len(best) and candidato > best)):
                best = candidato 

    dp[amount] = best

    return best

#print(optimal_change([5,3], 7))

def compare_change(coins: List[int], max_amount: int) -> Dict[str,
List[int]]:
    res = {
"optimal": [],
"suboptimal": [],
"greedy_failed": [],
"impossible": []
    }

    for i in range(max_amount+1):
        greedy_comb, remainder = greedy_change(coins, i)
        optimal_comb = optimal_change(coins, i)
        if optimal_comb != None and remainder == 0:
            if (greedy_comb != None):
                g = len(greedy_comb)
            if(optimal_comb != None):
                o = len(optimal_comb)
            if o == g:
                res["optimal"].append(i)
            if g>o:
                res["suboptimal"].append(i)
        if remainder != 0:
            if optimal_comb != None:
                res["greedy_failed"].append(i)
            else:
                res["impossible"].append(i)

    return res

#print(compare_change([7,5,3,1],30))

def activity_selection(activities: List[Tuple[str, int, int]]) -> List[Tuple[str, int, int]]:

    #se ordena dependiendo de cuando terminen
    actividades_ordenadas = sorted(activities, key=lambda x: x[2])
    #por defecto la primera actividad se elige si o si
    actividad_seleccionada = actividades_ordenadas[0]
    #lista que devolver
    actividades_realizadas = []
    #primera actividad realizada
    actividades_realizadas.append(actividad_seleccionada)

    for actividad in actividades_ordenadas:
        if actividad[1] >= actividad_seleccionada[2]:
            #fin-inicio
            #ocupado = ocupado + (actividad[2] - actividad[1])
            actividad_seleccionada = actividad
            actividades_realizadas.append(actividad_seleccionada)

    return actividades_realizadas




def generate_activities(n: int, seed: int = 42) -> List[Tuple[str, int, int]]:
    #se importa la funcion seed como semilla para que no hayan problemas
    semilla(seed)
    
    activities = []
    
    for i in range(n):
        name = f"A{i}"
        start = randint(0, 10000)
        duration = randint(1, 100)
        end = start + duration
        
        activities.append((name, start, end))
        
    return activities

def job_scheduling(jobs: List[Tuple[str, int, int]])-> Tuple[List[Optional[Tuple[str, int, int]]], int]:
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

#print(job_scheduling(generate_jobs(100)))