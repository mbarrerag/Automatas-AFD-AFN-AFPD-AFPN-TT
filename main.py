from AFD import AFD



def main():
    print("Pruebas\n")
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
    
    # automata.verificarCorregirCompletitud()
    # print(automata) 

    # print('Construir a partir de archivo\n')
    # automata = AFD(nombreArchivo='./Automatas_AFD/Automata_Incompleto.DFA')
    # print(automata)

    # print('Hallar estados limbo\n')
    # automata = AFD(nombreArchivo='./Automatas_AFD/Estados_Limbo.DFA')
    # print("Estados limbo: ", automata.hallarEstadosLimbo())

    # print('Hallar estados inaccesibles\n')
    # automata = AFD(nombreArchivo='./Automatas_AFD/Estados_Inaccesibles.DFA')
    # print("Estados inaccesibles: ", automata.hallarEstadosInaccesibles())

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
    # print(automata.hallarComplemento())

    # print("Hallar ProductorCartesianoY\n")
    # automata1 = AFD(nombreArchivo='./Automatas_AFD/EvenAs.DFA')
    # automata2 = AFD(nombreArchivo='./Automatas_AFD/EvenBs.DFA')
    # CartesianoY = automata1.hallarProductoCartesianoY(automata1, automata2)
    # cadena = "baabbaab"
    # print(CartesianoY)
    # print(CartesianoY.procesar_cadena_con_detalles(cadena))

    # print("Hallar ProductoCartesianoO\n")
    # automata1 = AFD(nombreArchivo='./Automatas_AFD/EvenAs.DFA')
    # automata2 = AFD(nombreArchivo='./Automatas_AFD/EvenBs.DFA')
    # CartesianoO = automata1.hallarProductoCartesianoO(automata1, automata2)
    # cadena = "aabbab"
    # print(CartesianoO)
    # print(CartesianoO.procesar_cadena_con_detalles(cadena))

    # print("Hallar ProductoCartesianoDiferencia\n")
    # automata1 = AFD(nombreArchivo='./Automatas_AFD/EvenAs.DFA')
    # automata2 = AFD(nombreArchivo='./Automatas_AFD/EvenBs.DFA')
    # CartesianoDif = automata1.hallarProductoCartesianoDiferencia(automata1, automata2)
    # cadena = "aaabbbab"
    # print(CartesianoDif)
    # print(CartesianoDif.procesar_cadena_con_detalles(cadena))

    # print("Hallar ProductoCartesianoDiferenciaSimetrica\n")
    # automata1 = AFD(nombreArchivo='./Automatas_AFD/EvenAs.DFA')
    # automata2 = AFD(nombreArchivo='./Automatas_AFD/EvenBs.DFA')
    # CartesianoDifSim = automata1.hallarProductoCartesianoDiferenciaSimetrica(automata1, automata2)
    # cadena = "aaabbbb"
    # print(CartesianoDifSim)
    # print(CartesianoDifSim.procesar_cadena_con_detalles(cadena))

    # print("Simplificar\n")
    # automata = AFD(nombreArchivo='./Automatas_AFD/Min_Test.DFA')
    # automata.simplificarAFD()
    # print(automata)


main()
