#Se determinó que el épsilon (cadena vacía) será un '?'
 
def verificar_input(input:str):
    traduccion = str.maketrans('áéíóúüÁÉÍÓÚÜ','aeiouuAEIOUU')
    input.translate(traduccion)
    caracteres_permitidos = ['?','|','+','*','(',')']
    lista_filtrada = [item for item in input if not isinstance(item, str) or not item.isalnum()]
    verdad = input.isalnum() or all(i in caracteres_permitidos for i in lista_filtrada)
    print(f"Usted ingresó {input}, y su valor de aceptación es:", verdad)
    #tal vez verificar que todos los paréntesis estén en pares? (cerrados y abiertos)

verificar_input("aee1515+++*****???|||||()()()()()")

