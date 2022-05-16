# ROUND ROBIN
programas = [
    {"id": "A",
     "instrucciones": ['nueva sum1 I 20', 'nueva sum2 I 24', 'nueva res I 0', 'sume sum1', 'sume sum2',
                       'etiqueta algo1 3', 'etiqueta algo2 4', 'almacene res', 'imprima res', 'retorne 0'],
     "tiempo de llegada": 0,
     "rafaga": 0,
     "rafaga de tiempo": 0,
     "tiempo de finalizacion": 0,
     "retorno": 0,
     "espera": 0},
    {"id": "B",
     "instrucciones": ['nueva x1 I 20', 'nueva x2 I 24', 'nueva res I 0', 'sume sum1', 'sume sum2',
                       'etiqueta algo1 3', 'etiqueta algo2 4', 'almacene res', 'imprima res', 'retorne 0'],
     "tiempo de llegada": 2,
     "rafaga": 0,
     "rafaga de tiempo": 0,
     "tiempo de finalizacion": 0,
     "retorno": 0,
     "espera": 0},
    {"id": "C",
     "instrucciones": ['nueva nombre I 23', 'nueva nombre_2 I 212', 'muestre nombre', 'cargue nombre', 'sume nombre_2',
                       'almacene nombre', 'imprima nombre', 'retorne 0'],
     "tiempo de llegada": 5,
     "rafaga": 0,
     "rafaga de tiempo": 0,
     "tiempo de finalizacion": 0,
     "retorno": 0,
     "espera": 0}
]
quantum = 2
print("quantum : ", quantum)
tiempos_llegada = [0, 0, 0]

cant_instrucciones = []

for programa in programas:
    instrucciones_programa = 0
    for instruccion in programa["instrucciones"]:
        if not (instruccion.startswith("nueva") or instruccion.startswith(
                "etiqueta") or instruccion.startswith("retorne")):
            instrucciones_programa += 1
    programa["tiempo de llegada"] = tiempos_llegada[programas.index(programa)]
    programa["rafaga"] = instrucciones_programa
    programa["rafaga de tiempo"] = instrucciones_programa
    cant_instrucciones.append(instrucciones_programa)

print("Cantidad de instrucciones x programa ", cant_instrucciones)
print("Rafagas x programa ", cant_instrucciones)
print("********")

contador = quantum

for programa in programas:
    print(programa)
print("********")
cant_programas = len(programas)  # es la variable que controla los programas que hacen falta por terminar
tiempo = 0
programas_cola = []
programa_ejecusion = None  # variable que corresponde al programa que actualmente se encuentra en ejecusion
n_programa = 0  # variable utilizada para pasar al siguiente
print("[+] Se establecieron varibles para el funcionamiento")
print("@@@@@@@ Incicio del Algortimo  @@@@@@@@")
sw = True  # Variable de control
while (cant_programas > 0):  # Mientras haya programas para ejecutarse
    print("---------------- Tiempo [" + str(tiempo) + "]  ---------------")
    # valida si en el tiempo de llegada actual ya pasaron programas antes o estan pasando
    if (len(programas) > n_programa and tiempo >= programas[n_programa]["tiempo de llegada"]):
        print("[+]El programa " + str(programas[n_programa]["id"]) + " se ingreso a la cola de listos")
        programas_cola.append(programas[n_programa])  # Agrega el programa actual a la cola actual
        n_programa += 1  # pasa al siguiente programa
    else:
        if n_programa > 0 or len(programas_cola) > 0:
            if (programa_ejecusion == None):
                programa_ejecusion = programas_cola.pop(0)
                sw = True
                print("[+] Se saca el proceso " + str(programa_ejecusion["id"]) + " de la cola y se ejecuta.")
                print(programa_ejecusion["instrucciones"])
            else:
                if sw:
                    if (programa_ejecusion["rafaga de tiempo"] >= quantum):
                        programa_ejecusion["rafaga de tiempo"] = programa_ejecusion["rafaga de tiempo"] - quantum
                        print("[+] Se resta " + str(quantum) + " a la rafaga del programa " + str(
                            programa_ejecusion["id"]) + " por superar el quantum")
                        tiempo = tiempo + quantum
                        print("[+] Se aumenta" + str(quantum) + " al tiempo")
                    else:
                        tiempo += programa_ejecusion["rafaga de tiempo"]
                        print("[+] Se aumenta " + str(programa_ejecusion["rafaga de tiempo"]) + " al tiempo")
                        print("[+] Se resta " + str(
                            programa_ejecusion["rafaga de tiempo"]) + " a la rafaga del proceso " + str(
                            programa_ejecusion["id"]))
                        programa_ejecusion["rafaga de tiempo"] = 0
                    if programa_ejecusion["rafaga de tiempo"] < 1:
                        print("---------------- Tiempo [" + str(tiempo) + "]  ---------------")
                        print("[+] El Proceso " + str(programa_ejecusion["id"]) + " finalizo.")
                        programa_ejecusion["tiempo de finalizacion"] = tiempo
                        programa_ejecusion["retorno"] = programa_ejecusion["tiempo de finalizacion"] - \
                                                        programa_ejecusion["tiempo de llegada"]
                        programa_ejecusion["espera"] = programa_ejecusion["retorno"] - programa_ejecusion["rafaga"]
                        cant_programas -= 1
                        programa_ejecusion = None
                    else:
                        sw = False
                else:
                    programas_cola.append(programa_ejecusion)
                    print("[+] Se agrega el proceso " + str(
                        programa_ejecusion["id"]) + " que estaba en ejecusion a la cola de listos")
                    programa_ejecusion = None
        else:
            tiempo += 1
print("@@@@@@@ Algoritmo Finalizado @@@@@@@@")
print("!!!!!!!!!!!!!! Resultados !!!!!")
total_retorno = 0
total_espera = 0
for programa in programas:
    print(
        "Programa " + str(programa["id"]) + " Finalizo: " + str(programa["tiempo de finalizacion"]) + " Espera: " + str(
            programa["espera"]) + " Retorno: " + str(programa["retorno"]))
    total_retorno += programa["retorno"]
    total_espera += programa["espera"]
print("Promedio de retorno: " + str(total_retorno / len(programas)))
print("Promedio de espera: " + str(total_espera / len(programas)))
