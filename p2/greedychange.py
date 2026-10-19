from collections.abc import Callable, Iterable, Sequence
from typing import Any, List, Dict, Tuple # hay que añadir list y dict

import time  # Proporciona temporizadores de alta resolución.
from random import randint
import numpy as np
import matplotlib.pyplot as plt  # Biblioteca utilizada para crear gráficas.



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

"""
    #Greedy change con programacion dinámica
    def optimal_change(coins: List[int], amount: int) -> List[int] | None:

        coins.sort(reverse=True)

        #coins selected
        selected = []

        #remainder after using the coins
        remainder = amount

        for coin in coins:
            if coin > remainder:
                continue

            for coin in coins:
                if coin > remainder:
                    continue

                if (amount % coin) == 0:
                    selected.append(coin*(amount/coin))
                    remainder = 0
                    return selected, remainder






        return selected, remainder


"""


def optimal_change(coins: List[int], amount: int) -> List[int] | None:
    if amount == 0:
        return []

    coins = sorted(coins, reverse=True)

    # dp[i] guarda la mejor combinación para conseguir i
    dp = [None] * (amount + 1)
    dp[0] = []

    for i in range(1, amount + 1):
        for coin in coins:
            if coin > i:
                continue

            previous = dp[i - coin]

            if previous is None:
                continue

            candidate = sorted(previous + [coin], reverse=True)

            if (
                dp[i] is None
                or len(candidate) < len(dp[i])
                or (
                    len(candidate) == len(dp[i])
                    and candidate > dp[i]
                )
            ):
                dp[i] = candidate

    return dp[amount]
"""
print(optimal_change([4, 3, 1], 6))
# [3, 3]

print(optimal_change([5, 3], 7))
# None

print(optimal_change([23, 19, 7, 5, 2, 1], 67))
# [50, 20, 10, 5, 2]
"""