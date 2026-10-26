from collections.abc import Callable, Iterable, Sequence
from typing import Any, List, Dict, Tuple # hay que añadir list y dict

import time  # Proporciona temporizadores de alta resolución.
from random import randint
import numpy as np
import matplotlib.pyplot as plt  # Biblioteca utilizada para crear gráficas.


def optimal_change(coins: List[int], amount: int) -> List[int] | None:

    dp = {}
    dp[0] = 0
    
    return optimal_change_recursive(coins, amount, dp)


def optimal_change_recursive(coins: List[int], amount: int, dp: Dict) -> List[int] | None:
    if amount == 0:
        return []
    
    # coins[5] es la combinacion para el amount 5 osea ej 1,1,1,1,1
    if coins[amount] != []:
        return coins[amount]