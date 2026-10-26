from collections.abc import Callable, Iterable, Sequence
from typing import Any, List, Dict, Tuple # hay que añadir list y dict

import time  # Proporciona temporizadores de alta resolución.
from random import randint
import numpy as np
import matplotlib.pyplot as plt  # Biblioteca utilizada para crear gráficas.


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