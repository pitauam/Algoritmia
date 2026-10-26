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
    
    