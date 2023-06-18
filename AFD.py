from graphviz import Digraph

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

        #self.verificarCorregirCompletitud()
        #self.hallarEstadosInaccesibles()
            

    def __str__(self):
        output = "!DFA\n"

        output += "#alphabet\n"
        
        # Ordenar el alfabeto eliminando duplicados
        sorted_alfabeto = sorted(set(self.alfabeto), key=ord)
        
        # Crear rangos
        rangos = []
        rango_actual = [sorted_alfabeto[0]]
        
        for i in range(1, len(sorted_alfabeto)):
            if ord(sorted_alfabeto[i]) - ord(rango_actual[-1]) == 1:
                rango_actual.append(sorted_alfabeto[i])
            else:
                rangos.append(rango_actual)
                rango_actual = [sorted_alfabeto[i]]
        rangos.append(rango_actual)

        # Imprimir rangos
        for rango in rangos:
            if len(rango) > 1:
                output += f"{rango[0]}-{rango[-1]}\n"
            else:
                output += f"{rango[0]}\n"


        output += "#states\n"
        estados_str = [str(estado) for estado in self.estados]
        output += "\n".join(estados_str) + "\n"
        

        output += "#initial\n"
        output += str(self.estadoInicial) + "\n"


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
        
        estados_no_limbo = [estado for estado in self.estados if estado not in self.estadosLimbo]
        output += "\n".join(sorted(estados_no_limbo)) + "\n" 

        output += "#initial\n"
        output += str(self.estadoInicial) + "\n"

        output += "#accepting\n"
        estados_aceptacion_no_limbo = [estado for estado in self.estadosAceptacion if estado not in self.estadosLimbo]
        output += "\n".join(sorted(estados_aceptacion_no_limbo)) + "\n"

        output += "#transitions\n"
        for source, transitions in self.delta.items():
            if source not in self.estadosLimbo:
                for letter, target in transitions.items():
                    if target != 'limbo':
                        output += f"{source}:{letter}>{target}\n"
        
        return output


        
    def verificarCorregirCompletitud(self):
        estadosLimbo = []  # Lista para mantener los estados que tienen transiciones al limbo

        for estado in self.estados:
            if estado not in self.delta:
                self.delta[estado] = {}

            for simbolo in self.alfabeto:
                if simbolo not in self.delta[estado]:  # Aquí verificamos si no hay transición definida para el símbolo
                    self.delta[estado][simbolo] = 'limbo'  # Agregamos una transición al limbo para el símbolo
                    if estado not in estadosLimbo:
                        estadosLimbo.append(estado)  # Añadimos el estado a la lista de estados que tienen transiciones al limbo

        self.estadosLimbo = estadosLimbo  # Actualizamos self.estadosLimbo con los estados que tienen transiciones al limbo

        return self.estadosLimbo



    def hallarEstadosLimbo(self):
        for estado in self.estados:
            if estado not in self.delta:
                self.estadosLimbo.append(estado)
        return self.estadosLimbo
    
    
    def hallarEstadosInaccesibles(self):
        self.estadosInaccesibles = self.estados.copy()
        if self.estadoInicial in self.estadosInaccesibles:
            self.estadosInaccesibles.remove(self.estadoInicial)
        for estado in self.estados:
            if estado in self.delta:
                for transicion in self.delta[estado]:
                    if self.delta[estado][transicion] in self.estadosInaccesibles:
                        self.estadosInaccesibles.remove(self.delta[estado][transicion])
        return self.estadosInaccesibles
    
    def eliminar_estados_inaccesibles(self):
        inaccesibles = self.hallarEstadosInaccesibles()
        self.estados = [state for state in self.estados if state not in inaccesibles]
        self.estadosAceptacion = [state for state in self.estadosAceptacion if state not in inaccesibles]
        self.delta = {state: transitions for state, transitions in self.delta.items() if state not in inaccesibles}


    def cargar_desde_archivo(self, nombreArchivo):
        self.alfabeto = []
        self.estados = []
        self.estadoInicial = None
        self.estadosAceptacion = []
        self.delta = {}
        self.estadosLimbo = []
        self.estadosInaccesibles = []

        secciones = {"#alphabet": [], "#states": [], "#initial": [], "#accepting": [], "#transitions": []}
        seccion_actual = None

        with open(nombreArchivo, 'r') as f:
            lines = f.readlines()
            
            # Identificar las secciones
            for line in lines:
                line = line.strip()
                if line in secciones:
                    seccion_actual = line
                elif seccion_actual and line:  # Aquí verificamos que la línea no esté vacía
                    secciones[seccion_actual].append(line)

            # Procesar cada sección
            for line in secciones['#alphabet']:
                # Validar si es un rango o un caracter individual
                if '-' in line and len(line.split('-')) == 2:  # Asegurarse de que la línea solo contenga dos partes
                    start, end = line.split('-')
                    self.alfabeto += [chr(x) for x in range(ord(start), ord(end) + 1) if chr(x) != '$']
                else:
                    if line != '$':
                        self.alfabeto.append(line)

            # Convertir el alfabeto a un conjunto para eliminar duplicados, y luego volver a una lista
            self.alfabeto = list(set(self.alfabeto))

            for line in secciones['#states']:
                self.estados.append(line)

            for line in secciones['#initial']:
                self.estadoInicial = line

            for line in secciones['#accepting']:
                self.estadosAceptacion.append(line)

            for line in secciones['#transitions']:
                if line:  # Aquí también verificamos que la línea no esté vacía antes de dividirla
                    source, letter = line.split(':')
                    letter, target = letter.split('>')
                    if source not in self.delta:
                        self.delta[source] = {}
                    self.delta[source][letter] = target


    def exportar(self, nombreArchivo):
        with open(nombreArchivo, 'w') as f:
            f.write(str(self))

    def procesar_cadena(self, cadena):
        estadoActual = self.estadoInicial
        for simbolo in cadena: # convertir lista a tupla
            if estadoActual not in self.delta:
                return False
            estadoActual = self.delta[estadoActual][simbolo] # convertir tupla de vuelta a lista
        return estadoActual in self.estadosAceptacion  # convertir a tupla antes de chequear

    
    def procesar_cadena_con_detalles(self, cadena):
        estadoActual = self.estadoInicial
        for simbolo in cadena: # convertir lista a tupla
            if estadoActual not in self.delta:
                return False
            print(f"{estadoActual},{simbolo} --> {self.delta[estadoActual][simbolo]}")
            estadoActual = self.delta[estadoActual][simbolo] # convertir tupla de vuelta a lista
        return estadoActual in self.estadosAceptacion  # convertir a tupla antes de chequear
    
    def procesar_cadena_con_detalles_print(self, cadena):
        estadoActual = self.estadoInicial
        procesamiento = f"{estadoActual}"
        for simbolo in cadena:
            if estadoActual not in self.delta:
                return False
            procesamiento += f",{simbolo} --> {self.delta[estadoActual][simbolo]}"
            estadoActual = self.delta[estadoActual][simbolo]
        return procesamiento 
    
    def procesarListaCadenas(self, listaCadenas, nombreArchivo, imprimirPantalla):
        if not nombreArchivo or not nombreArchivo.strip():
            nombreArchivo = "resultados.txt"

        contador_si = 0  # Contador para los "si"
        contador_no = 0  # Contador para los "no"

        with open(nombreArchivo, 'w') as archivo:
            for cadena in listaCadenas:
                detalles = self.procesar_cadena_con_detalles_print(cadena)  
                resultado = "si" if self.procesar_cadena(cadena=cadena) else "no"

                if resultado == "si":
                    contador_si += 1
                else:
                    contador_no += 1

                linea = f"{cadena}\t{detalles}\t{resultado}"
                archivo.write(linea + '\n')

                if imprimirPantalla:
                    print(linea)
            return contador_si, contador_no 
  

    def hallarComplemento(self):
        complemento = AFD()  
        complemento.alfabeto = self.alfabeto.copy() 

        complemento.estados = self.estados.copy()

        complemento.estadoInicial = self.estadoInicial

        complemento.estadosAceptacion = set(self.estados.copy()) - set(self.estadosAceptacion.copy()) 

        complemento.delta = self.delta.copy()

        return complemento
    
    def hallarProductoCartesianoY(self, afd1, afd2):
        producto_cartesiano = AFD()  

        producto_cartesiano.alfabeto = afd1.alfabeto

        producto_cartesiano.estados = {(estado1, estado2) for estado1 in afd1.estados for estado2 in afd2.estados}

        producto_cartesiano.estadoInicial = (afd1.estadoInicial, afd2.estadoInicial)

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


        producto_cartesiano.estadoInicial = (afd1.estadoInicial, afd2.estadoInicial)


        producto_cartesiano.estadosAceptacion = {(estado1, estado2) for estado1 in afd1.estados for estado2 in afd2.estados if estado1 in afd1.estadosAceptacion or estado2 in afd2.estadosAceptacion}

        producto_cartesiano.delta = {}
        for estado1 in afd1.estados:
            for estado2 in afd2.estados:
                producto_cartesiano.delta[(estado1, estado2)] = {}
                for simbolo in producto_cartesiano.alfabeto:
                    producto_cartesiano.delta[(estado1, estado2)][simbolo] = (afd1.delta[estado1][simbolo], afd2.delta[estado2][simbolo])

        return producto_cartesiano
    
    def hallarProductoCartesianoDiferenciaSimetrica(self, afd1, afd2):
        producto_cartesiano = AFD()  

        producto_cartesiano.alfabeto = afd1.alfabeto


        producto_cartesiano.estados = {(estado1, estado2) for estado1 in afd1.estados for estado2 in afd2.estados}


        producto_cartesiano.estadoInicial = (afd1.estadoInicial, afd2.estadoInicial)


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
            return self.hallarProductoCartesianoDiferenciaSimetrica(afd1,afd2)
        else:
            print("Operacion no valida")


    def draw(self):
        dfa = Digraph()

        for estado in self.estados:
            if estado in self.estadosAceptacion:
                dfa.attr('node', shape='doublecircle')
            else:
                dfa.attr('node', shape='circle')
            dfa.node(str(estado))

        dfa.attr('node', shape='ellipse')

        for source, transicion in self.delta.items():
            for symbol, target in transicion.items():
                if target not in self.estadosLimbo:
                    dfa.edge(str(source), str(target), label=str(symbol))

        dfa.attr('node', style='invis', width='0')
        dfa.node('start')
        dfa.edge('start', str(self.estadoInicial), style='bold')

        return dfa
    
    def combinar_estados(self, states):
        return ','.join(sorted(states))

    def simplificarAFD(self):
        self.eliminar_estados_inaccesibles()

        # Inicializar tabla triangular con todos los pares de estados
        tabla = {frozenset({p, q}): False for p in self.estados for q in self.estados if p != q}

        # Marcar con 'X' si un estado es un estado de aceptación y el otro no lo es
        for par in tabla:
            p, q = list(par)
            tabla[par] = (p in self.estadosAceptacion and q not in self.estadosAceptacion) or \
                        (q in self.estadosAceptacion and p not in self.estadosAceptacion)

        while True:
            nueva_tabla = tabla.copy()
            for par in tabla:
                if not tabla[par]:
                    p, q = list(par)
                    for a in self.alfabeto:
                        if self.delta[p][a] != self.delta[q][a] and \
                        tabla[frozenset({self.delta[p][a], self.delta[q][a]})]:
                            nueva_tabla[par] = True
                            break

            if nueva_tabla == tabla:
                break
            else:
                tabla = nueva_tabla

        # Combinar estados equivalentes
        clusters = []
        for par in tabla:
            if not tabla[par]:
                encontrado = False
                for cluster in clusters:
                    if par.issubset(cluster):
                        encontrado = True
                        break
                    if par.intersection(cluster):
                        cluster.update(par)
                        encontrado = True
                        break
                if not encontrado:
                    clusters.append(set(par))

        # Agregar estados que no aparecieron en ningún par a los clusters
        todos_los_estados_en_pares = set().union(*clusters)
        for estado in self.estados:
            if estado not in todos_los_estados_en_pares:
                clusters.append({estado})

        # Crear nuevo AFD con estados combinados
        nuevo_delta = {}
        for cluster in clusters:
            estado_combinado = self.combinar_estados(cluster)
            transiciones_combinadas = {}
            for a in self.alfabeto:
                proximo_estado = self.delta[next(iter(cluster))][a]
                for proximo_cluster in clusters:
                    if proximo_estado in proximo_cluster:
                        transiciones_combinadas[a] = self.combinar_estados(proximo_cluster)
                        break
            nuevo_delta[estado_combinado] = transiciones_combinadas

        self.estados = [self.combinar_estados(cluster) for cluster in clusters]
        self.delta = nuevo_delta

        # Actualizar los estados inicial y de aceptación con sus nuevos nombres
        for cluster in clusters:
            if self.estadoInicial in cluster:
                self.estadoInicial = self.combinar_estados(cluster)
            if any(estado in self.estadosAceptacion for estado in cluster):
                self.estadosAceptacion = [self.combinar_estados(cluster) for cluster in clusters if any(estado in self.estadosAceptacion for estado in cluster)]




       
#afd = AFD(nombreArchivo='testAFD.DFA')
#afd1 = AFD(nombreArchivo='evenA.DFA')
#afd2 = AFD(nombreArchivo='evenB.DFA')

# afd.hallarEstadosInaccesibles()
# afd.hallarEstadosLimbo()
#print(afd)
#print(afd.alfabeto)
#afd.verificarCorregirCompletitud()
#print(afd)
# afd.eliminar_estados_inaccesibles()

# print(afd.imprimirAFDSimplificado())
# afd.exportar('testAFD3.DFA')
#graph = afd2.draw()
#graph.view()
#print(afd1.procesar_cadena('abaa'))
#print(afd1.procesar_cadena_con_detalles('abbaaa'))
# print(afd2.procesar_cadena_con_detalles('abbabaabbbbb'))
# print(afd.procesar_cadena_con_detalles('aba'))

# afd.procesarListaCadenas(['aba','abbaa'], 'resultados.txt', True)
# print(afd.hallarComplemento())
# print(afd.hallarProductoCartesianoY(afd1,afd2))
# print(afd.hallarProductoCartesianoY(afd1,afd2).delta)
# cartesianoY = afd.hallarProductoCartesianoY(afd1,afd2)

#cartesianoO = afd.hallarProductoCartesianoDiferencia(afd1,afd2)
# cartesionD = afd.hallarProductoCartesianoDiferenciaSimetrica(afd1,afd2)
# print(cartesianoY.procesar_cadena_con_detalles('baababab'))
# print(cartesianoO.procesar_cadena_con_detalles('aabbab'))
# print(cartesionD.procesar_cadena_con_detalles('aaabbbb'))
# cartesiano1 = afd.hallarProductoCartesiano(afd1,afd2, 'interseccion')
# print(cartesiano1.procesar_cadena_con_detalles('aabbabab'))
#afdmin = AFD(nombreArchivo='minTest.DFA')
#afdmin.simplificarAFD()
#print(afdmin)
#afdmin.draw().view()







