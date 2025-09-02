#Se determinó que el épsilon (cadena vacía) será un '?'
import json

def verificar_input(input:str):
    traduccion = str.maketrans('áéíóúüÁÉÍÓÚÜ','aeiouuAEIOUU')
    input.translate(traduccion)
    caracteres_permitidos = ['?','|','+','*','(',')']
    lista_filtrada = [item for item in input if not isinstance(item, str) or not item.isalnum()]
    verdad = input.isalnum() or all(i in caracteres_permitidos for i in lista_filtrada)
    print(f"Usted ingresó {input}, y su valor de aceptación es:", verdad)
    #tal vez verificar que todos los paréntesis estén en pares? (cerrados y abiertos)

verificar_input("aee1515+++*****???|||||()()()()()") #ejemplo

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

#ejemplo 000000000000000000000000000000000000000000000000000000
estados = [0, 1, 2]
simbolos = ['a', 'b']
inicio = 0
aceptacion = [1]
transiciones = [(0, 'a', 1), (1, 'b', 2), (2, 'a', 0)]

export_automata(estados,simbolos,inicio,aceptacion,transiciones)
#ejemplo 111111111111111111111111111111111111111111111111111111
