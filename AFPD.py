from AFD import AFD

class AFD:
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


    def cargar_desde_archivo(self, nombreArchivo):
        self.estados = []
        self.estadoInicial = []
        self.estadosAceptacion = None
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
                    self.alfabeto = [chr(x) for x in range(ord(start), ord(end) + 1)]
                    i += 1

                if lines[i].strip() == '#Stackalphabet':
                    letter_range = lines[i+1].strip()
                    start, end = letter_range.split('-')
                    self.alfabeto = [chr(x) for x in range(ord(start), ord(end) + 1)]
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
        

    def procesarCadena (self, cadena):
        estadoActual = self.estadoInicial
        for simbolo in cadena: # convertir lista a tupla
         
            if estadoActual not in self.delta:

                return False
            destiny = estadoActual[0]
            pushletter = estadoActual[1]
            popletter = estadoActual[2]
            def indetificacionOperacion(self):
                
                if pushletter != "$" and popletter != "$":
                    return "remplazamiento"
                elif pushletter != "$":
                    return "push"
                elif popletter != "$":
                    return "pop"
                else: return -1

            operacionIdentificada = indetificacionOperacion()
            if(operacionIdentificada == "remplzamiento" or operacionIdentificada == "pop"):
               if(self.alfabetoPila[-1] != popletter):
                   return False
            if self.modificarPila(indetificacionOperacion(), pushletter):
              estadoActual = self.delta[estadoActual][simbolo] # convertir tupla de vuelta a lista
        return estadoActual in self.estadosAceptacion  # convertir a tupla antes de chequear



