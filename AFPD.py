from AFD import AFD

class AFPD:
    def __init__(self, estados=None, estadoInicial=None, estadosAceptacion=None, alfabetoCinta=None, alfabetoPila = None, delta=None, nombreArchivo=None):
        if nombreArchivo:
            self.cargar_desde_archivo(nombreArchivo)
            
        else:
            self.estados = estados
            self.estadoInicial = estadoInicial
            self.estadosAceptacion = estadosAceptacion
            self.alfabetoCinta = alfabetoCinta
            self.alfabetoPila = alfabetoPila
            self.delta = delta  
        self.verificarCorregirCompletitud()

    def cargar_desde_archivo(self, nombreArchivo):
        self.estados = []
        self.estadoInicial = None
        self.estadosAceptacion = []
        self.alfabetoCinta = []
        self.alfabetoPila = []
        self.delta = {}

        with open(nombreArchivo, 'r') as f:
            lines = f.readlines()
            
            for i in range(len(lines)):
                
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

                if lines[i].strip() == '#tapeAlphabet':
                    letter_range = lines[i+1].strip()
                    start, end = letter_range.split('-')
                    self.alfabetoCinta += [chr(x) for x in range(ord(start), ord(end) + 1)]
                    i += 1

                if lines[i].strip() == '#stackAlphabet':
                    letter_range = lines[i+1].strip()
                    start, end = letter_range.split('-')
                    self.alfabetoPila += [chr(x) for x in range(ord(start), ord(end) + 1)]
                    i += 1


                if lines[i].strip() == '#transitions':
                    i += 1
                    while i < len(lines) and lines[i].strip() != '':
                        source, consume, destiny, pushletter = lines[i].strip().split(':')
                        popletter, destiny = destiny.split('>')
                        if source not in self.delta:
                            self.delta[source] = {}
                        if consume not in self.delta[source]:
                            self.delta[source][consume] = ""
                        self.delta[source][consume] = [destiny, pushletter, popletter]
                        i += 1

        #print(self.delta)   
    def __str__(self):
        output = "!DFA\n"

        output += "#tapeAlphabet\n"
        
        # Ordenar el alfabeto eliminando duplicados
        sorted_alfabeto = sorted(set(self.alfabetoCinta), key=ord)
        
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

        output += "#Stackalphabet\n"
        
        # Ordenar el alfabeto eliminando duplicados
        sorted_alfabeto = sorted(set(self.alfabetoPila), key=ord)
        
        # Crear rangos
        rangos = []
        rango_actual = [sorted_alfabeto[0]]
        print(sorted_alfabeto)
        print(self.alfabetoPila)
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
                destiny = target[0]
                pushletter = target[1]
                popletter = target[2]
                output += f"{source}:{letter}:{popletter}>{destiny}:{pushletter}\n"
        
        #output += "#inaccessible\n"
        #output += "\n".join(sorted(self.estadosInaccesibles)) + "\n"

        #output += "#limbo\n"
        #output += "\n".join(sorted(self.estadosLimbo)) + "\n"

        return output
    def verificarCorregirCompletitud(self):
        islimboAdded = False
        for estado in self.estados:
            if estado not in self.delta:
                self.delta[estado] = {}
            
            for simbolo in self.alfabetoCinta:
                if simbolo not in self.delta[estado]:
                    self.delta[estado][simbolo] = ['limbo','$','$']
                #Se añadió este if para manejo de errores de doc con transiciones incompletas para el AFPD
                    if 'limbo' not in self.delta:                   
                        self.delta['limbo'] = {}
                        for simbolo in self.alfabetoCinta:
                            self.delta['limbo'][simbolo] = ['limbo','$','$']
                        islimboAdded = True
        if islimboAdded:            
            self.estados.append('limbo')
    
    def modificarPila(self, operacion, parametro):
        def pop(self):
            if (self.alfabetoPila == []):
                return False
            else: self.alfabetoPila.pop()
               
        if operacion == 'push':
            self.alfabetoPila.append(parametro)
            return True
        elif operacion == 'pop':
            pop(self)  
            return True    
        elif operacion == 'remplazamiento':
             if (self.alfabetoPila == []):
                return False
             else: self.alfabetoPila.pop()
           
             self.alfabetoPila.append(parametro)
             return True
        
    def isPilaEmpty(self):
        if self.alfabetoPila == []:
            return True
        else:
            return False
        
    def procesarCadena (self, cadena,detalles=False):
        self.alfabetoPila=[]
        estadoActual = self.estadoInicial
        procesamiento = f"{estadoActual}"
        for simbolo in cadena: # convertir lista a tupla
         
            if estadoActual not in self.delta:
                if(detalles):
                    print(cadena,procesamiento, 'Abortado')
                return (procesamiento,False) if detalles else False
            try:
                destiny = self.delta[estadoActual][simbolo][0]
                pushletter = self.delta[estadoActual][simbolo][1]
                popletter = self.delta[estadoActual][simbolo][2]
            except:
                #raise Exception("No hay camino posible")
                if(detalles):
                    print(cadena,procesamiento, 'Abortado')
                return (procesamiento,False) if detalles else False
            def indetificacionOperacion(self):
                
                if pushletter != "$" and popletter != "$":
                    return "remplazamiento"
                elif pushletter != "$":
                    return "push"
                elif popletter != "$":
                    return "pop"
                else: return -1

            operacionIdentificada = indetificacionOperacion(self)
            if(operacionIdentificada == "remplazamiento" or operacionIdentificada == "pop"):
               if(self.alfabetoPila == [] or self.alfabetoPila[-1] != popletter):
                   if(detalles):
                       print(cadena,procesamiento, 'Abortado')
                   return (procesamiento,False) if detalles else False
            procesamiento += f",{simbolo},{self.alfabetoPila} --> {destiny}"   
            if self.modificarPila(operacionIdentificada, pushletter):
              estadoActual = destiny # convertir tupla de vuelta a lista
        resultado = ((estadoActual in self.estadosAceptacion) and (self.isPilaEmpty()))
        if(detalles):
            print(cadena,procesamiento, 'Aceptacion' if resultado else 'Rechazado')
        
        return (procesamiento,resultado) if detalles else resultado  # convertir a tupla antes de chequear
    

    
    def procesarCadenaConDetalles(self, cadena):
          return self.procesarCadena(cadena,True)
      
    def procesarListaCadenas(self,listaCadenas,nombreArchivo,imprimirPantalla):
        if not nombreArchivo or not nombreArchivo.strip():
            nombreArchivo = "resultados.txt"
        with open(nombreArchivo, 'w') as archivo:
             for cadena in listaCadenas:
                 detalles = self.procesarCadenaConDetalles(cadena)  
                 resultado = "si" if self.procesarCadena(cadena=cadena) else "no"
                 linea = f"{cadena}\t{detalles[0]}\t{resultado}"
                 archivo.write(linea + '\n')
             

    def operacion(self,AFD,state1, state2, operador):
        if operador == "Y":
            if(state1 in AFD.estadosAceptacion and state2 in self.estadosAceptacion):
                return True
            else:
                return False
        elif operador == "O":
            if(state1 in AFD.estadosAceptacion or state2 in self.estadosAceptacion):
                return True
            else:
                return False
        elif operador == "diferencia":
            if(state1 in AFD.estadosAceptacion and not state2 in self.estadosAceptacion):
                return True
            else:
                return False
        elif operador == "difSimetrica":
            if(not state1 in AFD.estadosAceptacion and not state2 in self.estadosAceptacion):
                return True
            else:
                return False

    def hallarProductoCartesiano(self,afd1, afpd2, operacion):
        estados_Final = []
        delta_Final = {}
        aceptados = []
        #afd1 son el conjunto de estados del AFD
        #afpd2 son el conjunto de estados del AFPD
        for estado1 in afd1.estados:
            for estado2 in afpd2.estados:
                nombramiento = f"{ '{}' , '{}' }".format(estado1, estado2)
                estados_Final.append(nombramiento)
                #estado1 corresponde al estado del afd y estado2 al del afpd (self)
                if self.operacion(afd1,estado1, estado2, operacion):
                    aceptados.append(nombramiento)
                if afd1.alfabeto == afpd2.alfabetoCinta:
                    for letter in afd1.alfabeto:
                        trans1 = afd1.delta[estado1][letter]
                        #el delta AFPD retorna una lista de 3 direcciones [destiny,pushletter,popletter]
                        trans2 = afpd2.delta[estado2][letter]
                        delta_Final[nombramiento] = {}
                        delta_Final[nombramiento][letter] = [f"{ '{}' , '{}' }".format(trans1, trans2[0]),trans2[1],trans2[2]]
                else:
                    raise Exception(
                        "Los automatas tienen distintos lenguajes en la operacion hallarProductoCartesiano")
        inicial = f"{ '{}' , '{}' }".format(afd1.estadoInicial, afpd2.estadoInicial)
        return AFPD(estados=estados_Final,estadoInicial=inicial,  estadosAceptacion=aceptados,alfabetoCinta=afpd2.alfabetoCinta,alfabetoPila=afpd2.alfabetoPila,delta=delta_Final)