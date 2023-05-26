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
                        self.estadoInicial = lines[i+1].strip()
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
        estadoActual = self.estadoInicial
        for simbolo in cadena:
            if estadoActual not in self.delta:
                return False
            estadoActual = self.delta[estadoActual][simbolo]
        return estadoActual in self.estadosAceptacion
    
    def procesar_cadena_con_detalles(self, cadena):
        estadoActual = self.estadoInicial

        for simbolo in cadena:
            print(f"{estadoActual},{simbolo} --> {self.delta[estadoActual][simbolo]}")
            estadoActual = self.delta[estadoActual][simbolo]

        return estadoActual in self.estadosAceptacion
    
    def procesar_cadena_con_detalles_print(self, cadena):
        estadoActual = self.estadoInicial
        procesamiento = f"{estadoActual}"
        for simbolo in cadena:
            procesamiento += f",{simbolo} --> {self.delta[estadoActual][simbolo]}"
            estadoActual = self.delta[estadoActual][simbolo]
        return procesamiento 
    


    def procesarListaCadenas(self, listaCadenas, nombreArchivo, imprimirPantalla):

        if not nombreArchivo or not nombreArchivo.strip():
            nombreArchivo = "resultados.txt"

        with open(nombreArchivo, 'w') as archivo:
            for cadena in listaCadenas:
                detalles = self.procesar_cadena_con_detalles_print(cadena)  
                resultado = "si" if detalles else "no"  
                linea = f"{cadena}\t{detalles}\t{resultado}"

                archivo.write(linea + '\n')

                if imprimirPantalla:
                    print(linea)

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
    
    def merge_states(self, states):
        return ','.join(sorted(states))

    def simplificarAFD(self):
        self.eliminar_estados_inaccesibles()

        # Initialize triangular table with all pairs of states
        tabla = {frozenset({p, q}): False for p in self.estados for q in self.estados if p != q}

        # Mark with 'X' if one state is an accepting state and the other is not
        for pair in tabla:
            p, q = list(pair)
            tabla[pair] = (p in self.estadosAceptacion and q not in self.estadosAceptacion) or \
                        (q in self.estadosAceptacion and p not in self.estadosAceptacion)

        while True:
            new_table = tabla.copy()
            for pair in tabla:
                if not tabla[pair]:
                    p, q = list(pair)
                    for a in self.alfabeto:
                        if self.delta[p][a] != self.delta[q][a] and \
                        tabla[frozenset({self.delta[p][a], self.delta[q][a]})]:
                            new_table[pair] = True
                            break

            if new_table == tabla:
                break
            else:
                tabla = new_table

        # Merge equivalent states
        clusters = []
        for pair in tabla:
            if not tabla[pair]:
                found = False
                for cluster in clusters:
                    if pair.issubset(cluster):
                        found = True
                        break
                    if pair.intersection(cluster):
                        cluster.update(pair)
                        found = True
                        break
                if not found:
                    clusters.append(set(pair))

        # Add states that didn't appear in any pair to the clusters
        all_states_in_pairs = set().union(*clusters)
        for state in self.estados:
            if state not in all_states_in_pairs:
                clusters.append({state})

        # Create new DFA with merged states
        nuevo_delta = {}
        for cluster in clusters:
            merged_state = self.merge_states(cluster)
            merged_transitions = {}
            for a in self.alfabeto:
                next_state = self.delta[next(iter(cluster))][a]
                for next_cluster in clusters:
                    if next_state in next_cluster:
                        merged_transitions[a] = self.merge_states(next_cluster)
                        break
            nuevo_delta[merged_state] = merged_transitions

        self.estados = [self.merge_states(cluster) for cluster in clusters]
        self.delta = nuevo_delta

        # Update the initial and accepting states with their new names
        for cluster in clusters:
            if self.estadoInicial in cluster:
                self.estadoInicial = self.merge_states(cluster)
            if any(state in self.estadosAceptacion for state in cluster):
                self.estadosAceptacion = [self.merge_states(cluster) for cluster in clusters if any(state in self.estadosAceptacion for state in cluster)]



       
afd = AFD(nombreArchivo='testAFD.DFA')
afd1 = AFD(nombreArchivo='evenA.DFA')
afd2 = AFD(nombreArchivo='evenB.DFA')
#afd.verificarCorregirCompletitud()
# afd.hallarEstadosInaccesibles()
# afd.hallarEstadosLimbo()
# print(afd)
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
afdmin = AFD(nombreArchivo='minTest.DFA')
afdmin.simplificarAFD()
print(afdmin)
afdmin.draw().view()







