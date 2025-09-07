#Se determinó que el épsilon (cadena vacía) será un '?'
import json
from primeraMitad import shunting_yard,regex_AFN_McYamadaSon
from automathon import NFA

#estructura a seguir de automatas
automata = {
    "estados":[],
    "simbolos":[],
    "inicio":None,
    "aceptacion":[],
    "transiciones":[]
}
# automata["estados"] = [0,2,5,9,6,7]
# print(automata.get("estados"))


def verificar_input(input:str):
    traduccion = str.maketrans('áéíóúüÁÉÍÓÚÜ','aeiouuAEIOUU')
    input.translate(traduccion)
    caracteres_permitidos = ['?','|','+','*','(',')']
    lista_filtrada = [item for item in input if not isinstance(item, str) or not item.isalnum()]
    verdad = input.isalnum() or all(i in caracteres_permitidos for i in lista_filtrada)
    print(f"Usted ingresó {input}, y su valor de aceptación es:", verdad)
    return verdad
    #tal vez verificar que todos los paréntesis estén en pares? (cerrados y abiertos)
# verificar_input("aee1515+++*****???|||||()()()()()") #ejemplo

def export_automata(estados,simbolos,inicio,aceptacion,transiciones):
    data = {
        "estados": estados,
        "simbolos": simbolos,
        "inicio": inicio,
        "aceptacion": aceptacion,
        "transiciones": transiciones
    }
    #Se exportará a JSON
    with open("automata.json", "w") as json_file:
        json.dump(data, json_file, indent=3)
#ejemplo
# estados = [0, 1, 2]
# simbolos = ['a', 'b']
# inicio = 0
# aceptacion = [1]
# transiciones = [(0, 'a', 1), (1, 'b', 2), (2, 'a', 0)]
# export_automata(estados,simbolos,inicio,aceptacion,transiciones)
#/ejemplo
# automata_export = regex_AFN_McYamadaSon(shunting_yard("(0.0|1)*.1.(0|1)"))
# export_automata(automata_export["estados"],automata_export["simbolos"],automata_export["inicio"],automata_export["aceptacion"],automata_export["transiciones"])

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
        print("Validando NFA:", nfa.is_valid())
    except Exception as e:
        print("Advertencia: is_valid() lanzó excepción:", e)
    nfa.view(file_name)
    print(f"Visualización guardada como {file_name}.")

# visualize_automata(regex_AFN_McYamadaSon(shunting_yard("(0.0|1)*.1.(0|1)")),"prueba")
