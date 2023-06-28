from AFD import AFD
from AFN import AFN
#from AFN_Lambda import AFN_Lambda
from AFPD import AFPD
from AFPN import AFPN
from queue import LifoQueue
from Alfabeto import Alfabeto
from MT import MT
import ast
import random
from graphviz import Digraph

class ClasePrueba:
    def __init__(self):
        pass
    
    def probarAFD(self):
        # Crear autómatas AFD
        #afd1 = AFD(nombreArchivo='evenA.DFA')
        #afd1 = AFD(nombreArchivo='evenB.DFA')
        #afd1 = AFD(nombreArchivo='testAFD.DFA')
        afd1 = AFD(nombreArchivo='testAFD2.DFA')

        #afd1 = AFD(afd1.alfabeto,afd1.estados,afd1.estadoInicial,afd1.estadosAceptacion,afd1.delta)
        # Procesar cadenas con y sin detalles
    
        cadena = 'aba'
        resultado_sin_detalles = afd1.procesar_cadena(cadena)
        resultado_con_detalles = afd1.procesar_cadena_con_detalles(cadena)
  
        print(f"\n--Procesamiento sin detalles de la cadena '{cadena}': {resultado_sin_detalles}")
        print(f"\n--Procesamiento con detalles de la cadena '{cadena}': {resultado_con_detalles}")
        # Procesar listas de cadenas
        print("\n--Procesamiento de lista de cadenas\n")
        lista_cadenas = ['aba', 'abbaa', 'abbabaabbbbb']
        nombre_archivo = 'resultados_lista_de_cadenas.txt'
        imprimir_pantalla = True
        afd1.procesarListaCadenas(lista_cadenas, nombre_archivo, imprimir_pantalla)
        
        # Generar archivos
        nombre_archivo1 = 'resultado_con_detalles.txt'
        nombre_archivo2 = 'resultado_sin_detalles.txt'
        afd1.exportar(nombre_archivo1)
        afd1.exportar(nombre_archivo2)
        print("\n--AFD\n")
        print(afd1)
        print("\n--AFD Completitud\n")
        print(afd1.verificarCorregirCompletitud())
        print("\n--AFD Imprimir simplificado\n")
        print(afd1.imprimirAFDSimplificado())
        print("\n--AFD Simplificado\n")
        print(afd1.simplificarAFD())  
   

    def ProbarAFN(self):
        afn = AFN(nombreArchivo='AFNTest.txt')
        while(True):
            tipoPrueba =  int(input('''Escoja la prueba que desea realizar:
            \n 1) Imprimir AFN.
            \n 2) Imprimir simplificado AFN.
            \n 3) Estados inaccesibles AFN.
            \n 4) Exportar AFN.
            \n 5) Procesar cadena con detalle AFN.
            \n 6) Computar todos los procesamientos AFN.
            \n 7) Procesar lista cadenas AFN.
            \n 8) AFN to AFD.
            \n 0) Acabar.
            '''))
            if tipoPrueba == 1:
                print(afn)
            elif tipoPrueba == 2:
                afn.imprimirAFNSimplificado()
            elif tipoPrueba == 3:
                print('Estados inaccesibles: ' + afn.hallarEstadosInaccesibles())
            elif tipoPrueba == 4:
                afn.exportar()
                print("AFN exportado")
            elif tipoPrueba == 5:
                afn.procesar_cadena_con_detalles(cadena=input('Cadena: '))
            elif tipoPrueba == 6:
                afn.computarTodosLosProcesamientos(cadena=input('Cadena: '), nombreArchivo='Todos los procesamientos AFN')
            elif tipoPrueba == 7:
                listaCadenas = []
                while(True):
                    nuevaCadena = input("Nueva cadena: ")
                    if nuevaCadena != '$':
                        listaCadenas.append(nuevaCadena)
                    else:
                        break
                afn.procesarListaCadenas(listaCadenas = listaCadenas, nombreArchivo='Lista cadenas AFN', imprimirPantalla=True)
            elif tipoPrueba == 8:
                afd = afn.AFNtoAFD() 
                afn.procesarCadenaConDetallesConversion(cadena=input('Cadena: '))
                listaCadenas = []
                while(True):
                    nuevaCadena = input("Nueva cadena: ")
                    if nuevaCadena != '$':
                        listaCadenas.append(nuevaCadena)
                    else:
                        break
                afn.procesarListaCadenasConversion(listaCadenas=listaCadenas, nombreArchivo='Lista cadenas conversion AFN', imprimirPantalla=True)
            else:
                break

    def simplificacionAFN(self):
        afn1 = AFN(nombreArchivo='AFNTest.txt')
        print("\n--AFN Simplificado\n")
        afn1.imprimirAFNSimplificado()

    def probarAFNtoAFD(self):
         
         #afd1 = AFD(nombreArchivo='evenA.DFA')
         #afn1 = AFN(nombreArchivo='testAFN.NFA')  
         #afn1 = AFN(nombreArchivo='conversionAFNtoAFDTest.txt')
         print("--AFN\n")
         afn1 = AFN(nombreArchivo='AFNTest - copia.txt') 
         cadena = 'dba'  
         #procesar_cadena_afd1 = afd1.procesar_cadena(cadena)
         print(f"AFN procesando cadena {cadena} \n")
         procesar_cadena_afn1 = afn1.procesarCadena(cadena)
         print(procesar_cadena_afn1)
         print("\n--AFN a AFD\n")
         afn_afd = afn1.AFNtoAFD()
         print(afn_afd)
         print("\n--Nuevo AFD procesando cadena con detalle\n")
         afd_nuevo_procesamiento = afn_afd.procesar_cadena_con_detalles(cadena)
         print(f"\n--Procesamiento  de la cadena '{cadena}':\n Procesamiento AFN {procesar_cadena_afn1} \n Procesamiento nuevo AFD con detalle: {afd_nuevo_procesamiento} ")        
         print("\n--Procesamiento de lista de cadenas del nuevo AFD\n")
         lista_cadenas = ['aba', 'abbaa', 'abbabaabbbbb']
         nombre_archivo = 'resultados_lista_de_cadenas.txt'
         imprimir_pantalla = True
         afn_afd.procesarListaCadenas(lista_cadenas, nombre_archivo, imprimir_pantalla)
         afn1.draw_nfa().render('automata CartesianoDifSim', view=True, format='png')


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
        afd4 = AFD(nombreArchivo='minTest.DFA')
        print(f"\nAFD original \n")
        print(afd4)
        afd4.simplificarAFD()
        print(f"\nSimplificacion\n")
        print(afd4)
    def generar_cadenas_afn(self,afns):
        #Me gustaría que se generaran cadenas dependiendo del lenguaje de los afns (no todos tienen de lenguaje {a,b}) para poder hacer más pruebas
        cadenas_generadas = []
        for afn in afns:
            for _ in range(1000):
                tamano = random.randint(1, 10)  # Choose the size randomly
                cadena = ''.join(random.choices(['a', 'b'], k=tamano))  # Generate a random string
                print(cadena)
                cadenas_generadas.append(cadena)
        return cadenas_generadas
    
    def validarAFNtoAFD(self):
         afn1 = AFN(nombreArchivo='testAFN.NFA') 
         afd2 = AFD(nombreArchivo='evenA.DFA')
         afn3 = AFN(nombreArchivo='testAFN.NFA')  
         afn4 = AFN(nombreArchivo='conversionAFNtoAFDTest.txt')
         afn5 = AFN(nombreArchivo='AFNTest - copia.txt') 
         afns =[afn1,afd2,afn3,afn4,afn5]
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
        #firstAFNL = AFN_Lambda(nombreArchivo="LambdafFirstTest.NFE")
        secondAFNL = AFN_Lambda(nombreArchivo="LambdaSecondTest.NFE")
        lambdaClosureAFNL = AFN_Lambda(nombreArchivo="lambdaClausuraTest.NFE")
        #LambdaToStringTest = AFN_Lambda(nombreArchivo="LambdaToStringTest")

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
        # with open("LambdaToStringTest.NFE", "w") as file:
        #     file.write(LambdaToStringTest.__str__())

    def probarAFPD(self):
        afpd1 = AFPD(nombreArchivo='AFPD_Test.PDA')
        alfabeto = Alfabeto(afpd1.alfabetoCinta)
        cadena = alfabeto.generar_cadena_aleatoria(5)
        print("Procesamiento con detalle\n")
        afpd1.procesarCadenaConDetalles(cadena)
        print("Procesamiento de lista de cadenas\n")
        afpd1.procesarListaCadenas([alfabeto.generar_cadena_aleatoria(7),alfabeto.generar_cadena_aleatoria(2),alfabeto.generar_cadena_aleatoria(3)], "ResultadosAFPD.txt", True)
    
    def probarAFPDProductoCartesianoAFD(self):
        afd1 = AFD(nombreArchivo='AFDParAParB.DFA')
        afpd2 = AFPD(nombreArchivo='AFPD_Test.PDA')
        
        #print(afd1.alfabeto,afpd2.alfabetoCint[a)
        #print(afpd2.delta)
        afd_resultado = afpd2.hallarProductoCartesiano(afd1, afpd2, 'Y')
        print(afd_resultado)

<<<<<<< Updated upstream
   def probarAFPN(self):
        afpn = AFPN(nombreArchivo='testAFPN.pda')
        while(True):
            tipoPrueba =  int(input('''Escoja la prueba que desea realizar:
            \n 1) Imprimir AFPN.
            \n 2) Exportar AFPN.
            \n 3) Procesar cadena con detalle AFPN.
            \n 4) Computar todos los procesamientos AFPN.
            \n 5) Procesar lista cadenas AFPN.
            \n 6) Producto carteciano AFPN con AFD.
            \n 0) Acabar.
            '''))
            if tipoPrueba == 1:
                print(afpn)
            elif tipoPrueba == 2:
                afpn.exportar()
                print("AFPN exportado")
            elif tipoPrueba == 3:
                afpn.procesarCadenaConDetalle(cadena=input('Cadena: '))
            elif tipoPrueba == 4:
                afpn.computarTodosLosProcesamientos(cadena=input('Cadena: '), nombreArchivo='Todos los procesamientos AFPN')
            elif tipoPrueba == 5:
                listaCadenas = []
                while(True):
                    nuevaCadena = input("Nueva cadena: ")
                    if nuevaCadena != '$':
                        listaCadenas.append(nuevaCadena)
                    else:
                        break
                afpn.procesarListaCadenas(listaCadenas = listaCadenas)
            elif tipoPrueba == 6:
                afd = AFD(nombreArchivo='testAFD.DFA')
                print(afpn.hallarProductoCartesianoConAFD(afd=afd))
            else:
                break
=======
    def probarAFPN(self):
        afpn= AFPN(nombreArchivo='testAFPN.pda')
        afpn.draw_npfa().render('automata CartesianoY3ds4', view=True, format='png')
        print(afpn)
        afpn.exportar()
        afpn.procesarCadenaConDetalle(cadena='abaabbab')
        afpn.procesarCadenaConDetalle(cadena='aaabbb')
        afpn.computarTodosLosProcesamientos(cadena='aaabbb')
        afpn.procesarListaCadenas(listaCadenas=['abaa', '', 'aaaabbbb'])
        afd= AFD(nombreArchivo='testAFD.DFA')
        print(afpn.hallarProductoCartesianoConAFD(afd=afd))
>>>>>>> Stashed changes

    def probarMT(self):
        #prueba usando TM de palindromes pares

        Turing = MT(nombreArchivo="MT.tm")  
        print(Turing.procesarCadenaConDetalles("ababa"))
        print(Turing.procesarCadena("ababa"))
        print(Turing.procesarFuncion("aabbaa"))
        Turing.procesarListaCadenas(["aaaa", "aabbaa", "ababa"], "resultadosTM.txt", True)
        print(Turing)
        
# Llamar a la función para probar el producto cartesiano

# Crear instancia de la clase ClasePrueba y ejecutar los método correspondiente
clase_prueba = ClasePrueba()
#-------------AFD-----------------
#clase_prueba.probarAFD()
#clase_prueba.probarComplemento()
#clase_prueba.probarSimplificacion()
#clase_prueba.probarProductoCartesiano()
#-------------AFN-----------------
# clase_prueba.ProbarAFN()
# clase_prueba.simplificacionAFN()
# clase_prueba.probarAFNtoAFD()
# clase_prueba.validarAFNtoAFD() #validacion con mas de 5000 cadenas

#------------AFNL--------------


#------------
#clase_prueba.probarProductoCartesiano()
#clase_prueba.probarSimplificacion()

#------------AFNL--------------


#clase_prueba.probarAFNLambda()
#-------------AFPD-----------------
#clase_prueba.probarAFPD()

#clase_prueba.probarAFPDProductoCartesianoAFD()

# clase_prueba.probarAFPDProductoCartesianoAFD()
#-------------AFPN-----------------
clase_prueba.probarAFPN()
#--------------MT------------------
#clase_prueba.probarMT()

#clase_prueba.probarAFPDProductoCartesianoAFD()
