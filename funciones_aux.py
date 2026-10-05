#Utilidades para medir tiempos de ejecución y representar resultados.
# pylint: disable=missing-function-docstring


from collections.abc import Callable, Iterable, Sequence
from typing import Any
import time  # Proporciona temporizadores de alta resolución.
from random import randint
import numpy as np

import matplotlib.pyplot as plt  # Biblioteca utilizada para crear gráficas.


# I.A.1. Medición de tiempos de ejecución
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


# Función auxiliar para generar una gráfica de una serie de datos.
def plot_single_curve(
    x: Sequence[float],
    y: Sequence[float],
    title: str = "Gráfica de datos",
    xlabel: str = "Eje X",
    ylabel: str = "Eje Y",
    label: str | None = None,
    style: str = "o-",
    color: str = "b",
    grid: bool = True,
    filename: str | None = None,
    figsize: tuple[float, float] = (8.0, 5.0),
) -> None:
    """
    Genera y muestra una gráfica para una única serie de datos.

    Args:
        x: Valores que se mostrarán en el eje horizontal.
        y: Valores que se mostrarán en el eje vertical.
        title: Título de la gráfica.
        xlabel: Etiqueta del eje horizontal.
        ylabel: Etiqueta del eje vertical.
        label: Texto de la leyenda. Si es ``None``, no se muestra leyenda.
        style: Formato de la línea y los marcadores, por ejemplo ``"o-"``.
        color: Color de la curva, por ejemplo ``"b"`` o ``"tab:blue"``.
        grid: Indica si se debe mostrar una cuadrícula.
        filename: Nombre del fichero de salida. Si es ``None``, no se guarda.
        figsize: Tupla ``(ancho, alto)`` expresada en pulgadas.

    Returns:
        ``None``. La función muestra la gráfica y, opcionalmente, la guarda.

    Raises:
        ValueError: Si ``x`` e ``y`` no tienen la misma longitud.
    """
    # Una curva necesita un valor x para cada valor y.
    if len(x) != len(y):
        raise ValueError("x e y deben tener la misma longitud")

    # Crear una figura nueva evita mezclar esta gráfica con otra anterior.
    plt.figure(figsize=figsize)

    # Dibujar la serie de datos con el estilo y el color solicitados.
    plt.plot(x, y, style, color=color, label=label)

    # Añadir información descriptiva facilita la interpretación de la gráfica.
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    # La cuadrícula es opcional para no imponer una presentación concreta.
    if grid:
        plt.grid(True, linestyle="--", alpha=0.6)

    # Solo se muestra la leyenda cuando se ha proporcionado una etiqueta.
    if label is not None:
        plt.legend(loc="best")

    # Ajustar automáticamente los márgenes evita que se corten las etiquetas.
    plt.tight_layout()

    # Guardar la figura únicamente cuando se ha indicado un nombre de fichero.
    if filename is not None:
        # split(".") funciona en ejemplos sencillos; pathlib sería preferible
        # en programas más robustos para trabajar con extensiones de fichero.
        file_format: str = filename.rsplit(".", maxsplit=1)[-1]
        plt.savefig(filename, format=file_format, dpi=300)

    # Mostrar la figura en pantalla.
    plt.show()

#FIND_DUPLICATES 28/9/26
def find_duplicates(lst) -> list:
    salida = []

    for i in range(len(lst)):
        if lst[i] in salida:
            continue

        #for j in range(i+1, len(lst)):
        for j in range(i):
            if lst[j] == lst[i]:
                salida.append(lst[j])
                break

    return salida

def preparar_find_duplicates(n):
    return list(range(n // 2)) + list(range(n // 2))
"""
Nlist = [10, 20, 50, 100, 200, 300, 400, 500, 900]

#print(time_measure(find_duplicates, preparar_find_duplicates,Nlist, 10000, 1000))


resultados = time_measure(
    find_duplicates,
    preparar_find_duplicates,
    Nlist,
    Nrep=100,
    Nstat=10
)

for n, (media, varianza) in zip(Nlist, resultados):
    print(f"n = {n}")
    print(f"  Tiempo medio: {media:.10f} segundos")
    print(f"  Varianza:     {varianza:.10e}")
    print() 


#generar la grafica

tiempos_medios = []

for media, varianza in resultados:
    tiempos_medios.append(media)

plot_single_curve(
    x=Nlist,
    y=tiempos_medios,
    title="Tiempo de ejecución de find_duplicates",
    xlabel="Tamaño de entrada (n)",
    ylabel="Tiempo medio (segundos)",
    label="find_duplicates",
    style="o-",
    color="blue"
)
"""

# HAS SUM PAIR 28/9/26 y 05/10/26
def has_sum_pair(par) -> bool:  
    lst, target = par
    dict = {}
    for element in lst:
        resta = target - element
        if resta in dict:
            return True
        dict[element] = True

    return False

def preparar_has_sum_pair(n):
    return [randint(0, n) for i in range(n)]

"""
Pruebas:

print(has_sum_pair(([1, 4, 7, 12, 3], 11)))
# True

print(has_sum_pair(([5, 8, 3], 10)))
# False
"""


# I.B Algoritmos de codificación y compresión de listas

# I.B.1 
# caso base i = 0 crea 100%
# mira el siguiente y:
# si es igual +1
# si es distinto lo crea

def rle_encode_naive(lst):
    # tlist tiene dos elementos, elem y count
    # tlist = [elem, count]
    
    tlist = []

    # el primer elemento se añade si o si
    tlist = tlist + [(lst[0], 1)]
    # para cada elemento en lst
    for i in range(len(lst)-1):
        # separa tlist en elem y count
        elem, count = tlist[len(tlist)-1]
        # si el siguiente elemento de lst está en tlist
        if lst[i+1] == elem:
            # suma 1 a count sustituyendo la tupla por una con count + 1
            tlist[len(tlist)-1] = (elem, count + 1)
        # si el siguiente elemento de lst no está en tlist
        else:
            # crea una nueva tupla
            tlist = tlist + [(lst[i+1], 1)]

    return tlist

def preparar_rle_encode_naive(n):
    return [i // 10 for i in range(n)]

Nlist = [10, 20, 50, 100, 200, 300, 400, 500, 900, 2000, 3000, 5000, 7500, 8500, 10000]

resultados = time_measure(
    rle_encode_naive,
    preparar_rle_encode_naive,
    Nlist,
    Nrep=100,
    Nstat=10
)

for n, (media, varianza) in zip(Nlist, resultados):
    print(f"n = {n}")
    print(f"  Tiempo medio: {media:.10f} segundos")
    print(f"  Varianza:     {varianza:.10e}")
    print()

tiempos_medios = []

for media, varianza in resultados:
    tiempos_medios.append(media)

plot_single_curve(
    x=Nlist,
    y=tiempos_medios,
    title="Tiempo de ejecución de rle_encode_naive",
    xlabel="Tamaño de entrada (n)",
    ylabel="Tiempo medio (segundos)",
    label="rle_encode_naive",
    style="o-",
    color="red"
)

def rle_encode_optimized(lst):
    tlist = []

    # el primer elemento se añade si o si
    tlist.append((lst[0], 1))
    # para cada elemento en lst
    for i in range(len(lst)-1):
        # separa tlist en elem y count
        elem, count = tlist[len(tlist)-1]
        # si el siguiente elemento de lst está en tlist
        if lst[i+1] == elem:
            # suma 1 a count sustituyendo la tupla por una con count + 1
            tlist[len(tlist)-1] = (elem, count + 1)
        # si el siguiente elemento de lst no está en tlist
        else:
            # crea una nueva tupla
            tlist.append((lst[i+1], 1))

# II.A TAD Conjunto Disjunto
def init_cd(n: int)-> np.ndarray:
    array = []
    for i in range(n):
        array[i] = -1
    
    return array
