#Se determinó que el épsilon (cadena vacía) será un '?'
import json
from primeraMitad import shunting_yard,regex_AFN_McYamadaSon
from automathon import NFA
from construcionSubConjuntos import construccionSubConjuntos 
from Minimal import reduccionAFD

#estructura a seguir de automatas
automata = {
    "estados":[],
    "simbolos":[],
    "inicio":None,
    "aceptacion":[],
    "transiciones":[]
}


def verificar_input(input:str):
    traduccion = str.maketrans('áéíóúüÁÉÍÓÚÜ','aeiouuAEIOUU')
    input.translate(traduccion)
    caracteres_permitidos = ['?','|','+','*','(',')','.']
    lista_filtrada = [item for item in input if not isinstance(item, str) or not item.isalnum()]
    verdad = input.isalnum() or all(i in caracteres_permitidos for i in lista_filtrada)
    print(f"Usted ingresó {input}, y su valor de aceptación es:", verdad)
    return verdad


def export_automata(automata,tituloArchivo):
    #Se exportará a JSON
    with open(f"{tituloArchivo}.json", "w") as json_file:
        json.dump(automata, json_file, indent=3)


def visualize_automata(mi_auto, file_name="automata"):
    q = set(mi_auto["estados"])
    #Automathon solo permite la cadena vacía '' para epsilon,
    sigma = set()
    for s in mi_auto["simbolos"]:
        if s == '?':
            sigma.add('')   # interpretacion de epsilon en libreria
        else:
            sigma.add(s)
    
    delta = {estado: {} for estado in q}
    for origen, simbolo, destino in mi_auto["transiciones"]:
        sym = '' if simbolo == '?' else simbolo
        if origen not in delta:
            delta[origen] = {}
        delta[origen].setdefault(sym, set()).add(destino)
    
    initial_state = mi_auto["inicio"]
    f = set(mi_auto["aceptacion"])  # conjunto de finales
    
    nfa = NFA(q=q, sigma=sigma, delta=delta, initial_state=initial_state, f=f)
    
    try:
        nfa.is_valid()
    except Exception as e:
        print("Advertencia: is_valid() lanzó excepción:", e)
    nfa.view(file_name)
    print(f"Visualización guardada como {file_name}.")


def aceptacion_palabra(palabra, automata):
    tokens = list(palabra)
    if not all(i in automata["simbolos"] for i in tokens):
        print("Los símbolos de la palabra ingresada no pertenecen al alfabeto del autómata.")
        return False

    estado_actual = automata["inicio"]
    transiciones = automata["transiciones"]
    aceptacion = automata["aceptacion"]

    print(f"\nProcesando palabra: '{palabra}'")
    print(f"Estado inicial: {estado_actual}")

    for simbolo in tokens:
        encontrado = False
        for transicion in transiciones:
            origen, simbolo_transicion, destino = transicion
            if origen == estado_actual and simbolo_transicion == simbolo:
                print(f"  ({origen}) --[{simbolo}]--> ({destino})")
                estado_actual = destino
                encontrado = True
                break
        if not encontrado:
            print(f"  ❌ No hay transición desde el estado '{estado_actual}' con el símbolo '{simbolo}'.")
            return False

    if estado_actual in aceptacion:
        print(f"✅ La palabra '{palabra}' es aceptada. Estado final: {estado_actual}\n")
        return True
    else:
        print(f"❌ La palabra '{palabra}' NO es aceptada. Estado final: {estado_actual}\n")
        return False
            


#MAIN
menu = "1"
minimal_general = None
print("Bienvenido a este programa relacionado a autómatas, por favor, seleccione una opción: \n")
while menu != "0":
    print("1. Construir un nuevo automata minimal a partir de una regex")
    print("2. Comprobar si una cadena pertenece al autómata")
    print("0. Salir")
    menu = input("Seleccione una opción: ")
    
    if menu == "1":
        print("La regex a ingresar debe de tener únicamente valores alfanuméricos, así como | para unión, * para estella de Kleene, + para suma de Kleene, . para concatenación")
        print("Para la cadena vacía épsilon, usar ?")
        
        regex = input("Ingrese la regexp: ")
        
        if verificar_input(regex) == False: 
            print("Ingresó una entrada no válida. Por favor, ingrese únicamente alfanuméricos y los siguientes símbolos: |*+.?")
        else:
            postfix = shunting_yard(regex)
            afn = regex_AFN_McYamadaSon(postfix)
            export_automata(afn,"AFN")
            visualize_automata(afn,"AFN")
            
            afd = construccionSubConjuntos(afn)
            export_automata(afd,"AFD")
            visualize_automata(afd,"AFD")

            AFD_minimal = reduccionAFD(afd)
            export_automata(AFD_minimal,"Minimal")
            visualize_automata(AFD_minimal,"Minimal")
            # print(AFD_minimal)
            minimal_general = AFD_minimal
#(0|1)*.1.1.(0|1)*
#(0|1.1)*.(0.0|1.1).(0|1)*              (0.0|1.1)*.(0.0.0|1.1.1).(0.0|1.1)*
#(0|1).1.1.(0|1) 

    elif menu == "2":
        palabra_verificar = input("Ingrese la palabra a verificar: ")
        if minimal_general is None: 
            print("Primero ingrese una regexp para volverla AFD minimal, en la opción 1.")
        else:
            aceptacion_palabra(palabra_verificar,minimal_general)

    elif menu == "0":
        print("Gracias por utilizar el programa :D")
    else:
        print("Ingrese una opción válida del menú")
