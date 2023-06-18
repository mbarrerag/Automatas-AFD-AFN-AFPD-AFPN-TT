from AFD import AFD
from AFN import AFN
from AFN_Lambda import AFN_Lambda
from AFPD import AFPD
from queue import LifoQueue
from Alfabeto import Alfabeto
import ast
import random

class ClasePrueba:
    def __init__(self):
        pass
    
    def probarAFD(self):
        # Crear autómatas AFD
        afd1 = AFD(nombreArchivo='AFDParAParB.txt')
        #afd1 = AFD(afd1.alfabeto,afd1.estados,afd1.estadoInicial,afd1.estadosAceptacion,afd1.delta)
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
        print(afd1)
   

    def ProbarAFN(self):

        afn1 = AFN(nombreArchivo='AFNTest.txt')
        alfabeto = Alfabeto(afn1.alfabeto)
        cadena = 'bbac'
        procesar_cadena = afn1.procesarCadena(cadena) 
        print(f"\nProcesamiento  de la cadena '{cadena}': {procesar_cadena}\n")
        print("\nProcesamiento un proesamiento de aceptacion \n")
        procesar_cadena_detalle = afn1.procesar_cadena_con_detalles(cadena)
        
        print("\nProcesamiento  posible de la cadena \n")
        procesamientos_posibles = afn1.computarTodosLosProcesamientos(cadena)

    
        print(f"\nProcesamiento  de lista de cadenas \n")
        lista_cadenas = [alfabeto.generar_cadena_aleatoria(3), alfabeto.generar_cadena_aleatoria(5), alfabeto.generar_cadena_aleatoria(10)]
        nombre_archivo = 'resultados_lista_de_cadenas.txt'
        imprimir_pantalla = True
        afn1.procesarListaCadenas(lista_cadenas, nombre_archivo, imprimir_pantalla)
        nombre_archivo1 = 'resultado_con_detalles.txt'
        nombre_archivo2 = 'procesamientos_posibles.txt'
        afn1.exportar(nombre_archivo1)
        afn1.exportar(nombre_archivo2)

    def probarAFNtoAFD(self):
         
         #afd1 = AFD(nombreArchivo='evenA.DFA')
         #afn1 = AFN(nombreArchivo='testAFN.NFA')  
         afn1 = AFN(nombreArchivo='conversionAFNtoAFDTest.txt')
         cadena = '000'  
         #procesar_cadena_afd1 = afd1.procesar_cadena(cadena)
         print(f"AFN procesando cadena {cadena} \n")
         procesar_cadena_afn1 = afn1.procesarCadena(cadena)
         print(procesar_cadena_afn1)
         print("\nAFN a AFD\n")
         afn_afd = afn1.AFNtoAFD()
         print(afn_afd)
         print("\nNuevo AFD procesando cadena\n")
         afd_nuevo_procesamiento = afn_afd.procesar_cadena(cadena)
         print(f"\nProcesamiento  de la cadena '{cadena}':\n Procesamiento AFN {procesar_cadena_afn1} \n Procesamiento nuevo AFD: {afd_nuevo_procesamiento} ")        
    
    def probarComplemento(self):
        afd1 = AFD(nombreArchivo='evenA.DFA')
        afd_complemento = afd1.hallarComplemento()
        print(f"AFD original '{afd1}'\n")
        print(f"\n\nAFD Complemento \n'{afd_complemento}'")

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
        print("\n\nDiagrama del Producto Cartesiano de la Diferencia simetrica con la Interseccion:")
        producto_cartesiano = afd1.hallarProductoCartesiano(interseccion, diferencia, 'interseccion')
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
    
    def validarAFNtoAFD(self):
         afn1 = AFN(nombreArchivo='testAFN.NFA') 
         afns =[afn1]
         lista_cadenas = clase_prueba.generar_cadenas_afn(afns)
         imprimir_pantalla = True
         print("Procesamiento AFN")
         contador_si_afn, contador_no_afn = afn1.procesarListaCadenas(lista_cadenas, 'resultados_AFN_cedenas_aleatorias.txt', imprimir_pantalla)
         print("AFN a AFD")
         afn_afd = afn1.AFNtoAFD()
         contador_si_afd, contador_no_afd = afn_afd.procesarListaCadenas(lista_cadenas, 'resultados_AFNtoAFD_cedenas_aleatorias.txt', imprimir_pantalla)
         print("Cantidad de cadenas aceptadas AFN :\n", contador_si_afn)
         print("Cantidad de cadenas rechazadas AFN:\n", contador_no_afn)
         print("Cantidad de cadenas aceptadas nuevo AFD :\n", contador_si_afd)
         print("Cantidad de cadenas rechazadas nuevo AFD:\n", contador_no_afd)

    def probarAFNLambda(self):
    # Crear autómatas AFN-λ
        #firstAFNL = AFN_Lambda(nombreArchivo="firstAFNLtest.NFE")
        secondAFNL = AFN_Lambda(nombreArchivo="secondAFNLtest.NFE")
        lambdaClosureAFNL = AFN_Lambda(nombreArchivo="lambdaClausuraTest.NFE")
        #toStringTestAFNL = AFN_Lambda(nombreArchivo="toStringTestAFNL")

        # Calcular la λ-clausura de un estado
        lambdaClosureState = lambdaClosureAFNL.calcularLambdaClausura(states=['s0'])
        print("Lambda clausura de 's0':", lambdaClosureState)

        # Calcular la λλ-clausura de un conjunto de estados
        lambdaClosureStates = lambdaClosureAFNL.calcularLambdaClausura(states=["s0", "s3"])
        print("Lambda clausura de ['s0', 's3']:", lambdaClosureStates)
        
        # Procesar cadenas mostrando solo un procesamiento de aceptación
        print("Procesamiento de '01112012' en secondAFNL:")
        result = secondAFNL.procesarCadena("01112012", True)
        print("Aceptada:", result)

        # Procesar cadenas mostrando todos los procesamientos posibles
        print("Procesar cadenas mostrando todos los procesamientos posibles en AFN-λ")
        result = secondAFNL.procesarCadenaConDetalles("102")
        print("Aceptada:", result)

        # # Consultar los procesamientos de aceptación, abortados y de rechazo
        print("Consultar los procesamientos de aceptación, abortados y de rechazo AFN-λ")
        result = secondAFNL.procesarCadena("2")
        print("Aceptada:", result)

        # # Procesar listas de cadenas
        # cadenas = ["0111012", "2", "11"]
        # for cadena in cadenas:
        #     print("Procesamiento de", cadena, "en secondAFNL:")
        #     result = secondAFNL.procesarCadena(cadena, True)
        #     print("Aceptada:", result)

        # # Generar archivos
        # with open("toStringTestAFNL.NFE", "w") as file:
        #     file.write(toStringTestAFNL.__str__())

    def probarAFPD(self):
        afpd1 = AFPD(nombreArchivo='AFPD_Test.txt')
        alfabeto = Alfabeto(afpd1.alfabeto)
        cadena = alfabeto.generar_cadena_aleatoria(5)
        print(cadena,end=" ")
        print(afpd1.procesarCadena(cadena))
        afpd1.procesarCadenaConDetalles(cadena)
    

# Llamar a la función para probar el producto cartesiano

# Crear instancia de la clase ClasePrueba y ejecutar los método correspondiente
clase_prueba = ClasePrueba()
#clase_prueba.probarAFD()
#clase_prueba.ProbarAFN()
#clase_prueba.probarAFNtoAFD()
#clase_prueba.probarComplemento()
#clase_prueba.probarProductoCartesiano()
#clase_prueba.probarSimplificacion()
#clase_prueba.validarAFNtoAFD()
#clase_prueba.probarAFNLambda()
clase_prueba.probarAFPD()