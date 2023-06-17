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
                    i += 1
                    while i < len(lines) and lines[i].strip() != '':
                        source, letter = lines[i].strip().split(':')
                        letter, target = letter.split('>')
                        target = target.split(';')
                        if source not in self.delta:
                            self.delta[source] = {}
                        if letter not in self.delta[source]:
                            self.delta[source][letter] = []
                        self.delta[source][letter] += target
                        i += 1
        #print(self.delta)     

   