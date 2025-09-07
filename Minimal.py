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
    print("todosLosPares",todosLosPares)

                



    for a in aceptacion:

        for estado in estados:

            if estado != a and estado not in aceptacion:
                # print("aceptados", a)
                # print(estado)
                par = [a, estado]
                par.sort()
                pares.append(par)

    print("Pares", pares)


    




reduccionAFD(automata)
print("")
reduccionAFD(automata2)
