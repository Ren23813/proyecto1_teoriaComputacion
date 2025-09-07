# AFN a AFD
# Implementacion del algoritmo de conversion AFN a AFD: Construccion de Subconjuntos.

#qué estoy intentando hacer
#primero ver si todos los estados son alcanzables, es decir ver que todos los estados aparecen en el tercr elemento de al menos una transicion


def eliminarEstadosNoAlcanzables(estados, transiciones, inicio, aceptacion):
    
    estadosAlcanzablesTransiciones = []                     #lista que almacena todos los estados alcanzables de las transiciones

    for transicion in transiciones:             #se agregan los estado que si son alcanzables
        if transicion[2] != inicio:
            estadosAlcanzablesTransiciones.append(transicion[2]) #no se agrega el estado inicial
    
    estadosNoInicial = estados.copy()
    estadosNoInicial.remove(inicio)             #listado de estados sin el estado inicial

    estadosAlcanzables = list(set(estadosAlcanzablesTransiciones)) #eliminar estados duplicados de las transiciones

    estadosNoInicial.sort() #ordenar ambos
    estadosAlcanzables.sort() #ordenar ambos

    estadosNoAlcanzables = []

    transicionesAlcanzables = transiciones.copy()

    # print(estadosNoInicial)
    # print(estadosAlcanzables)
    if estadosNoInicial != estadosAlcanzables:
        estadosNoAlcanzables = [elemento for elemento in estadosNoInicial if elemento not in estadosAlcanzables] #llenar con los estados no alcanzables
        

        for transicion in transiciones:
            for estado in estadosNoAlcanzables:
                if transicion[0] == estado:
                    
                    transicionesAlcanzables.remove(transicion)

        estadosAlcanzables.append(inicio)
        estadosAlcanzables.sort()

        aceptacion2 = aceptacion.copy()

        for a in aceptacion2:
            for estado in estadosNoAlcanzables:
                if a == estado:
                    aceptacion2.remove(estado)
                    
        return transicionesAlcanzables, estadosAlcanzables, aceptacion2
    else: 
        estados.sort()
        return transiciones, estados, aceptacion
    
print("")


def empaquetarAFD(estadosDeterministas, tablaTransiciones, simbolosOriginal, inicio, aceptacionNuevo):
    # Diccionario final
    automataDeterminista = {
        "estados": [],
        "simbolos": simbolosOriginal,
        "inicio": "",
        "aceptacion": [],
        "transiciones": []
    }

    # Generar nombres para los estados deterministas (conjuntos)
    # Convertimos cada lista de estados en un string concatenando con '_'
    estado_map = {}
    for idx, e in enumerate(estadosDeterministas):
        if e == []:
            nombre = "Vacio"  # Nombre para estado vacío
        else:
            nombre = "_".join(map(str, e))
        estado_map[idx] = nombre
        automataDeterminista["estados"].append(nombre)

    # Estado inicial
    automataDeterminista["inicio"] = estado_map[0]  # El primero en estadosDeterministas

    # Estados de aceptación
    for idx, e in enumerate(estadosDeterministas):
        if e in aceptacionNuevo:
            automataDeterminista["aceptacion"].append(estado_map[idx])

    # Crear transiciones únicas
    transiciones_set = set()
    for idx_origen, fila in enumerate(tablaTransiciones):
        origen = estado_map[idx_origen]
        for col_idx, destino_lista in enumerate(fila):
            simbolo = simbolosOriginal[col_idx]
            if destino_lista == []:
                destino_nombre = "Vacio"
                key = (origen, simbolo, destino_nombre)
                transiciones_set.add(key)
            else:
                destino_nombre = "_".join(map(str, destino_lista))
                key = (origen, simbolo, destino_nombre)
                transiciones_set.add(key)

    # Convertir set a lista
    for t in transiciones_set:
        automataDeterminista["transiciones"].append(list(t))

    # Convertir la lista de aceptación a nombres tipo 'q0_q10'
    aceptacion_cadenas = []
    for estado in aceptacionNuevo:
        if estado == []:
            nombre = "Vacio"
        else:
            nombre = "_".join(map(str, estado))
        aceptacion_cadenas.append(nombre)

    # Luego en el diccionario:
    automataDeterminista["aceptacion"] = aceptacion_cadenas


    return automataDeterminista


#Acá intento construir algo más
def construccionSubConjuntos(automata):
    estados = automata["estados"]
    simbolos = automata["simbolos"]
    simbolosOriginal = simbolos.copy()
    inicio = automata["inicio"]
    aceptacion = automata["aceptacion"]
    transiciones = automata["transiciones"]


    #Se empieza el procedimiento de eliminar los estados no alcanzables
    reduccionCompleta = True
    transiciones2 = []
    estados2 = []
    aceptacion2 = []


    while reduccionCompleta == True:
        transiciones2, estados2, aceptacion2 = eliminarEstadosNoAlcanzables(estados,transiciones,inicio, aceptacion)

        if estados != estados2:
            transiciones, estados, aceptacion = eliminarEstadosNoAlcanzables(estados2,transiciones2,inicio, aceptacion2)
        else:
            reduccionCompleta = False

    print("estados", estados)
    print("transiciones", transiciones)
    print("aceptacion", aceptacion)

    simbolos.sort()
    existeEpsilon = False
    for trans in transiciones:
        if trans[1] == "?":
            existeEpsilon = True
            simbolos.append("?")
            simbolos.append("¡")
            break

    #hacer la tabla de transiones no determinista con las transiciones ingresadas desde el automata
    
    print("simbolos",simbolos)
    estadosTransiciones = []

    for e in range(len(estados)):
        fila = []

        for s in range(len(simbolos)):
            valor = []

            for transicion in transiciones:
                if (transicion[0] == estados[e]) & (transicion[1] == simbolos[s]):

                    valor.append(transicion[2])
                
                
                    


            fila.append(valor)
          
        estadosTransiciones.append(fila)

    #se agregan los valores a la columna de clave en la tabla de estados
    
    for e in range(len(estados)):
        for s in range(len(simbolos)):
            if "?" in simbolos:
                epsilon = simbolos.index("?")
               

            if simbolos[s] =="¡":
                clave = []

                if len(estadosTransiciones[e][epsilon]) == 0:
                    clave.append(estados[e])
                elif len(estadosTransiciones[e][epsilon]) == 1:
                    clave.append(estados[e])
                    clave.append(estadosTransiciones[e][epsilon][0])


                elif len(estadosTransiciones[e][epsilon]) > 1:
                    clave.append(estados[e])

                    for h in estadosTransiciones[e][epsilon]:
                        clave.append(h)
                clave = list(set(clave)) 
                clave.sort()

                estadosTransiciones[e][s] = clave

    #se agregan los estados faltantes creados por e mismo epsilon
    print(estados)
    if "¡" in simbolos:
        clave = simbolos.index("¡")
        for e in range(len(estados)):


            if len(estadosTransiciones[e][clave]) > 1:
            

                for a in estadosTransiciones[e][clave]:
                  
                    #print("RRRRRR", a, estados[e])
                    if a != estados[e]:
                        #indice = 0
                        indice = estados.index(a)


                        posiblesNuevas = estadosTransiciones[indice][clave]
                        # print("&&&&&&&", estadosTransiciones)
                        # print("iiiiiii", estadosTransiciones[indice])
                        #print("yyyyy", posiblesNuevas)
                        



                        if len(posiblesNuevas) == 1:
                            #print("nooo", posiblesNuevas[0], estadosTransiciones[e][clave])
                            if posiblesNuevas[0] not in estadosTransiciones[e][clave]:
                                estadosTransiciones[e][clave].append(posiblesNuevas[0])
                                #print("RA")
                        elif len(posiblesNuevas) > 1:
                            #print("naaaa", posiblesNuevas[0], estadosTransiciones[e][clave])

                            for h in posiblesNuevas:

                                if h not in estadosTransiciones[e][clave]:
                                    estadosTransiciones[e][clave].append(h)
                        estadosTransiciones[e][clave] = sorted(list(set(estadosTransiciones[e][clave])))
                                    

                                 
    if "¡" in simbolos:
        clave = simbolos.index("¡")
        for a in estadosTransiciones:
            a[clave].sort()


        





    # print("O")
    # for a in estadosTransiciones:
    #     print(a)

    estadosDeterministas = estados.copy()
    


    agregado = False
    #agregar transiciones al conjunto vacio siempre que no exista una transicion para un estado
    for estadosR in estadosTransiciones:    
        for trans in estadosR:
            if len(trans) == 0 and agregado == False:
              
                estadosDeterministas.append([])
    
                fila = []
                for i in range(len(simbolos)):
                    fila.append([])
  
                estadosTransiciones.append(fila)
                agregado = True
                break
        if agregado:
            break
            
    # print("estados deterministas")
    # for j in range(len(estadosDeterministas)):
    #     print(estadosDeterministas[j], "    ", estadosTransiciones[j])

  
    
   
  

    
    #Los vuelvo conjuntos
    copiaestadosD = estadosDeterministas.copy()
    estadosDeterministas.clear()
    for o in copiaestadosD:
        if o != []:

            f = []
            f.append(o)
            estadosDeterministas.append(f)
        else:
            estadosDeterministas.append([])


    

    #determinista con ?
   
        # ---------- Inicio: nueva implementación para el caso existeEpsilon == True ----------
    if existeEpsilon == True:
        # índice de la columna "clave" (la clausura ε que tú ya llenaste)
        clave_idx = simbolos.index("¡")

        # 1) localizar el índice del estado inicial en la tabla NFA (estados)
        try:
            idx_inicio = estados.index(inicio)
        except ValueError:
            # precaución: si no lo encuentra, usar la primera fila por defecto
            idx_inicio = 0

        # 2) obtener la "clave" (clausura ε) del estado inicial
        inicio_clausura = estadosTransiciones[idx_inicio][clave_idx]
        # normalizar (eliminar duplicados y ordenar)
        inicio_clausura = sorted(list(dict.fromkeys(inicio_clausura)))

        # 3) preparar estructuras para la construcción por subconjuntos (AFD)
        # estadosDeterministas: lista de listas, cada elemento es una lista de nombres de estados NFA
        estadosDeterministas = []
        tablaTransiciones = []   # cada fila corresponderá al estado determinista en el mismo índice
        cola = []                # BFS/cola de estados por procesar

        # símbolos a procesar: columnas en 'simbolos' que corresponden a simbolosOriginal
        symbol_cols = []
        for s in simbolosOriginal:
            try:
                symbol_cols.append(simbolos.index(s))
            except ValueError:
                # si algún símbolo original no está presente (raro), lo ignoramos
                pass

        # 4) inicializar con la clausura del inicio
        estadosDeterministas.append(inicio_clausura)
        tablaTransiciones.append(None)  # placeholder; se llenará cuando procesemos esta fila
        cola.append(inicio_clausura)

        # 5) proceso principal: para cada estado determinista, calcular su fila (por cada símbolo)
        while cola:
            actual = cola.pop(0)                       # actual: lista de NFA-states, p. ej. ['P','Q']
            idx_actual = estadosDeterministas.index(actual)  # índice donde colocar la fila
            fila = []

            # para cada símbolo del alfabeto original (sin ? ni ¡)
            for col_sym in symbol_cols:
                # move: union de destinos directos por 'col_sym' desde cada estado en 'actual'
                move_set = set()
                for sNFA in actual:
                    # puede suceder que un nombre en 'actual' no aparezca en 'estados' (seguridad)
                    if sNFA not in estados:
                        continue
                    idx_sNFA = estados.index(sNFA)
                    destinos = estadosTransiciones[idx_sNFA][col_sym]  # lista (puede ser [])
                    for d in destinos:
                        if d is not None and d != "":
                            move_set.add(d)

                # ahora aplicamos clausura ε a cada estado en move_set:
                nueva_clausura = set()
                for d in sorted(move_set):
                    if d not in estados:
                        continue
                    idx_d = estados.index(d)
                    clausura_d = estadosTransiciones[idx_d][clave_idx]  # lista de estados (su clausura)
                    for c in clausura_d:
                        nueva_clausura.add(c)

                # representamos la célula como lista ordenada (o [] si está vacía)
                nueva_lista = sorted(list(nueva_clausura))

                # agregar la célula a la fila (combinada correctamente, no append de listas-anidadas)
                fila.append(nueva_lista)

                # si ese nuevo conjunto no estaba en los estados deterministas, añadirlo y crear placeholder
                if nueva_lista not in estadosDeterministas:
                    estadosDeterministas.append(nueva_lista)
                    tablaTransiciones.append(None)  # placeholder para su fila futura
                    cola.append(nueva_lista)

            # una vez calculada la fila completa para 'actual', guardarla en la tabla en su índice
            tablaTransiciones[idx_actual] = fila

        # 6) asegurar que todas las filas están llenas (por si quedó algún None)
        num_cols = len(symbol_cols)
        for i in range(len(tablaTransiciones)):
            if tablaTransiciones[i] is None:
                tablaTransiciones[i] = [ [] for _ in range(num_cols) ]

        # 7) si el estado vacío [] apareció, garantizamos que tenga su propia fila (ya lo añadimos)
        #    (arriba ya añadimos fila-placeholder en cuanto apareció [])

        # 8) terminar: preparar variables que se usan más abajo en tu función
        estadosFinales = estadosDeterministas.copy()   # lo que tú llamabas "estadosFinales"
        # (tablaTransiciones ya está construida acorde a 'estadosFinales')

        # ---------- Construir lista de aceptación del determinista ----------
        # Primero, convertir los estados de aceptación del NFA a listas para comparación
        aceptacionC = []
        for a in aceptacion:
            fila = []
            if len(str(a)) == 1:
                fila.append(a)
            elif len(str(a)) > 1:
                for i in a:
                    fila.append(i)
            aceptacionC.append(fila)

        # Ahora, recorrer todos los estados deterministas y agregar a aceptacionNuevo
        aceptacionNuevo = []
        for e in estadosFinales:  # e es lista de NFA-states, ej ['q0','q1']
            if any(estado in aceptacion for estado in e):
                aceptacionNuevo.append(e)
        # eliminar duplicados, por si acaso
        aceptacionNuevo = [list(x) for x in {tuple(a) for a in aceptacionNuevo}]
                # ---------- Fin construcción de aceptacionNuevo ----------


        # print(":D tablaTransiciones")
        # for b in range(len(tablaTransiciones)):
        #     print(estadosDeterministas[b], "   ", tablaTransiciones[b])
        # print("Aceptacion", aceptacionNuevo)
    # ---------- Fin: nueva implementación para existeEpsilon == True ----------


        
        automataAFD = empaquetarAFD(estadosDeterministas, tablaTransiciones, simbolosOriginal, inicio, aceptacionNuevo)
                        


        

    
    #Determinista sin ?
        
    elif existeEpsilon == False:
        fila = 0
        while fila < len(estadosDeterministas):
            #print("E", estadosTransiciones)
            estadoActual = estadosDeterministas[fila]
            transicionesActuales = estadosTransiciones[fila]

            agregarElementoEstados = []

            for t in transicionesActuales:
                #agregarElementoEstados.clear()
                if not t:
                    continue
                agregarElementoEstados = sorted(set(t))  

                # No hacemos nada si está vacío o ya existe
                if len(agregarElementoEstados) != 0 and agregarElementoEstados not in estadosDeterministas:
                    
                    estadosDeterministas.append(agregarElementoEstados)
                
                    
                    #print("ESTADOOOOOOS", estadosDeterministas)
                    agregarFila = []

                    for col in range(len(simbolos)):
                        #print("COL", col)
                        elementoFila = []

                        for p in agregarElementoEstados:
                            buscarEstado = [p]
                            #print("PPPPPP", buscarEstado)

                            if buscarEstado in estadosDeterministas:
                                numFila = estadosDeterministas.index(buscarEstado)
                                #print("INDEX", numFila)

                                resultadoBusqueda = estadosTransiciones[numFila][col]
                                #print("ENCONTRADO", resultadoBusqueda)

                                for u in resultadoBusqueda:
                                    if u not in elementoFila:
                                        elementoFila.append(u)

                        elementoFila = list(set(elementoFila))
                        elementoFila.sort()
                        #print("ELEMENTO FILA", elementoFila)
                        agregarFila.append(elementoFila)
                    estadosTransiciones.append(agregarFila)
            

            fila += 1
                    
        inicioFinal = [inicio]
        estadosFinales = []
        tablaTransiciones = []
        for i in range(len(estadosTransiciones)):
            estadoActual = estadosDeterministas[i]
            transicionActual = estadosTransiciones[i]

            if i == 0 and estadoActual == inicioFinal:
                estadosFinales.append(estadoActual)
                tablaTransiciones.append(transicionActual)
            

            

            for s in range(len(simbolos)):
                estadoSiguiente = transicionActual[s]
                

                if estadoSiguiente not in estadosFinales:
                    if estadoSiguiente not in estadosDeterministas:
                        estadoSiguiente.sort()
                    indice = estadosDeterministas.index(estadoSiguiente)
                    v = estadosTransiciones[indice]
                    
                    estadosFinales.append(estadoSiguiente)
                    tablaTransiciones.append(v)
                





                        
        #volver los estados de aceptación listas
        aceptacionC = []
        for a in aceptacion:
            fila = []
            if len(str(a)) == 1:
                fila.append(a)
            elif len(str(a)) > 1:
                for i in a:
                    fila.append(i)
            aceptacionC.append(fila)




        #agregar los nuevos estados que contienen estados de aceptación en estados de aceptación
        aceptacionNuevo= []
        for e in estadosFinales:
            if len(e) > 0:
                for i in e:
                    comprobar = []
                    comprobar.append(i)

                    if comprobar in aceptacionC:
                        aceptacionNuevo.append(e)
                        break


    
        print("E")
        for uuu in tablaTransiciones:
            print(uuu)
        print("EEE", tablaTransiciones)
        print("U", estadosFinales)
        print("A",aceptacionNuevo)
        
        #este truena 
        #print("UUUUUUUUUUUUUUUUU", estadosTransiciones[0][1][0])
        automataAFD = empaquetarAFD(estadosFinales, tablaTransiciones, simbolosOriginal, inicio, aceptacionNuevo)
    


    return automataAFD






    









      




#automatas de ejemplo
automata1 = {
    "estados" : [0, 1, 2],
    "simbolos":["a", "b","c"],
    "inicio": 0,
    "aceptacion": [1, 2],
    "transiciones" :[ [0, "a", 1], [1, "b", 2], [2, "a", 1]]

}





# Automata 3
automata3 = {
    "estados": [0, 1],
    "simbolos": ["a", "b"],
    "inicio": 0,
    "aceptacion": [1],
    "transiciones": [
        [0, "a", 1],
        [0, "b", 0],
        [1, "a", 1],
        [1, "b", 0]
    ]
}


# Automata 4 (con épsilon como "?")
automata4 = {
    "estados": [0, 1, 2, 3],
    "simbolos": ["a", "b"],
    "inicio": 0,
    "aceptacion": [3],
    "transiciones": [
        [0, "a", 1],
        [0, "?", 2],  # épsilon
        [1, "b", 3],
        [2, "b", 3]
    ]
}


# Automata 5
automata5 = {
    "estados": [0, 1, 2],
    "simbolos": ["a", "b"],
    "inicio": 0,
    "aceptacion": [2],
    "transiciones": [
        [0, "a", 1],
        [0, "b", 0],
        [1, "a", 1],
      
        [1, "b", 2],
          [1, "b", 1],
        [2, "a", 2],
        [2, "b", 2]
    ]
}


# Automata 8 (letras como estados)
automata8 = {
    "estados": ["A", "B", "C", "H", "J"],
    "simbolos": ["0", "1"],
    "inicio": "A",
    "aceptacion": ["C"],
    "transiciones": [
        ["A", "0", "J"],
        ["A", "?", "C"],
        ["B", "1", "C"],
        ["C", "0", "A"],
        ["C", "1", "C"],
        ["B", "1", "A"]
    ]
}


# Automata 9 (con estado inalcanzable)
automata9 = {
    "estados": ["A", "B", "C", "D"],
    "simbolos": ["0", "1"],
    "inicio": "A",
    "aceptacion": ["C", "D"],
    "transiciones": [
        ["A", "0", "B"],
        ["B", "1", "C"],
        ["C", "0", "A"]
        # D no tiene transiciones
    ]
}



# AFND con dos estados no alcanzables encadenados
automata10 = {
    "estados" : ["A", "B", "C", "D", "E"],
    "simbolos" : ["0", "1"],
    "inicio":"A",
    "aceptacion" : ["C", "D", "E"],  # D y E son de aceptación pero no alcanzables
    "transiciones":[
        ["A", "0", "B"],  # A → B con 0
        ["B", "1", "C"],  # B → C con 1
        ["C", "0", "A"],  # C → A con 0
        # D y E no tienen conexión con A, B o C
        ["D", "1", "E"]   # D → E con 1 (pero D nunca es alcanzable, por tanto E tampoco)
    ]

}


# AFND con 3 estados inalcanzables encadenados (D -> E -> F)
automata11 = {
    "estados": ["A", "B", "C", "D", "E", "F"],
    "simbolos": ["0", "1"],
    "inicio": "A",
    "aceptacion": ["C", "D", "E", "F"],   # D, E, F también marcados como aceptacion (ejemplo)
    "transiciones": [
        # Componente principal alcanzable desde A
        ["A", "0", "B"],
        ["B", "1", "C"],
        ["C", "0", "A"],

        # Estados inalcanzables encadenados
        ["D", "1", "E"],   # D -> E
        ["E", "0", "F"]    # E -> F
        # Nota: no hay transiciones desde A/B/C hacia D/E/F, por eso son inalcanzables
    ]
}

automata12 = {
    "estados": ["A", "B", "C"],
    "simbolos": ["0", "1"],
    "inicio": "A",
    "aceptacion": ["C"],
    "transiciones": [
        ["A", "0", "B"],
        ["A", "0", "C"],   # misma entrada "0" desde A va tanto a B como a C
        ["B", "0", "A"],
        ["B", "1", "C"],
        ["C", "1", "A"]
    ]
}

automata13 = {
    "estados": ["P", "Q", "R", "S"],
    "simbolos": ["0", "1"],
    "inicio": "P",
    "aceptacion": ["R", "S"],
    "transiciones": [
        ["P", "1", "Q"],
        ["P", "1", "S"],
        ["P", "1", "R"],   # mismo estado P, mismo símbolo 1, a dos estados distintos
        ["Q", "0", "R"],
        ["Q", "0", "S"],   # Q → 0 → R y S (dos salidas)
        ["R", "1", "R"],   # bucle en R
        ["R", "1", "Q"],
        ["S", "0", "P"]
    ]
}

automata14 = {
    "estados": ["P", "Q", "R", "S"],
    "simbolos": ["0", "1"],
    "inicio": "P",
    "aceptacion": ["R", "S"],
    "transiciones": [
        ["P", "1", "Q"],
        ["P", "1", "S"],
        ["P", "1", "R"],   # mismo estado P, mismo símbolo 1, a dos estados distintos
        ["Q", "0", "R"],
        ["Q", "0", "S"],   # Q → 0 → R y S (dos salidas)
        ["R", "1", "R"],   # bucle en R
        ["R", "1", "Q"],
        ["S", "0", "P"],
        ["S", "?", "S"],
        ["Q", "?", "P"],

    ]
}


automata15 = {
    "estados": ["A", "B", "C", "D", "E", "F"],
    "simbolos": ["0", "1"],
    "inicio": "A",
    "aceptacion": ["D"],
    "transiciones": [
        ["A", "0", "E"],
        ["A", "1", "B"],   # mismo estado P, mismo símbolo 1, a dos estados distintos
        ["B", "1", "C"],
        ["B", "?", "D"],   # Q → 0 → R y S (dos salidas)
        ["C", "1", "D"],   # bucle en R
        ["E", "0", "F"],
        ["E", "?", "B"],
        ["E", "?", "C"],
        ["F", "0", "D"],

    ]
}

automata16 ={
    'estados': ['q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q8', 'q9', 'q10', 'q11', 'q12', 'q13', 'q14', 'q15', 'q16', 'q17'], 
    'simbolos': ['0', '1'], 
    'inicio': 'q8', 
    'aceptacion': ['q17'], 
    'transiciones': [
        ['q0', '0', 'q1'], 
        ['q2', '0', 'q3'], 
        ['q1', '?', 'q2'], 
        ['q4', '1', 'q5'], 
        ['q6', '?', 'q0'], 
        ['q6', '?', 'q4'], 
        ['q3', '?', 'q7'], 
        ['q5', '?', 'q7'], 
        ['q8', '?', 'q6'], 
        ['q7', '?', 'q6'], 
        ['q7', '?', 'q9'], 
        ['q8', '?', 'q9'], 
        ['q10', '1', 'q11'], 
        ['q9', '?', 'q10'], 
        ['q12', '0', 'q13'], 
        ['q14', '1', 'q15'], 
        ['q16', '?', 'q12'], 
        ['q16', '?', 'q14'], 
        ['q13', '?', 'q17'], 
        ['q15', '?', 'q17'], 
        ['q11', '?', 'q16']]
        }



# print("automata 1:")
# construccionSubConjuntos( automata1)
# print("")
# print("automata 3:")
# construccionSubConjuntos(automata3)
# print("")
print("automata 4:")
construccionSubConjuntos(automata4)
print("")
# print("automata 5:")
# construccionSubConjuntos(automata5)
# print("")
# print("automata 8:")
# construccionSubConjuntos(automata8)
# print("")
# print("automata 9:")
# construccionSubConjuntos(automata9)
# print("")
# print("automata 10:")
# construccionSubConjuntos(automata10)
# print("")
# print("automata 11:")
# construccionSubConjuntos(automata11)
# print("")
# print("automata 12:")
# construccionSubConjuntos(automata12)
print("")
print("automata 13:")
print(construccionSubConjuntos(automata13))
print("")
print("automata 14:")
construccionSubConjuntos(automata14)

print("")
print("automata 15:")
construccionSubConjuntos(automata15)
print("")
print("automata 16:")
print(construccionSubConjuntos(automata16))

