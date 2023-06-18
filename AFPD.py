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
                        source, consume, destiny, pushletter= lines[i].strip().split(':')
                        popletter, destiny = destiny.split('>')
                        if source not in self.delta:
                            self.delta[source] = {}
                        if consume not in self.delta[source]:
                            self.delta[source][consume] = ""
                        self.delta[source][consume] = destiny
                        i += 1

        #print(self.delta)   
    def modificarPila(self, operacion, parametro):
        def pop(self):
            if (self.alfabetoPila[-1] != ""):
                return -1
            elif (self.alfabetoPila[-1] == parametro):
                self.alfabetoPila.pop()
            else: return -1 
                
        if operacion == 'push':
            self.alfabetoPila.append(parametro)
        elif operacion == 'pop':
            pop(self)     
        elif operacion == 'remplazamiento':
            pop(self)
            self.alfabetoPila.append(parametro)
            return 0



   