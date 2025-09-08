# AFN a AFD
# Implementacion del algoritmo de conversion AFN a AFD: Construccion de Subconjuntos.

#qué estoy intentando hacer
#primero ver si todos los estados son alcanzables, es decir ver que todos los estados aparecen en el tercr elemento de al menos una transicion
def alcanzables_desde(inicio, transiciones):
    visitados = set([inicio])
    pila = [inicio]
    while pila:
        actual = pila.pop()
        for origen, simbolo, destino in transiciones:
            if origen == actual and destino not in visitados:
                visitados.add(destino)
                pila.append(destino)
    return visitados

def eliminarEstadosNoAlcanzables(estados, transiciones, inicio, aceptacion):
    visitados = alcanzables_desde(inicio, transiciones)
    nuevos_estados = [e for e in estados if e in visitados]
    nuevas_trans = [t for t in transiciones if t[0] in visitados and t[2] in visitados]
    nuevas_acept = [a for a in aceptacion if a in visitados]
    return nuevas_trans, nuevos_estados, nuevas_acept

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
        nombre = "_".join(e) if e else "Vacio"
        estado_map[idx] = nombre
        automataDeterminista["estados"].append(nombre)

    # Estado inicial
    automataDeterminista["inicio"] = estado_map[0]  # El primero en estadosDeterministas

    # Estados de aceptación
    
    # Crear transiciones únicas
    transiciones_set = set()
    for idx_origen, fila in enumerate(tablaTransiciones):
        origen = estado_map[idx_origen]
        for col_idx, destino_lista in enumerate(fila):
            simbolo = simbolosOriginal[col_idx]
            destino_nombre = "_".join(destino_lista) if destino_lista else "Vacio"
            transiciones_set.add((origen, simbolo, destino_nombre))


    automataDeterminista["transiciones"] = [list(t) for t in transiciones_set]

    # Mantener aceptación sin recalcularla
    automataDeterminista["aceptacion"] = [
        "_".join(e) if e else "Vacio" for e in aceptacionNuevo
    ]

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

    simbolos.sort()
    existeEpsilon = False
    for trans in transiciones:
        if trans[1] == "?":
            existeEpsilon = True
            simbolos.append("?")
            simbolos.append("¡")
            break

    #hacer la tabla de transiones no determinista con las transiciones ingresadas desde el automata
    
    # print("simbolos",simbolos)
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
    # print(estados)
    # ---------- Reemplazo: calcular clausuras ε transitivas por cada estado ----------
    if "¡" in simbolos:
        clave = simbolos.index("¡")
        # construir lista de adyacencia por epsilon basada en estadosTransiciones
        # epsilon_adj[i] = lista de destinos por epsilon desde estados[i]
        epsilon_adj = []
        for i in range(len(estados)):
            # estadosTransiciones[i][clave] ya es la lista inicial (puede contener varios)
            # queremos tratarlas como adyacencia directa
            epsilon_adj.append(list(estadosTransiciones[i][clave]))

        # ahora para cada estado calcular clausura_epsilon usando pila (BFS/DFS)
        for i in range(len(estados)):
            cierre = set()
            stack = [estados[i]]
            while stack:
                v = stack.pop()
                if v in cierre:
                    continue
                cierre.add(v)
                # conseguir índices de los vecinos epsilon de v
                try:
                    idx_v = estados.index(v)
                except ValueError:
                    continue
                for nbr in epsilon_adj[idx_v]:
                    if nbr not in cierre:
                        stack.append(nbr)
            # asignar la clausura ordenada y sin duplicados a la columna '¡'
            estadosTransiciones[i][clave] = sorted(list(cierre))

    # asegurar orden consistente
    if "¡" in simbolos:
        clave = simbolos.index("¡")
        for a in estadosTransiciones:
            a[clave].sort()
    # ---------- fin reemplazo ----------


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
        # en vez de aceptacionC toda, conviértela a conjunto
        aceptacion_set = set(aceptacion)   # {'q27'}
        aceptacionNuevo = [e for e in estadosFinales if any(st in aceptacion_set for st in e)]


        # Ahora, recorrer todos los estados deterministas y agregar a aceptacionNuevo
        aceptacionNuevo = []
        for e in estadosFinales:  # e es lista de NFA-states, ej ['q0','q1']
            if any(estado in aceptacion for estado in e):
                aceptacionNuevo.append(e)

        # eliminar duplicados, por si acaso
        #print("Aceptación nuevo:", aceptacionNuevo)

        aceptacionNuevo = [list(x) for x in {tuple(a) for a in aceptacionNuevo}]
        #print("Aceptación nuevo:", aceptacionNuevo)

                # ---------- Fin construcción de aceptacionNuevo ----------



        
        automataAFD = empaquetarAFD(estadosDeterministas, tablaTransiciones, simbolosOriginal, inicio, aceptacionNuevo)
                        

        
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


                        
        automataAFD = empaquetarAFD(estadosFinales, tablaTransiciones, simbolosOriginal, inicio, aceptacionNuevo)

    return automataAFD


