# Proyecto1: Teoria de la Computacion
Proyecto realizado para la construcción de autómatas a base de expresiones regulares, así como la verificación de palabras dentro de ese autómata.
### Se desarrollaron los algoritmos:
* Shunting Yard (regexp a postfix)
* Thompson-McNaughton-Yamada (regexp a AFN)
* Construcción de subconjuntos (AFN a AFD)
* Hopcroft (AFD a AFD minimal)

Para interactuar con el programa, se debe ejecutar el main.py. Ahí, se le pedirá ingresar una regexp o una palabra para verificar su aceptación dentro del autómata (construido a base de la regexp). Como salida, se obtendrá un .json descriptivo de cada uno de los autómatas, así como una imagen .png para la visualización de cada autómata.

### Requisitos: 
* Python (base, collections) instalado
* Graphviz instalado `https://graphviz.org/download/` & `pip install graphviz`
* Automathon instalado `pip install automathon`
  
### Recomendaciones:
- Utilizar la '?' para representar la cadena vacía épsilon. 
- La regexp a ingresar, para construir los autómatas, si tiene concatenación, escribir explícitamente cada concatenación con un '.'
- Las operaciones regexp aceptadas son: estrella de Kleene (*), suma de Kleene (+), concatenación (.), unión (|); el uso de paréntesis '()' también son aceptados.    
