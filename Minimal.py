automata ={
    'estados': ['q0_q10_q4_q6_q8_q9', 'q1_q2', 'q0_q10_q11_q12_q14_q16_q4_q5_q6_q7_q9', 'q0_q10_q3_q4_q6_q7_q9', 'Vacio', 'q1_q13_q17_q2', 'q0_q10_q11_q12_q14_q15_q16_q17_q4_q5_q6_q7_q9'], 
    'simbolos': ['0', '1'], 
    'inicio': 'q0_q10_q4_q6_q8_q9', 
    'aceptacion': ['q0_q10_q11_q12_q14_q15_q16_q17_q4_q5_q6_q7_q9', 'q1_q13_q17_q2'], 
    'transiciones': [
        ['q0_q10_q3_q4_q6_q7_q9', '1', 'q0_q10_q11_q12_q14_q16_q4_q5_q6_q7_q9'], 
        ['q1_q13_q17_q2', '0', 'q0_q10_q3_q4_q6_q7_q9'], 
        ['q0_q10_q4_q6_q8_q9', '1', 'q0_q10_q11_q12_q14_q16_q4_q5_q6_q7_q9'], 
        ['Vacio', '0', 'Vacio'], ['q1_q2', '1', 'Vacio'], 
        ['q1_q2', '0', 'q0_q10_q3_q4_q6_q7_q9'], 
        ['q0_q10_q11_q12_q14_q15_q16_q17_q4_q5_q6_q7_q9', '0', 'q1_q13_q17_q2'], 
        ['Vacio', '1', 'Vacio'], 
        ['q0_q10_q11_q12_q14_q16_q4_q5_q6_q7_q9', '1', 'q0_q10_q11_q12_q14_q15_q16_q17_q4_q5_q6_q7_q9'], 
        ['q0_q10_q11_q12_q14_q16_q4_q5_q6_q7_q9', '0', 'q1_q13_q17_q2'], 
        ['q0_q10_q3_q4_q6_q7_q9', '0', 'q1_q2'], 
        ['q0_q10_q11_q12_q14_q15_q16_q17_q4_q5_q6_q7_q9', '1', 'q0_q10_q11_q12_q14_q15_q16_q17_q4_q5_q6_q7_q9'], 
        ['q0_q10_q4_q6_q8_q9', '0', 'q1_q2'], 
        ['q1_q13_q17_q2', '1', 'Vacio']
    ]
}

automata2 ={
    'estados': ['A','B', 'C','E', 'F', 'G', 'H'], 
    'simbolos': ['0', '1'], 
    'inicio': 'A', 
    'aceptacion': ['C'], 
    'transiciones': [
        ['B', '0', 'G'], 
        ['B', '1', 'C'], 
        ['A', '0', 'B'], 
        ['A', '1', 'F'], 
        ['C', '0', 'A'], 
        ['C', '1', 'C'], 
        ['E', '1', 'F'], 
        ['E', '0', 'H'], 
        ['F', '0', 'C'], 
        ['F', '1', 'G'], 
        ['G', '0', 'G'], 
        ['G', '1', 'E'], 
        ['H', '0', 'G'], 
        ['H', '1', 'C']
    ]
}

def reconstruirMinimo(automata, diferencia):
    """
    automata: dict en formato {'estados':..., 'simbolos':..., 'inicio':..., 'aceptacion':..., 'transiciones':...}
    diferencia: lista de pares de estados equivalentes (los que se pueden unir)
    """
    estados = automata["estados"]
    simbolos = automata["simbolos"]
    inicio = automata["inicio"]
    aceptacion = automata["aceptacion"]
    transiciones = automata["transiciones"]

    # Paso 1: agrupar estados equivalentes
    grupos = []   # lista de sets
    for a, b in diferencia:
        # busca si alguno de los dos ya está en un grupo
        encontrado = None
        for g in grupos:
            if a in g or b in g:
                g.update([a, b])
                encontrado = g
                break
        if not encontrado:
            grupos.append(set([a, b]))

    # incluir estados que no quedaron en ningún grupo
    for e in estados:
        if not any(e in g for g in grupos):
            grupos.append(set([e]))

    # asignar un nombre a cada grupo

     # Paso 2: dar nombres cortos n1, n2, ...
    mapa = {}
    for i, g in enumerate(grupos, start=1):
        nombre = f"n{i}"
        for estado in g:
            mapa[estado] = nombre

    # Paso 3: nuevos estados
    nuevos_estados = sorted(set(mapa.values()))

    # Paso 4: nuevo inicio
    nuevo_inicio = mapa[inicio]

    # Paso 5: aceptación (lista de cadenas)
    nuevos_aceptacion = sorted({mapa[e] for e in aceptacion})

    # Paso 6: reconstruir transiciones sin duplicados
    nuevas_transiciones = []
    for origen, simbolo, destino in transiciones:
        nuevo_origen = mapa[origen]
        nuevo_destino = mapa[destino]
        if [nuevo_origen, simbolo, nuevo_destino] not in nuevas_transiciones:
            nuevas_transiciones.append([nuevo_origen, simbolo, nuevo_destino])

    automata_min = {
        "estados": nuevos_estados,
        "simbolos": simbolos,
        "inicio": nuevo_inicio,
        "aceptacion": nuevos_aceptacion,
        "transiciones": nuevas_transiciones
    }

    return automata_min




def reduccionAFD(automata):
    estados = automata["estados"]
    simbolos = automata["simbolos"]
    inicio = automata["inicio"]
    aceptacion = automata["aceptacion"]
    transiciones = automata["transiciones"]
    tablaTransiciones = []
    pares = []
    todosLosPares = []


    for estado in estados:

        for estado2 in estados:

            if estado != estado2:

                posiblePar = [estado, estado2]
                posiblePar.sort()

                if posiblePar not in todosLosPares:
                    todosLosPares.append(posiblePar)
    #print("todosLosPares",todosLosPares)

                



    for a in aceptacion:

        for estado in estados:

            if estado != a and estado not in aceptacion:
                # print("aceptados", a)
                # print(estado)
                par = [a, estado]
                par.sort()
                pares.append(par)

    #print("Pares", pares)



    for par in pares:

      


        for trans1 in transiciones:

            for trans2 in transiciones:

                if trans1[1] == trans2[1]:


                    uno = trans1[2]
                    dos = trans2[2]

                    previo = [uno, dos]
                    previo.sort()

                    comparar = [trans1[0], trans2[0]]
                    comparar.sort()
                    

                    if uno != dos and previo in pares:
                        
                        

                        if comparar not in pares:
                            pares.append(comparar)
                          

    

    #print("pares", pares)

    diferencia = [x for x in todosLosPares if x not in pares]

    #print("dup", diferencia)


    return reconstruirMinimo(automata, diferencia)

   



                 


    




# reduccionAFD(automata)
# print("")
# print(reduccionAFD(automata2))
