import ast

class AFD:
    def __init__(self, alfabeto=None, estados=None, estadoInicial=None, estadosAceptacion=None, delta=None, nombreArchivo=None):
        if nombreArchivo:
            self.cargar_desde_archivo(nombreArchivo)
            
        else:
            self.alfabeto = alfabeto
            self.estados = estados
            self.estadoInicial = estadoInicial
            self.estadosAceptacion = estadosAceptacion
            self.delta = delta
            self.estadosLimbo = []
            self.estadosInaccesibles = []
            

    def __str__(self):
        output = "!DFA\n"
        output += "#alphabet\n"
        start = min(self.alfabeto)
        end = max(self.alfabeto)
        output += f"{start}-{end}\n"
        output += "#states\n"
        estados_str = [str(estado) for estado in self.estados]
        output += "\n".join(estados_str) + "\n"
        

        output += "#initial\n"
        estadoInicial_str = [str(estado) for estado in self.estadoInicial]
        output += "\n".join(estadoInicial_str) + "\n"


        output += "#accepting\n"
        estadosAceptacion_str = [str(estado) for estado in self.estadosAceptacion]  
        output += "\n".join(estadosAceptacion_str) + "\n"
        output += "#transitions\n"
        for source, transitions in self.delta.items():
            for letter, target in transitions.items():
                output += f"{source}:{letter}>{target}\n"
        
        output += "#inaccessible\n"
        output += "\n".join(sorted(self.estadosInaccesibles)) + "\n"
        output += "#limbo\n"
        output += "\n".join(sorted(self.estadosLimbo)) + "\n"

        return output

    def imprimirAFDSimplificado(self):
        output = "!DFA\n"  
        output += "#states\n"
        output += "\n".join(sorted(self.estados)) + "\n" 
        output += "#initial\n"
        output += str(self.estadoInicial[0]) + "\n"
        output += "#accepting\n"
        output += "\n".join(sorted(self.estadosAceptacion)) + "\n"
        output += "#transitions\n"
        for source, transitions in self.delta.items():
            for letter, target in transitions.items():
                output += f"{source}:{letter}>{target}\n"
        
        return output

        
    def verificarCorregirCompletitud(self):
        for estado in self.estados:
            if estado not in self.delta:
                self.delta[estado] = {}
                for simbolo in self.alfabeto:
                    self.delta[estado][simbolo] = 'limbo'
                self.estadosLimbo.append(estado)
        return self.estadosLimbo


    def hallarEstadosLimbo(self):
        for estado in self.estados:
            if estado not in self.delta:
                self.estadosLimbo.append(estado)
        return self.estadosLimbo
    
    
    def hallarEstadosInaccesibles(self):
        self.estadosInaccesibles = self.estados.copy()
        self.estadosInaccesibles.remove(self.estadoInicial[0])
        for estado in self.estados:
            if estado in self.delta:
                for transicion in self.delta[estado]:
                    if self.delta[estado][transicion] in self.estadosInaccesibles:
                        self.estadosInaccesibles.remove(self.delta[estado][transicion])
        return self.estadosInaccesibles




    def cargar_desde_archivo(self, nombreArchivo):
        self.alfabeto = []
        self.estados = []
        self.estadoInicial = []
        self.estadosAceptacion = []
        self.delta = {}
        self.estadosLimbo = []
        self.estadosInaccesibles = []
        with open(nombreArchivo, 'r') as f:
            lines = f.readlines()

            for i in range(len(lines)):
                    if lines[i].strip() == '#alphabet':
                        letter_range = lines[i+1].strip()
                        start, end = letter_range.split('-')
                        self.alfabeto = [chr(x) for x in range(ord(start), ord(end) + 1)]
                        i += 1

                    if lines[i].strip() == '#states':
                        while lines[i+1].strip() != '#initial':
                            self.estados.append(lines[i+1].strip())
                            i += 1
                    
                    if lines[i].strip() == '#initial':
                        self.estadoInicial.append(lines[i+1].strip())
                        i += 1
                    
                    if lines[i].strip() == '#accepting':
                        while lines[i+1].strip() != '#transitions':
                            self.estadosAceptacion.append(lines[i+1].strip())
                            i += 1

                    if lines[i].strip() == '#transitions':
                        while i < len(lines) and lines[i+1].strip() != '':
                            source, letter = lines[i+1].strip().split(':')
                            letter, target = letter.split('>')
                            if source not in self.delta:
                                self.delta[source] = {}
                            self.delta[source][letter] = target
                            i += 1

    def exportar(self, nombreArchivo):
        with open(nombreArchivo, 'w') as f:
            f.write(str(self))

    def procesar_cadena(self, cadena):
        estadoActual = self.estadoInicial[0]
        for simbolo in cadena:
            estadoActual = self.delta[estadoActual][simbolo]
        return estadoActual in self.estadosAceptacion
    
    def procesar_cadena_con_detalles(self, cadena):
        estadoInicial_str = [tuple(estado) for estado in self.estadoInicial]
        estadoActual = tuple(estadoInicial_str[0])

        for simbolo in cadena:
            print(f"{estadoActual},{simbolo} --> {self.delta[estadoActual][simbolo]}")
            estadoActual = self.delta[estadoActual][simbolo]
        return estadoActual in self.estadosAceptacion
    
    def procesar_cadena_con_detalles_print(self, cadena):
        estadoActual = self.estadoInicial[0]
        procesamiento = f"{estadoActual}"
        for simbolo in cadena:
            procesamiento += f",{simbolo} --> {self.delta[estadoActual][simbolo]}"
            estadoActual = self.delta[estadoActual][simbolo]
        return procesamiento 
    
# procesarListaCadenas(listaCadenas,nombreArchivo, imprimirPantalla): procesa
# cada cadenas con detalles pero los resultados deben ser impresos en un archivo
# cuyo nombre es nombreArchivo; si este es inválido se asigna un nombre por
# defecto. Además, todo esto debe ser impreso en pantalla de acuerdo al valor del
# Booleano imprimirPantalla. Los campos deben estar separados por tabulación y
# son:
# ▪ cadena,
# ▪ sucesión de parejas (estado, símbolo) de cada paso del procesamiento .
# ▪ sí o no dependiendo de si la cadena es aceptada o no.

    def procesarListaCadenas(self, listaCadenas, nombreArchivo, imprimirPantalla):
        # Verify if the filename is valid, otherwise assign a default name
        if not nombreArchivo or not nombreArchivo.strip():
            nombreArchivo = "resultados.txt"

        # Process each cadena in the list
        with open(nombreArchivo, 'w') as archivo:
            for cadena in listaCadenas:
                detalles = self.procesar_cadena_con_detalles_print(cadena)  # Assuming self.procesarCadena() is the method for processing each cadena

                resultado = "si" if detalles else "no"  # Update the logic here based on the expected result
                linea = f"{cadena}\t{detalles}\t{resultado}"

                # Write to the file
                archivo.write(linea + '\n')

                # Print to the screen if indicated
                if imprimirPantalla:
                    print(linea)

    def hallarComplemento(self):
        complemento = AFD()  
        complemento.alfabeto = self.alfabeto.copy() 

        complemento.estados = self.estados.copy()

        complemento.estadoInicial = self.estadoInicial.copy()

        complemento.estadosAceptacion = set(self.estados.copy()) - set(self.estadosAceptacion.copy()) 

        complemento.delta = self.delta.copy()

        return complemento
    
    def hallarProductoCartesianoY(self, afd1, afd2):
        producto_cartesiano = AFD()  

        producto_cartesiano.alfabeto = afd1.alfabeto
        print(producto_cartesiano.alfabeto)


        producto_cartesiano.estados = {(estado1, estado2) for estado1 in afd1.estados for estado2 in afd2.estados}


        producto_cartesiano.estadoInicial = {(estado1, estado2) for estado1 in afd1.estadoInicial for estado2 in afd2.estadoInicial}


        producto_cartesiano.estadosAceptacion = {(estado1, estado2) for estado1 in afd1.estadosAceptacion for estado2 in afd2.estadosAceptacion}

        producto_cartesiano.delta = {}
        for estado1 in afd1.estados:
            for estado2 in afd2.estados:
                producto_cartesiano.delta[(estado1, estado2)] = {}
                for simbolo in producto_cartesiano.alfabeto:
                    producto_cartesiano.delta[(estado1, estado2)][simbolo] = (afd1.delta[estado1][simbolo], afd2.delta[estado2][simbolo])

        return producto_cartesiano

    def hallarProductoCartesianoO(self, afd1, afd2):
        producto_cartesiano = AFD()  

        producto_cartesiano.alfabeto = afd1.alfabeto


        producto_cartesiano.estados = {(estado1, estado2) for estado1 in afd1.estados for estado2 in afd2.estados}


        producto_cartesiano.estadoInicial = {(estado1, estado2) for estado1 in afd1.estadoInicial for estado2 in afd2.estadoInicial}


        producto_cartesiano.estadosAceptacion = {(estado1, estado2) for estado1 in afd1.estados for estado2 in afd2.estados if estado1 in afd1.estadosAceptacion or estado2 in afd2.estadosAceptacion}

        producto_cartesiano.delta = {}
        for estado1 in afd1.estados:
            for estado2 in afd2.estados:
                producto_cartesiano.delta[(estado1, estado2)] = {}
                for simbolo in producto_cartesiano.alfabeto:
                    producto_cartesiano.delta[(estado1, estado2)][simbolo] = (afd1.delta[estado1][simbolo], afd2.delta[estado2][simbolo])

        return producto_cartesiano
    
    def hallarProductoCartesianoDiferencia(self, afd1, afd2):
        producto_cartesiano = AFD()  

        producto_cartesiano.alfabeto = afd1.alfabeto


        producto_cartesiano.estados = {(estado1, estado2) for estado1 in afd1.estados for estado2 in afd2.estados}


        producto_cartesiano.estadoInicial = {(estado1, estado2) for estado1 in afd1.estadoInicial for estado2 in afd2.estadoInicial}


        producto_cartesiano.estadosAceptacion = {(estado1, estado2) for estado1 in afd1.estados for estado2 in afd2.estados if estado1 in afd1.estadosAceptacion and estado2 not in afd2.estadosAceptacion}

        producto_cartesiano.delta = {}
        for estado1 in afd1.estados:
            for estado2 in afd2.estados:
                producto_cartesiano.delta[(estado1, estado2)] = {}
                for simbolo in producto_cartesiano.alfabeto:
                    producto_cartesiano.delta[(estado1, estado2)][simbolo] = (afd1.delta[estado1][simbolo], afd2.delta[estado2][simbolo])

        return producto_cartesiano
    
    def hallarProductoCartesiano(self,afd1,afd2, operacion):
        if operacion == 'interseccion':
            return self.hallarProductoCartesianoY(afd1,afd2)
        elif operacion == 'union':
            return self.hallarProductoCartesianoO(afd1,afd2)
        elif operacion == 'diferencia':
            return self.hallarProductoCartesianoDiferencia(afd1,afd2)
        else:
            print("Operacion no valida")

        
    


    
print("start test:")
afd = AFD(nombreArchivo='testAFD.DFA')
afd1 = AFD(nombreArchivo='evenA.DFA')
afd2 = AFD(nombreArchivo='evenB.DFA')
#afd.verificarCorregirCompletitud()
#afd.hallarEstadosLimbo()
#afd.hallarEstadosInaccesibles()

#print(afd)
#print(afd.imprimirAFDSimplificado())
#afd.exportar('testAFD2.DFA')
#print(afd.procesar_cadena('aba'))
#print(afd1.procesar_cadena_con_detalles('abbaaa'))
#print(afd2.procesar_cadena_con_detalles('abbabaabbbbb'))
#print(afd.procesar_cadena_con_detalles('aba'))

#afd.procesarListaCadenas(['aba','abbaa'], 'resultados.txt', True)
#print(afd.hallarComplemento())
#print(afd.hallarProductoCartesianoY(afd1,afd2))
#print(afd.hallarProductoCartesianoY(afd1,afd2).delta)
#cartesiano = afd.hallarProductoCartesianoY(afd1,afd2)
##cartesionD = afd.hallarProductoCartesianoDiferencia(afd1,afd2)
#print(cartesiano.procesar_cadena_con_detalles('baababab'))
#print(cartesionO.procesar_cadena_con_detalles('aabbab'))
#print(cartesionD.procesar_cadena_con_detalles('aaabbbb'))
#cartesiano1 = afd.hallarProductoCartesiano(afd1,afd2, 'interseccion')
#print(cartesiano1.procesar_cadena_con_detalles('aabbabab'))






