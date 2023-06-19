from AFD import AFD
from AFPD import AFPD
from Alfabeto import Alfabeto

def main():
    # print("Pruebas\n")
    # print('\nPruebas de la clase AFD\n')

    # print("Revisar si el AFD esta completo y corregirlo")

    # alfabeto = ['a', 'b']
    # estados = ['s0', 's1']
    # estadoInicial = 's0'
    # estadosAceptacion = ['s0']
    # delta = {'s0': {'a': 's1'}, 's1': {'a': 's0', 'b': 's1'}}

    # automata = AFD(alfabeto=alfabeto, 
    #            estados=estados, 
    #            estadoInicial=estadoInicial, 
    #            estadosAceptacion=estadosAceptacion, 
    #            delta=delta)
    
    # automata.draw().render('automata Incompleto', view=True,format='png')
    # automata.verificarCorregirCompletitud()
    # print(automata) 
    # automata.draw().render('automata Completo', view=True, format='png')

    # print('Construir a partir de archivo\n')
    # automata = AFD(nombreArchivo='./Automatas_AFD/Automata_Incompleto.DFA')
    # print(automata)
    # automata.draw().render('automata Incompleto2', view=True, format='png')

    # print('Hallar estados limbo\n')
    # automata = AFD(nombreArchivo='./Automatas_AFD/Estados_Limbo.DFA')
    # print("Estados limbo: ", automata.hallarEstadosLimbo())
    # print(automata)

    # print('Hallar estados inaccesibles\n')
    # automata = AFD(nombreArchivo='./Automatas_AFD/Estados_Inaccesibles.DFA')
    # print("Estados inaccesibles: ", automata.hallarEstadosInaccesibles())
    # print(automata)

    # print('Imprimir automata simplificado y completo\n')
    # automata = AFD(nombreArchivo='./Automatas_AFD/Automata_Incompleto.DFA')
    # print(automata.imprimirAFDSimplificado())

    # print('Exportar a archivo\n')
    # automata = AFD(nombreArchivo='./Automatas_AFD/Automata_Incompleto.DFA')
    # automata.exportar('./Automatas_AFD/testAFDexport.DFA')

    # print('Procesar en detalle\n')
    # automata = AFD(nombreArchivo='./Automatas_AFD/EvenAs.DFA')
    # cadena = 'aabbaab'
    # print("\n", automata.procesar_cadena_con_detalles(cadena), "\n")

    # print('Procesar Lista de Cadenas\n')
    # automata = AFD(nombreArchivo='./Automatas_AFD/EvenAs.DFA')
    # listaCadenas = ['aabbaab', 'aabbaa', 'aabbaaba']
    # print("\n", automata.procesarListaCadenas(listaCadenas, None, True), "\n")

    # print('Hallar complemento\n')
    # automata = AFD(nombreArchivo='./Automatas_AFD/EvenAs.DFA')
    # automata.draw().render('automata original', view=True, format='png')
    # print(automata.hallarComplemento())
    # automata.hallarComplemento().draw().render('automata complemento', view=True, format='png')

    # print("Hallar ProductorCartesianoY\n")
    # automata1 = AFD(nombreArchivo='./Automatas_AFD/EvenAs.DFA')
    # automata2 = AFD(nombreArchivo='./Automatas_AFD/EvenBs.DFA')
    # CartesianoY = automata1.hallarProductoCartesianoY(automata1, automata2)
    # cadena = "baabbaab"
    # print(CartesianoY)
    # print(CartesianoY.procesar_cadena_con_detalles(cadena))
    # CartesianoY.draw().render('automata CartesianoY', view=True, format='png')

    # print("Hallar ProductoCartesianoO\n")
    # automata1 = AFD(nombreArchivo='./Automatas_AFD/EvenAs.DFA')
    # automata2 = AFD(nombreArchivo='./Automatas_AFD/EvenBs.DFA')
    # CartesianoO = automata1.hallarProductoCartesianoO(automata1, automata2)
    # cadena = "aabbbaab"
    # print(CartesianoO)
    # print(CartesianoO.procesar_cadena_con_detalles(cadena))
    # CartesianoO.draw().render('automata CartesianoO', view=True, format='png')

    # print("Hallar ProductoCartesianoDiferencia\n")
    # automata1 = AFD(nombreArchivo='./Automatas_AFD/EvenAs.DFA')
    # automata2 = AFD(nombreArchivo='./Automatas_AFD/EvenBs.DFA')
    # CartesianoDif = automata1.hallarProductoCartesianoDiferencia(automata1, automata2)
    # cadena = "aaabbab"
    # print(CartesianoDif)
    # print(CartesianoDif.procesar_cadena_con_detalles(cadena))
    # CartesianoDif.draw().render('automata CartesianoDif', view=True, format='png')

    # print("Hallar ProductoCartesianoDiferenciaSimetrica\n")
    # automata1 = AFD(nombreArchivo='./Automatas_AFD/EvenAs.DFA')
    # automata2 = AFD(nombreArchivo='./Automatas_AFD/EvenBs.DFA')
    # CartesianoDifSim = automata1.hallarProductoCartesianoDiferenciaSimetrica(automata1, automata2)
    # cadena = "aaabbbb"
    # print(CartesianoDifSim)
    # print(CartesianoDifSim.procesar_cadena_con_detalles(cadena))
    # CartesianoDifSim.draw().render('automata CartesianoDifSim', view=True, format='png')

    # print("Simplificar\n")
    # automata = AFD(nombreArchivo='./Automatas_AFD/Min_Test.DFA')
    # automata.draw().render('automata originalMin', view=True, format='png')
    # automata.simplificarAFD()
    # print(automata)
    
    # print('\nPruebas de la clase AFPD\n') 
    #  
    """""
    print("Veriificar Determinimo\n")

    print("Construir a partir de archivo\n") 

    afpd1 = AFPD(nombreArchivo='AFPD_Test.txt')
    afpd2 = AFPD(nombreArchivo='AFPD_Test2.txt')
    alfabeto = Alfabeto(afpd1.alfabetoCinta)
    cadena = alfabeto.generar_cadena_aleatoria(5)
    print("Imprimir automata\n")
    print(afpd1)
    print(afpd2)

    print("Procesamiento con detalle\n")

    afpd1.procesarCadenaConDetalles(cadena)
    
    print("Procesamiento de lista de cadenas\n")
    
    afpd1.procesarListaCadenas([alfabeto.generar_cadena_aleatoria(7),alfabeto.generar_cadena_aleatoria(2),alfabeto.generar_cadena_aleatoria(3)], "ResultadosAFPD.txt", True)    
    """
main()
