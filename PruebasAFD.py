from AFD import AFD
import ast

class ClasePrueba:
    def __init__(self):
        pass
    
    def probarAFD(self):
        # Crear autómatas AFD
        afd1 = AFD(nombreArchivo='evenA.DFA')
        afd2 = AFD(nombreArchivo='evenB.DFA')
        
        # Procesar cadenas con y sin detalles
        cadena = 'aba'
        resultado_sin_detalles = afd1.procesar_cadena(cadena)
        resultado_sin_detalles1 = afd2.procesar_cadena(cadena)
        #resultado_con_detalles = afd1.procesar_cadena_con_detalles(cadena)
  
        print(f"Procesamiento sin detalles de la cadena '{cadena}': {resultado_sin_detalles}")
        print(f"Procesamiento sin detalles de la cadena '{cadena}': {resultado_sin_detalles1}")
        
        
        # print(f"Procesamiento con detalles de la cadena '{cadena}': {resultado_con_detalles}")

        # Procesar listas de cadenas
        lista_cadenas = ['aba', 'abbaa', 'abbabaabbbbb']
        nombre_archivo = 'resultados.txt'
        imprimir_pantalla = True
        afd1.procesarListaCadenas(lista_cadenas, nombre_archivo, imprimir_pantalla)
        
        # # Crear objetos a partir del procesamiento
        #objeto1 = ast.literal_eval(resultado_con_detalles)  # Convertir cadena a objeto
       # objeto2 = ast.literal_eval(resultado_sin_detalles)
        #print(f"Objeto procesado con detalles: {objeto1}")
        
        # Generar archivos
        # nombre_archivo1 = 'resultado_con_detalles.txt'
        nombre_archivo2 = 'resultado_sin_detalles.txt'
        #afd1.exportar(nombre_archivo1)
        afd2.exportar(nombre_archivo2)
        
   

# Crear instancia de la clase ClasePrueba y ejecutar el método correspondiente
clase_prueba = ClasePrueba()
clase_prueba.probarAFD()
