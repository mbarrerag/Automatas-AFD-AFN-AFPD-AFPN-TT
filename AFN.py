import AFD
class AFN:
    def __init__(self, alfabeto=None, estados=None, estadoInicial=None, estadosAceptacion=None, delta=None, nombreArchivo=None):
        if nombreArchivo:
            self.cargar_desde_archivo(nombreArchivo)

        else:
            self.alfabeto = alfabeto
            self.estados = estados
            self.estadoInicial = estadoInicial
            self.estadosAceptacion = estadosAceptacion
            self.estadosInaccesibles = []
            self.delta = dict(delta)

    def cargar_desde_archivo(self, nombreArchivo):
        self.alfabeto = []
        self.estados = []
        self.estadoInicial = []
        self.estadosAceptacion = []
        self.estadosInaccesibles = []
        self.delta = {}

        with open(nombreArchivo, 'r') as f:
            lines = f.readlines()

            for i in range(len(lines)):
                if lines[i].strip() == '#alphabet':
                    letter_range = lines[i+1].strip()
                    start, end = letter_range.split('-')
                    self.alfabeto = [chr(x)
                                     for x in range(ord(start), ord(end) + 1)]
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
                    i += 1
                    while i < len(lines) and lines[i].strip() != '':
                        source, letter = lines[i].strip().split(':')
                        letter, target = letter.split('>')
                        target = target.split(';')
                        if source not in self.delta:
                            self.delta[source] = {}
                        self.delta[source][letter] = target
                        i += 1

    def hallarEstadosInaccesibles(self):

        estadosAccesibles = []
        estadosAccesibles.append(self.estadoInicial[0])
        while True:
            copiaEstadosAccesibles = estadosAccesibles.copy()
            for estado in estadosAccesibles:
                if(estado in self.delta):
                    for caracter in self.delta[estado]:
                        for estadoTransicionado in self.delta[estado][caracter]:
                            if not estadoTransicionado in estadosAccesibles:
                                estadosAccesibles.append(estadoTransicionado)
            if copiaEstadosAccesibles == estadosAccesibles:
                break
        self.estadosInaccesibles = self.estados.copy()
        for estado in estadosAccesibles:
            self.estadosInaccesibles.remove(estado)
        return self.estadosInaccesibles

    def __str__(self):
        output = "!NFA\n"
        output += "#alphabet\n"
        output += f"{min(self.alfabeto)}-{max(self.alfabeto)}\n"
        output += "#states\n"
        output += "\n".join(sorted(self.estados)) + "\n"
        output += "#initial\n"
        output += str(self.estadoInicial[0]) + "\n"
        output += "#accepting\n"
        output += "\n".join(sorted(self.estadosAceptacion)) + "\n"
        output += "#transitions\n"
        for estado in self.delta:
            for caracter in self.delta[estado]:
                output += f'{estado}:{caracter}>'
                for estadoTransicionado in self.delta[estado][caracter]:
                    output += estadoTransicionado+';'
                output = output.rstrip(';')
                output += '\n'
        output += "#inaccessible\n"
        output += "\n".join(sorted(self.estadosInaccesibles)) + "\n"
        return output

    

    def imprimirAFNSimplificado(self):
        output = "!NFA\n"
        output += "#states\n"
        estados = self.estados.copy()
        for x in self.estadosInaccesibles:
            estados.remove(x)
        output += "\n".join(sorted(estados)) + "\n"
        output += "#initial\n"
        output += str(self.estadoInicial[0]) + "\n"
        output += "#accepting\n"
        output += "\n".join(sorted(self.estadosAceptacion)) + "\n"
        output += "#transitions\n"
        for estado in self.delta:
            for caracter in self.delta[estado]:
                output += f'{estado}:{caracter}>'
                for estadoTransicionado in self.delta[estado][caracter]:
                    output += estadoTransicionado+';'
                output = output.rstrip(';')
                output += '\n'

        return output

    def exportar(self, nombreArchivo):
        quitar = ''
        for x in self.estadosInaccesibles:
            quitar += x + '\n'
        cadena = str(self).rstrip(quitar)
        with open(nombreArchivo, 'w') as f:
            f.write(cadena.rstrip("#inaccessible"))
    
    def AFNtoAFD(self, imprimirTabla = False):
        estadosAFD = []
        estadoInicialAFD = ['{'+self.estadoInicial[0]+'}']
        deltaAFD = {}
        estadosAceptacionAFD = []

        for estado in self.estados:
            estadosAFD.append(estado)
        
        while True:
            copiaEstadosAFD = estadosAFD.copy()
            for estado in estadosAFD:
                if not estado in deltaAFD:
                    deltaAFD[estado] = {}
                    for caracter in self.alfabeto:
                        transicion = []
                        for subEstado in estado.split(','):
                            if subEstado in self.delta:
                                if caracter in self.delta[subEstado]:
                                    transicion += self.delta[subEstado][caracter]
                        strTransicion = ''
                        for elemento in transicion:
                            strTransicion += elemento+','
                        strTransicion = strTransicion.rstrip(',')
                        deltaAFD[estado][caracter] = strTransicion
                        if not strTransicion in estadosAFD and strTransicion != '':
                            estadosAFD.append(strTransicion)
            if copiaEstadosAFD == estadosAFD:
                break
        
        for estadoAFD in estadosAFD:
            for estadoAceptacion in self.estadosAceptacion:
                if estadoAceptacion in estadoAFD and '{'+estadoAFD+'}' not in estadosAceptacionAFD :
                    estadosAceptacionAFD.append('{'+estadoAFD+'}')
        
        for i in range(estadosAFD.__len__()):
            estadosAFD[i] = '{'+estadosAFD[i]+'}'
        
        deltaAFDItera = {}
        for estado in deltaAFD:
            deltaAFDItera['{'+estado+'}'] = {}
            for caracter in deltaAFD[estado]:
                deltaAFDItera['{'+estado+'}'][caracter] = '{'+deltaAFD[estado][caracter]+'}'
        deltaAFD = deltaAFDItera

        afd = AFD.AFD(alfabeto=self.alfabeto, estados=estadosAFD, estadoInicial=estadoInicialAFD, estadosAceptacion=estadosAceptacionAFD, delta=deltaAFD)
        afd.hallarEstadosInaccesibles()
        afd.hallarEstadosLimbo()
        if imprimirTabla:
            nuemeroDeEspacios = 5
            for estado in afd.estados:
                if estado.__len__() > nuemeroDeEspacios:
                    nuemeroDeEspacios = estado.__len__()
            nuemeroDeEspacios += 2

            print('Estados antiguos y nuevos:')
            print('|'+'delta'.center(nuemeroDeEspacios, " ")+'|', end = '')
            for caracter in afd.alfabeto:
                print(caracter.center(nuemeroDeEspacios, " ")+'|', end = '')
            print('')
            for estado in afd.delta:
                print('|'+estado.center(nuemeroDeEspacios, " ")+'|', end = '')
                for caracter in afd.delta[estado]:
                    print(afd.delta[estado][caracter].center(nuemeroDeEspacios, " ")+'|', end='')
                print('')
        
        return afd
    
    def procesarCadena(self, cadena = ''):
        afd = self.AFNtoAFD()
        return afd.procesar_cadena(cadena = cadena)
