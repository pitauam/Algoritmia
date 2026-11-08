import time
from p2 import (
    greedy_change, optimal_change, compare_change,
    activity_selection, generate_activities,
    job_scheduling, generate_jobs
)

print("=== APARTADO I.D: CAMBIO DE MONEDAS (1 a 500) ===")
sistemas = [
    [200, 100, 50, 20, 10, 5, 2, 1],
    [10, 5, 2, 1],
    [25, 10, 4, 1],
    [4, 3, 1]
]

for coins in sistemas:
    # Pasamos list(coins) para evitar mutaciones
    res = compare_change(list(coins), 500)
    total = 500
    opt = len(res["optimal"])
    sub = len(res["suboptimal"])
    fail = len(res["greedy_failed"])
    imp = len(res["impossible"])
    
    # Medición de tiempos de 1 a 500
    t0 = time.perf_counter()
    for m in range(1, 501):
        greedy_change(list(coins), m)
    t_greedy = time.perf_counter() - t0

    t0 = time.perf_counter()
    for m in range(1, 501):
        optimal_change(list(coins), m)
    t_opt = time.perf_counter() - t0

    print(f"Sistema {coins}:")
    print(f"  Optimal: {opt} ({opt/total*100:.2f}%) | Suboptimal: {sub} ({sub/total*100:.2f}%) | "
          f"Greedy Failed: {fail} ({fail/total*100:.2f}%) | Impossible: {imp} ({imp/total*100:.2f}%)")
    print(f"  Tiempos -> Greedy: {t_greedy:.6f} s | Optimal: {t_opt:.6f} s\n")

print("=== APARTADO II.C: SELECCION DE ACTIVIDADES ===")
for n in [100, 500, 1000, 5000]:
    acts = generate_activities(n, seed=42)
    tiempos = []
    for _ in range(10):
        t0 = time.perf_counter()
        sel = activity_selection(acts)
        tiempos.append(time.perf_counter() - t0)
    t_medio = sum(tiempos) / len(tiempos)
    num_sel = len(sel)
    porc = (num_sel / n) * 100
    print(f"n={n:4d} | Tiempo medio: {t_medio:.6f} s | Seleccionadas: {num_sel:4d} | Porcentaje: {porc:.2f}%")

print("\n=== APARTADO III.C: PLANIFICACION DE TAREAS ===")
for n in [100, 500, 1000, 5000]:
    jobs = generate_jobs(n, seed=42)
    tiempos = []
    for _ in range(10):
        t0 = time.perf_counter()
        sched, total_profit = job_scheduling(jobs)
        tiempos.append(time.perf_counter() - t0)
    t_medio = sum(tiempos) / len(tiempos)
    num_sel = sum(1 for x in sched if x is not None)
    porc = (num_sel / n) * 100
    print(f"n={n:4d} | Tiempo medio: {t_medio:.6f} s | Beneficio: {total_profit:7d} | "
          f"Seleccionadas: {num_sel:4d} ({porc:.2f}%)")


import matplotlib.pyplot as plt


n_vals = [100, 500, 1000, 5000]

# Datos del Apartado II.C (Selección de actividades)
act_tiempos = [0.000011, 0.000062, 0.000170, 0.001277]
act_seleccionadas = [72, 180, 250, 562]
act_porcentajes = [72.00, 36.00, 25.00, 11.24]

# Datos del Apartado III.C (Planificación de tareas)
job_tiempos = [0.000038, 0.000444, 0.001290, 0.024402]
job_beneficios = [9578, 47584, 94923, 473174]
job_porcentajes = [10.00, 10.00, 10.00, 10.00]

# Configuración visual general
plt.rcParams.update({'font.size': 11})

# 1. Gráfica 1: Actividades - Tamaño vs Tiempo
plt.figure(figsize=(7, 4.5))
plt.plot(n_vals, act_tiempos, marker='o', color='#1f77b4', linewidth=2)
plt.title('Selección de Actividades: Tamaño de entrada vs. Tiempo')
plt.xlabel('Tamaño de entrada (n)')
plt.ylabel('Tiempo medio de ejecución (s)')
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.savefig('grafica1.png', dpi=300)
plt.close()

# 2. Gráfica 2: Actividades - Tamaño vs Número de seleccionadas
plt.figure(figsize=(7, 4.5))
plt.plot(n_vals, act_seleccionadas, marker='s', color='#2ca02c', linewidth=2)
plt.title('Selección de Actividades: Tamaño vs. Actividades seleccionadas')
plt.xlabel('Tamaño de entrada (n)')
plt.ylabel('Número de actividades seleccionadas')
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.savefig('grafica2.png', dpi=300)
plt.close()

# 3. Gráfica 3: Actividades - Tamaño vs Porcentaje seleccionado
plt.figure(figsize=(7, 4.5))
plt.plot(n_vals, act_porcentajes, marker='^', color='#ff7f0e', linewidth=2)
plt.title('Selección de Actividades: Tamaño vs. Porcentaje seleccionado')
plt.xlabel('Tamaño de entrada (n)')
plt.ylabel('Actividades seleccionadas (%)')
plt.ylim(0, 100)
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.savefig('grafica3.png', dpi=300)
plt.close()

# 4. Gráfica 4: Tareas - Número de tareas vs Tiempo
plt.figure(figsize=(7, 4.5))
plt.plot(n_vals, job_tiempos, marker='o', color='#d62728', linewidth=2)
plt.title('Planificación de Tareas: Número de tareas vs. Tiempo')
plt.xlabel('Número de tareas (n)')
plt.ylabel('Tiempo medio de ejecución (s)')
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.savefig('grafica4.png', dpi=300)
plt.close()

# 5. Gráfica 5: Tareas - Número de tareas vs Beneficio total
plt.figure(figsize=(7, 4.5))
plt.plot(n_vals, job_beneficios, marker='s', color='#9467bd', linewidth=2)
plt.title('Planificación de Tareas: Número de tareas vs. Beneficio total')
plt.xlabel('Número de tareas (n)')
plt.ylabel('Beneficio total obtenido')
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.savefig('grafica5.png', dpi=300)
plt.close()

# 6. Gráfica 6: Tareas - Número de tareas vs Porcentaje seleccionado
plt.figure(figsize=(7, 4.5))
plt.plot(n_vals, job_porcentajes, marker='^', color='#8c564b', linewidth=2)
plt.title('Planificación de Tareas: Número de tareas vs. Porcentaje seleccionado')
plt.xlabel('Número de tareas (n)')
plt.ylabel('Tareas seleccionadas (%)')
plt.ylim(0, 25)
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.savefig('grafica6.png', dpi=300)
plt.close()

print("¡Gráficas grafica1.png a grafica6.png generadas correctamente!")