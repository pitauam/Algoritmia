
import math
import random

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

def simulate_single_walk(steps: int) -> tuple[float, float, float]:
    if(steps == 0):
        return (0.0,0.0,0.0)
    x=0.0
    y=0.0
    for i in range(steps):
        theta = random.uniform(0, 2 * math.pi)
        xi = math.cos(theta)
        yi = math.sin(theta)
        x = x+xi
        y = y+yi
    return (x,y, math.sqrt((x*x)+(y*y)))

    """
    Simula la trayectoria bidimensional de una sola partícula que parte desde el origen (0.0, 0.0) 
    y da un número determinado de pasos en direcciones aleatorias uniformes [0, 2*pi).

    :param steps: Número de pasos a simular.
    :return: Tupla con la posición final (x, y) y la distancia euclidiana final al origen.
    """
print(simulate_single_walk(50))
def monte_carlo_diffusion_simulation(num_particles: int, num_steps: int) -> float:
    
    
    
    """
    Aplica el método de Monte Carlo simulando un conjunto masivo de partículas independientes 
    para calcular la Distancia Cuadrática Media (R^2).

    :param num_particles: Número total de partículas independientes a simular.
    :param num_steps: Número de pasos por caminata.
    :return: Valor de la Distancia Cuadrática Media (R^2).
    """
    pass
