# Práctica 3: Programación Dinámica - Algoritmos Recursivos - Monte Carlo
# Algoritmia y Estructuras de Datos Avanzadas - Curso 2026-2027

import math
import random

# =============================================================================
# I. Alineamiento de Proteínas
# =============================================================================

# I.A Alineamiento Global: Needleman-Wunsch

def needleman_wunsch_matrix(seq1: str, seq2: str, match: int = 2, mismatch: int = -1, gap: int = -1) -> list[list[int]]:

    #primero hay que hacer la matriz:
    # columnas es seq1 y filas son seq2. "_" no se usa y por eso se llama así
    filas = len(seq2) + 1
    columnas = len(seq1) + 1
    matriz = []

    for i in range(filas):
        fila_nueva = []
        for j in range(columnas):
            fila_nueva.append(0)
        matriz.append(fila_nueva)

    #se rellena la primera columna y la primera fila
    for i in range(filas):
        matriz[i][0] = i * gap
    
    for i in range(columnas):
        matriz[0][i] = i * gap

    #algoritmo para calcular la matriz, el rango es de 1 a filas para no salirse al hacer seq[i-1]
    for i in range(1, filas):
        for j in range(1, columnas):
            #si coinciden las letras el score es 2
            if seq2[i - 1] == seq1[j - 1]:
                score = match
            #si no coinciden se pone el score a mismatch
            else:
                score = mismatch

            #se calculan las 3 opciones
            diagonal = matriz[i - 1][j - 1] + score
            arriba = matriz[i - 1][j] + gap
            izquierda = matriz[i][j - 1] + gap

            #se elige el maximo de entre las 3 opciones
            matriz[i][j] = max(diagonal, arriba, izquierda)

    """
    Construye y devuelve la matriz completa de programación dinámica para el 
    alineamiento global de dos secuencias mediante el algoritmo Needleman-Wunsch.

    La matriz resultante tiene dimensiones (len(seq2) + 1) x (len(seq1) + 1), 
    donde seq1 se desarrolla a lo largo de las columnas y seq2 a lo largo de las filas.

    :param seq1: Primera secuencia a alinear (desarrollada en columnas).
    :param seq2: Segunda secuencia a alinear (desarrollada en filas).
    :param match: Puntuación acordada para una coincidencia de caracteres.
    :param mismatch: Penalización por diferencia de caracteres.
    :param gap: Penalización por introducción de hueco (gap).
    :return: Matriz de programación dinámica (lista de listas de enteros).
    """
    return matriz

#prueba cutre
#for i in range(5):
#    print(needleman_wunsch_matrix("HELO", "HALO", 2, -1, -1)[i])


def needleman_wunsch_backtracking(matrix: list[list[int]], seq1: str, seq2: str, match: int = 2, mismatch: int = -1, gap: int = -1) -> tuple[str, str, int]:
    seq1_final = []
    seq2_final = []
    i = len(seq2)
    j = len(seq1)
    #número de abajo a la derecha
    ij = matrix[i][j]
    while not (j == 0 and i == 0):
        if (j>0 and i>0):
            act = matrix[i][j]
            ismatch = (seq1[j-1] == seq2[i-1])
            diagonal = matrix[i-1][j-1] + (match if ismatch else mismatch)
            up = matrix[i-1][j] + gap
            left = matrix[i][j-1] + gap
            if (act == diagonal):
                seq1_final.append(seq1[j-1])
                seq2_final.append(seq2[i-1])
                i -= 1
                j -= 1
            elif (act==up):
                seq1_final.append('-')
                seq2_final.append(seq2[i-1])
                i -= 1
            elif (act == left):
                seq1_final.append(seq1[j-1])
                seq2_final.append('-')
                j -= 1
            elif i > 0:
                seq1_final.append('-')
                seq2_final.append(seq2[i-1])
                i -= 1
        elif i > 0:
            seq1_final.append('-')
            seq2_final.append(seq2[i-1])
            i -= 1
        elif j > 0:
            seq1_final.append(seq1[j-1])
            seq2_final.append('-')
            j -= 1
    return_seq1 = "".join(seq1_final[::-1])
    return_seq2 = "".join(seq2_final[::-1])

    return return_seq1, return_seq2, ij
    
    
    
    """
    Reconstruye las secuencias alineadas globalmente y calcula el score total a partir 
    de la matriz de programación dinámica de Needleman-Wunsch mediante backtracking.

    El backtracking comienza en la esquina inferior derecha (len(seq2), len(seq1)) y 
    recorre la matriz hasta la esquina superior izquierda (0, 0). 
    En la estructura de la matriz, seq1 se desarrolla en columnas y seq2 en filas.

    :param matrix: Matriz de programación dinámica previamente calculada.
    :param seq1: Primera secuencia original (desarrollada en columnas).
    :param seq2: Segunda secuencia original (desarrollada en filas).
    :param match: Puntuación acordada para una coincidencia.
    :param mismatch: Penalización por diferencia.
    :param gap: Penalización por hueco.
    :return: Tupla con (aligned_seq1, aligned_seq2, total_score).
    """
    pass

# I.B Alineamiento Local: Smith-Waterman

def smith_waterman_matrix(seq1: str, seq2: str, match: int = 2, mismatch: int = -1, gap: int = -1) -> list[list[int]]:
    """
    Construye y devuelve la matriz de programación dinámica para el alineamiento 
    local de dos secuencias mediante el algoritmo Smith-Waterman.

    Aplica inicialización a ceros en los bordes (primera fila y primera columna) 
    y truncamiento a cero en cada celda para evitar valores negativos. 
    La matriz tiene dimensiones (len(seq2) + 1) x (len(seq1) + 1), donde seq1 se 
    desarrolla a lo largo de las columnas y seq2 a lo largo de las filas.

    :param seq1: Primera secuencia a alinear (desarrollada en columnas).
    :param seq2: Segunda secuencia a alinear (desarrollada en filas).
    :param match: Puntuación por coincidencia.
    :param mismatch: Penalización por diferencia.
    :param gap: Penalización por hueco.
    :return: Matriz de programación dinámica local (lista de listas de enteros).
    """
    filas = len(seq2) + 1
    columnas = len(seq1) + 1
    matriz = []

    #crear matriz de ceros
    #los bordes se ponen a 0
    for i in range(filas):
        fila_nueva = []
        for j in range(columnas):
            fila_nueva.append(0)
        matriz.append(fila_nueva)

    #se rellena lo de dentro
    for i in range(1, filas):
        for j in range(1, columnas):
            if seq2[i - 1] == seq1[j - 1]:
                score = match
            else:
                score = mismatch

            diagonal = matriz[i - 1][j - 1] + score
            arriba = matriz[i - 1][j] + gap
            izquierda = matriz[i][j - 1] + gap

            #se mete un 0 en el max para que no sea negativo :)
            matriz[i][j] = max(0, diagonal, arriba, izquierda)

    return matriz

def smith_waterman_backtracking(matrix: list[list[int]], seq1: str, seq2: str, match: int = 2, mismatch: int = -1, gap: int = -1) -> tuple[str, str, int]:
    """
    Reconstruye el alineamiento local óptimo y su puntuación a partir de la matriz 
    de Smith-Waterman mediante backtracking.

    Localiza el valor máximo global en la matriz y realiza el backtracking hasta 
    alcanzar una celda con valor 0. En la matriz, seq1 se desarrolla en columnas 
    y seq2 en filas.

    :param matrix: Matriz de programación dinámica local previamente calculada.
    :param seq1: Primera secuencia original (desarrollada en columnas).
    :param seq2: Segunda secuencia original (desarrollada en filas).
    :param match: Puntuación por coincidencia.
    :param mismatch: Penalización por diferencia.
    :param gap: Penalización por hueco.
    :return: Tupla con (sub_seq1, sub_seq2, max_score).
    """
    #primero se saca el numero de filas y columnas de la matriz
    filas = len(matrix)
    columnas = len(matrix[0])

    #variables para guardar el valor maximo y su posicion (i = fila, j = columna)
    max_score = 0
    max_i = 0
    max_j = 0

    #se recorre toda la matriz para encontrar el valor maximo global
    for i in range(filas):
        for j in range(columnas):
            if matrix[i][j] > max_score:
                max_score = matrix[i][j]
                max_i = i
                max_j = j

    #variables para ir guardando las secuencias alineadas
    sub_seq1 = ""
    sub_seq2 = ""

    #se empieza el backtracking desde la posicion del maximo
    i = max_i
    j = max_j

    #el bucle sigue mientras no se llegue a una celda con 0 ni se salga de los bordes
    while i > 0 and j > 0 and matrix[i][j] > 0:
        #se mira si las letras coinciden (filas son seq2 y columnas son seq1)
        if seq2[i - 1] == seq1[j - 1]:
            score = match
        else:
            score = mismatch

        #se comprueba de donde viene el valor de la celda actual:
        #si viene de la diagonal (match o mismatch)
        if matrix[i][j] == matrix[i - 1][j - 1] + score:
            sub_seq1 = seq1[j - 1] + sub_seq1
            sub_seq2 = seq2[i - 1] + sub_seq2
            i -= 1
            j -= 1
        #si viene de arriba (gap en seq1, que son las columnas)
        elif matrix[i][j] == matrix[i - 1][j] + gap:
            sub_seq1 = "-" + sub_seq1
            sub_seq2 = seq2[i - 1] + sub_seq2
            i -= 1
        #si viene de la izquierda (gap en seq2, que son las filas)
        elif matrix[i][j] == matrix[i][j - 1] + gap:
            sub_seq1 = seq1[j - 1] + sub_seq1
            sub_seq2 = "-" + sub_seq2
            j -= 1

    return (sub_seq1, sub_seq2, max_score)

#pruebas
"""
f0 = [0, 0, 0, 0, 0, 0]
f1 = [0, 2, 1, 0, 0, 0]
f2 = [0, 1, 4, 3, 2, 1]
f3 = [0, 0, 3, 3, 2, 4]
f4 = [0, 0, 2, 2, 5, 4]
f5 = [0, 0, 1, 1, 4, 7]
matriz_test = [f0, f1, f2, f3, f4, f5]

print(smith_waterman_backtracking(matriz_test, "CGTGA", "CGAGA", 2, -1, -1))

f0_igual = [ 0, 0 ]
f1_igual = [ 0, 2 ]
m_igual = [f0_igual, f1_igual]
print(smith_waterman_backtracking(m_igual, "H", "H", 2, -1, -1))

f0_distinta = [ 0, 0 ]
f1_distinta = [ 0, 0 ]
m_distinta = [f0_distinta, f1_distinta]
print(smith_waterman_backtracking(m_distinta, "H", "E", 2, -1, -1))
print(smith_waterman_backtracking(m_distinta, "H", "h", 2, -1, -1))

f0_vacia = [ 0, 0 ]
m_vacia = [f0_vacia]
print(smith_waterman_backtracking(m_vacia, "H", "", 2, -1, -1))
"""

# =============================================================================
# II. Optimización de Rutas en una Cuadrícula
# =============================================================================

# II.A Recursividad Ingenua (Enfoque de Fuerza Bruta)

def min_path_recursive(grid: list[list[int]], i: int, j: int) -> int:
    """
    Calcula el coste mínimo para alcanzar la celda (i, j) desde el origen (0, 0) 
    utilizando una estrategia recursiva pura (fuerza bruta sin memoización).

    :param grid: Matriz rectangular de costes numéricos enteros.
    :param i: Índice de la fila de la celda destino.
    :param j: Índice de la columna de la celda destino.
    :return: Coste acumulado mínimo para llegar a la celda (i, j).
    """
    #caso base 1: si llegamos al origen (0, 0), devolvemos su propio coste
    if i == 0 and j == 0:
        return grid[0][0]

    #caso base 2: si estamos en la primera fila (i == 0), solo podemos venir de la izquierda
    if i == 0:
        return grid[0][j] + min_path_recursive(grid, 0, j - 1)

    #caso base 3: si estamos en la primera columna (j == 0), solo podemos venir de arriba
    if j == 0:
        return grid[i][0] + min_path_recursive(grid, i - 1, 0)

    #caso general: elegimos el camino mas barato entre venir de arriba o de la izquierda
    arriba = min_path_recursive(grid, i - 1, j)
    izquierda = min_path_recursive(grid, i, j - 1)

    return grid[i][j] + min(arriba, izquierda)

"""
f0 = [ 1, 3, 1, 2 ]
f1 = [ 2, 1, 8, 1 ]
f2 = [ 4, 2, 1, 2 ]
f3 = [ 5, 2, 1, 1 ]
grid = [f0, f1, f2, f3]

#coste hasta esquina abajo izquierda (9)
print(min_path_recursive(grid, 3, 3))

#caso limite desde origen hasta origen
print(min_path_recursive(grid, 0, 0))
"""

# II.B Programación Dinámica (Enfoque Bottom-Up)

def min_path_dp(grid: list[list[int]]) -> tuple[int, list[list[int]]]:
    """
    Calcula el coste mínimo para ir desde la celda (0, 0) hasta (N-1, M-1) 
    mediante programación dinámica ascendente (bottom-up).

    :param grid: Matriz de costes de dimensiones N x M.
    :return: Tupla con el coste mínimo global (int) y la matriz dp de costes acumulados.
    """
    pass

# II.C Reconstrucción de la Ruta Óptima

def get_optimal_path(grid: list[list[int]]) -> tuple[int, list[tuple[int, int]]]:
    """
    Reconstruye la secuencia exacta de coordenadas (0, 0) ... (N-1, M-1) que forman 
    el camino de coste mínimo en la cuadrícula.

    Invoca internamente a min_path_dp(grid) para generar la matriz de costes acumulados.

    :param grid: Matriz original de costes.
    :return: Tupla con el coste total mínimo y la lista de coordenadas (i, j) de la ruta.
    """
    pass

# =============================================================================
# III. Simulación de Movimiento y Difusión mediante Caminata Aleatoria (Random Walk)
# =============================================================================
#nota: probabilidad entre 0 y 1
# III.A El comportamiento de una partícula individual

def simulate_single_walk(steps: int) -> tuple[float, float, float]:
    """
    Simula la trayectoria bidimensional de una sola partícula que parte desde el origen (0.0, 0.0) 
    y da un número determinado de pasos en direcciones aleatorias uniformes [0, 2*pi).

    :param steps: Número de pasos a simular.
    :return: Tupla con la posición final (x, y) y la distancia euclidiana final al origen.
    """
    pass

# III.B El enfoque de Monte Carlo y la Ley de Difusión

def monte_carlo_diffusion_simulation(num_particles: int, num_steps: int) -> float:
    """
    Aplica el método de Monte Carlo simulando un conjunto masivo de partículas independientes 
    para calcular la Distancia Cuadrática Media (R^2).

    :param num_particles: Número total de partículas independientes a simular.
    :param num_steps: Número de pasos por caminata.
    :return: Valor de la Distancia Cuadrática Media (R^2).
    """
    pass

# III.C Confinamiento y barreras absorbentes

def simulate_particle_with_barrier(steps: int, max_radius: float) -> bool:
    """
    Simula la caminata paso a paso de una partícula evaluando en cada paso si supera 
    un radio límite (barrera absorbente).

    :param steps: Número máximo de pasos.
    :param max_radius: Radio límite de la barrera desde el origen.
    :return: True si la partícula cruza la barrera en algún paso, False en caso contrario.
    """
    pass

def calculate_escape_probability(num_particles: int, num_steps: int, max_radius: float) -> float:
    """
    Estima la probabilidad de escape de un conjunto de partículas en presencia 
    de una barrera absorbente mediante el método de Monte Carlo.

    :param num_particles: Número de partículas a simular.
    :param num_steps: Número máximo de pasos por partícula.
    :param max_radius: Radio de la barrera absorbente.
    :return: Probabilidad de escape expresada en el intervalo [0.0, 1.0].
    """
    pass