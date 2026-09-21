from time import perf_counter # librería time para usar perf_counter()

def time_measure(f: function, dataprep: function, Nlist: list, Nrep=1000, Nstat=100) -> list:
    start = perf_counter()



    finish = perf_counter()

# Pruebas de time_measure:
def time_measure_test():
     time_measure()

def main():
    time_measure_test()


main()