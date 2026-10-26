from collections.abc import Callable, Iterable, Sequence
from typing import Any, List, Dict, Tuple # hay que añadir list y dict

import time  # Proporciona temporizadores de alta resolución.
from random import randint
import numpy as np
import matplotlib.pyplot as plt  # Biblioteca utilizada para crear gráficas.


def activity_selection(activities: List[Tuple[str, int, int]]) -> List[Tuple[str, int, int]]:

    #se ordena dependiendo de cuando terminen
    actividades_ordenadas = sorted(activities, key=lambda x: x[2])
    #por defecto la primera actividad se elige
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


#print(activity_selection([("A",1,4), ("B",3,5), ("C",0,6), ("D",5,7), ("E",8,9), ("F",5,9)]))