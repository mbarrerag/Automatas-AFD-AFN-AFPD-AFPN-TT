from AFD import AFD
from AFN import AFN
import random
import ast

class ClasePrueba:
    def __init__(self):
        pass
    
    def probarAFD(self):
        # Crear autómatas AFD
        afd1 = AFD(nombreArchivo='evenA.DFA')
        
        # Procesar cadenas con y sin detalles
        cadena = 'aba'
        resultado_sin_detalles = afd1.procesar_cadena(cadena)
        resultado_con_detalles = afd1.procesar_cadena_con_detalles(cadena)
  
        print(f"Procesamiento sin detalles de la cadena '{cadena}': {resultado_sin_detalles}")
        print(f"Procesamiento sin detalles de la cadena '{cadena}': {resultado_con_detalles}")
        
        # Procesar listas de cadenas
        lista_cadenas = ['aba', 'abbaa', 'abbabaabbbbb']
        nombre_archivo = 'resultados_lista_de_cadenas.txt'
        imprimir_pantalla = True
        afd1.procesarListaCadenas(lista_cadenas, nombre_archivo, imprimir_pantalla)

        # Generar archivos
        nombre_archivo1 = 'resultado_con_detalles.txt'
        nombre_archivo2 = 'resultado_sin_detalles.txt'
        afd1.exportar(nombre_archivo1)
        afd1.exportar(nombre_archivo2)
      
        
   

    def ProbarAFN(self):
        
        afn1 = AFN(nombreArchivo='testAFN.NFA')   

        cadena = 'abbaa'
        procesar_cadena = afn1.procesarCadena(cadena) 
        print(f"Procesamiento  de la cadena '{cadena}': {procesar_cadena}")
        procesar_cadena_detalle = afn1.procesar_cadena_con_detalles(cadena)
        procesamientos_posibles = afn1.computarTodosLosProcesamientos(cadena)
        lista_cadenas = ['aba', 'abbaa', 'abbabaabbbbb']
        nombre_archivo = 'resultados_lista_de_cadenas.txt'
        imprimir_pantalla = True
        afn1.procesarListaCadenas(lista_cadenas, nombre_archivo, imprimir_pantalla)

        nombre_archivo1 = 'resultado_con_detalles.txt'
        nombre_archivo2 = 'procesamientos_posibles.txt'
        afn1.exportar(nombre_archivo1)
        afn1.exportar(nombre_archivo2)

    def probarAFNtoAFD(self):
         
         afd1 = AFD(nombreArchivo='evenA.DFA')
         afn1 = AFN(nombreArchivo='testAFN.NFA')   
         cadena = 'abb'  
         procesar_cadena_afd1 = afd1.procesar_cadena(cadena)
         procesar_cadena_afn1 = afn1.procesarCadena(cadena)
         print(f"\nProcesamiento  de la cadena '{cadena}':\n Procesamiento AFD: {procesar_cadena_afd1} \n Procesamiento AFN {procesar_cadena_afn1} \n")
         print("AFN a AFD")
         afn_afd = afn1.AFNtoAFD()
         afd_nuevo_procesamiento = afn_afd.procesar_cadena(cadena)
         print(f"\nProcesamiento  de la cadena '{cadena}':\n Procesamiento nuevo AFD: {afd_nuevo_procesamiento} \n Procesamiento AFN {procesar_cadena_afn1}")
         
    def probarComplemento(self):
        afd1 = AFD(nombreArchivo='evenA.DFA')
        afd_complemento = afd1.hallarComplemento()
        print(f"AFD original '{afd1}'\n")
        print(f"\n\nAFD Complemento '{afd_complemento}'")

    def probarProductoCartesiano(self):
        # Crear los AFD a partir de los archivos
        afd1 = AFD(nombreArchivo='evenA.DFA')
        afd2 = AFD(nombreArchivo='evenB.DFA')

        # Producto cartesiano con intersección (∩)
        interseccion = afd1.hallarProductoCartesiano(afd1, afd2, 'interseccion')
        print("\n\nProducto Cartesiano con Interseccion:")
        print(interseccion)

        # Producto cartesiano con unión (∪)
        union = afd1.hallarProductoCartesiano(afd1, afd2, 'union')
        print("\n\nProducto Cartesiano con Union:")
        print(union)

        # # Producto cartesiano con diferencia (-)
        diferencia = afd1.hallarProductoCartesiano(afd1, afd2, 'diferencia')
        print("\n\nProducto Cartesiano con Diferencia Simetrica:")
        print(diferencia)

        # Dibujar el AFD resultante del producto cartesiano con intersección (∩)
        print("\n\nDiagrama del Producto Cartesiano con Intersección:")
        producto_cartesiano = afd1.hallarProductoCartesiano(union, diferencia, 'interseccion')
        print(producto_cartesiano)

    def probarSimplificacion(self):
        afd1 = AFD(nombreArchivo='evenA.DFA')
        cadena = 'aaabbb'
        print(f"\nAFD original '{afd1}'\n\n")
        afd1.simplificarAFD()
        afd1_simplificado = afd1
        print(f"\nSimplificacion '{afd1_simplificado}'\n")
        afd1_simplificado.procesar_cadena(cadena)
    
    def generar_cadenas_afn(self,afns):
        cadenas_generadas = []
        for afn in afns:
            for _ in range(5000):
                tamano = random.randint(1, 10)  # Choose the size randomly
                cadena = ''.join(random.choices(['a', 'b'], k=tamano))  # Generate a random string
                print(cadena)
                cadenas_generadas.append(cadena)
        return cadenas_generadas
    
    def afn_to_afd_aleatorio(self):
         afn1 = AFN(nombreArchivo='testAFN.NFA') 
         afns =[afn1,afn1]
         lista_cadenas = clase_prueba.generar_cadenas_afn(afns)
         nombre_archivo = 'resultados_AFN_cedenas_aleatorias.txt'
         imprimir_pantalla = True
         print("Procesamiento AFN")
         #afn1.procesarListaCadenas(lista_cadenas, nombre_archivo, imprimir_pantalla)
         print("AFN a AFD")
         afn_afd = afn1.AFNtoAFD()
         #nombre_archivo = 'resultados_AFNtoAFD_cedenas_aleatorias.txt'
         #afn_afd.procesarListaCadenas(['aba','abbaa'], nombre_archivo, imprimir_pantalla)
# Llamar a la función para probar el producto cartesiano

# Crear instancia de la clase ClasePrueba y ejecutar los método correspondiente
clase_prueba = ClasePrueba()
#clase_prueba.probarAFD()
#clase_prueba.ProbarAFN()
#clase_prueba.probarAFNtoAFD()
#clase_prueba.probarComplemento()
#clase_prueba.probarProductoCartesiano()
#clase_prueba.probarSimplificacion()
clase_prueba.afn_to_afd_aleatorio()