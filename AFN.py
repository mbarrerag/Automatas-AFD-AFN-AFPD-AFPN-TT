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
        self.estadoInicial = None
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

    def hallarEstadosInaccesibles(self):

        estadosAccesibles = []
        estadosAccesibles.append(self.estadoInicial)
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
        output += str(self.estadoInicial) + "\n"
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
        output += str(self.estadoInicial) + "\n"
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

    def AFNtoAFD(self, imprimirTabla=True):
        estadosAFD = []
        estadoInicialAFD = '{'+self.estadoInicial+'}'
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
                                    for estadoPasado in self.delta[subEstado][caracter]:
                                        if estadoPasado not in transicion:
                                            transicion.append(estadoPasado)
                        transicion.sort()            
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
                if estadoAceptacion in estadoAFD and '{'+estadoAFD+'}' not in estadosAceptacionAFD:
                    estadosAceptacionAFD.append('{'+estadoAFD+'}')

        for i in range(estadosAFD.__len__()):
            estadosAFD[i] = '{'+estadosAFD[i]+'}'

        deltaAFDItera = {}
        for estado in deltaAFD:
            deltaAFDItera['{'+estado+'}'] = {}
            for caracter in deltaAFD[estado]:
                deltaAFDItera['{'+estado+'}'][caracter] = '{' + \
                    deltaAFD[estado][caracter]+'}'
        deltaAFD = deltaAFDItera

        afd = AFD.AFD(alfabeto=self.alfabeto, estados=estadosAFD, estadoInicial=estadoInicialAFD,
                      estadosAceptacion=estadosAceptacionAFD, delta=deltaAFD)
        
        if imprimirTabla:
            nuemeroDeEspacios = 5
            for estado in afd.estados:
                if estado.__len__() > nuemeroDeEspacios:
                    nuemeroDeEspacios = estado.__len__()
            nuemeroDeEspacios += 2

            print('Estados antiguos y nuevos:')
            print('|'+'delta'.center(nuemeroDeEspacios, " ")+'|', end='')
            for caracter in afd.alfabeto:
                print(caracter.center(nuemeroDeEspacios, " ")+'|', end='')
            print('')
            for estado in afd.delta:
                print('|'+estado.center(nuemeroDeEspacios, " ")+'|', end='')
                for caracter in afd.delta[estado]:
                    print(afd.delta[estado][caracter].center(
                        nuemeroDeEspacios, " ")+'|', end='')
                print('')
        afd.eliminar_estados_inaccesibles()
        return afd

    def procesarCadena(self, cadena=''):
        estadosActuales = [self.estadoInicial]
        for caracter in cadena:
            siguientesEstados = []
            for estadoActual in estadosActuales:
                if estadoActual in self.delta:
                    if caracter in self.delta[estadoActual]:
                        siguientesEstados += self.delta[estadoActual][caracter]
            if siguientesEstados == []:
                return False
            estadosActuales = siguientesEstados
        aceptacion = False
        for estado in estadosActuales:
            if estado in self.estadosAceptacion:
                aceptacion = True
        return aceptacion

    def procesar_cadena_con_detalles(self, cadena=''):
        inicio = self.nodo(
            estado=self.estadoInicial, cadena=cadena, camino=self.estadoInicial)
        self.generarCaminos(nodoActual=inicio)

        caminos = self.obtenerCaminos(nodoActual=inicio)
        aceptacion = False
        for camino in caminos:
            if camino[0] == 'ac':
                aceptacion = True
                print(camino[1])
                break
        if aceptacion == False:
            caminoAImprimir = caminos[0][1]
            for camino in caminos:
                if camino[1].__len__() < caminoAImprimir.__len__():
                    caminoAImprimir = camino[1]
            print(caminoAImprimir)
        return aceptacion

    def computarTodosLosProcesamientos(self, cadena='', nombreArchivo=''):
        inicio = self.nodo(
            estado=self.estadoInicial, cadena=cadena, camino=self.estadoInicial)
        self.generarCaminos(nodoActual=inicio)

        caminos = self.obtenerCaminos(nodoActual=inicio, imprimir=True)
        archivoAceptadas = open(f'{nombreArchivo}Aceptadas.txt', 'w')
        archivoRechazadas = open(f'{nombreArchivo}Rechazadas.txt', 'w')
        archivoAbortadas = open(f'{nombreArchivo}Abortadas.txt', 'w')
        for camino in caminos:
            if camino[0] == 'ac':
                archivoAceptadas.write(f"{camino[1]} \n")
            elif camino[0] == 're':
                archivoRechazadas.write(f"{camino[1]} \n")
            elif camino[0] == 'ab':
                archivoAbortadas.write(f"{camino[1]} \n")
        archivoAceptadas.close()
        archivoRechazadas.close()
        archivoAbortadas.close()
        return caminos.__len__()

    def generarCaminos(self, nodoActual=None):
        if nodoActual.cadena != '':
            if nodoActual.estado in self.delta:
                if nodoActual.cadena[0] in self.delta[nodoActual.estado]:
                    for estadoTransicionado in self.delta[nodoActual.estado][nodoActual.cadena[0]]:
                        nodoActual.next.append(self.nodo(
                            estado=estadoTransicionado, cadena=nodoActual.cadena[1:], camino=nodoActual.camino+f'--{nodoActual.cadena[0]}-->{estadoTransicionado}'))
                    for nodoSiguiente in nodoActual.next:
                        self.generarCaminos(nodoSiguiente)
                else:
                    nodoActual.camino += f'--{nodoActual.cadena[0]}-->//'
            else:
                nodoActual.camino += f'--{nodoActual.cadena[0]}-->//'

    def obtenerCaminos(self, nodoActual=None, imprimir=False):
        if nodoActual.next == []:
            if '//' in nodoActual.camino:
                if imprimir:
                    print(f'{nodoActual.camino} : abortado')
                return [['ab', nodoActual.camino]]
            else:
                if nodoActual.estado in self.estadosAceptacion:
                    if imprimir:
                        print(f'{nodoActual.camino} : aceptacion')
                    return [['ac', nodoActual.camino]]
                else:
                    if imprimir:
                        print(f'{nodoActual.camino} : rechazo')
                    return [['re', nodoActual.camino]]
        else:
            caminos = []
            for siguienteNodo in nodoActual.next:
                caminos += self.obtenerCaminos(
                    nodoActual=siguienteNodo, imprimir=imprimir)
            return caminos

    def procesarListaCadenas(self, listaCadenas=[], nombreArchivo='', imprimirPantalla=False):
        archivo = open(f'{nombreArchivo}.txt', 'w')
        contador_si = 0  # Contador para los "si"
        contador_no = 0
        for cadena in listaCadenas:
            textoDeCadena = ''
            textoDeCadena += f'{cadena}\n'

            inicio = self.nodo(
                estado=self.estadoInicial, cadena=cadena, camino=self.estadoInicial)
            self.generarCaminos(nodoActual=inicio)
            caminos = self.obtenerCaminos(nodoActual=inicio)
            numeroDeProcesamientosDeAceptacion = 0
            numeroDeProcesamientosDeRechazo = 0
            numeroDeProcesamientosDeAbortado = 0
            for camino in caminos:
                if camino[0] == 'ac':
                    numeroDeProcesamientosDeAceptacion += 1
                elif camino[0] == 're':
                    numeroDeProcesamientosDeRechazo += 1
                elif camino[0] == 'ab':
                    numeroDeProcesamientosDeAbortado += 1

            if numeroDeProcesamientosDeAceptacion == 0:
                caminoAImprimir = caminos[0][1]
                for camino in caminos:
                    if camino[1].__len__() < caminoAImprimir.__len__():
                        caminoAImprimir = camino[1]
                textoDeCadena += f'{caminoAImprimir}\n'
            else:
                for camino in caminos:
                    if camino[0] == 'ac':
                        textoDeCadena += f'{camino[1]}\n'
                        break

            textoDeCadena += f'{caminos.__len__()}\n'

            textoDeCadena += f'{numeroDeProcesamientosDeAceptacion}\n'
            textoDeCadena += f'{numeroDeProcesamientosDeRechazo}\n'
            textoDeCadena += f'{numeroDeProcesamientosDeAbortado}\n'

            if numeroDeProcesamientosDeAceptacion == 0:
                textoDeCadena += 'no\n'
                contador_no += 1
            else:
                textoDeCadena += 'si\n'
                contador_si += 1
            archivo.write(textoDeCadena)
            if imprimirPantalla:
                print(textoDeCadena)
                print('------------------------')
        archivo.close()
        return contador_si, contador_no

    def procesarCadenaConversion(self, cadena=''):
        afd = self.AFNtoAFD()
        return afd.procesar_cadena(cadena=cadena)

    def procesarCadenaConDetallesConversion(self, cadena=''):
        afd = self.AFNtoAFD()
        return afd.procesar_cadena_con_detalles(cadena=cadena)

    def procesarListaCadenasConversion(self, listaCadenas=[], nombreArchivo='', imprimirPantalla=False):
        afd = self.AFNtoAFD()
        afd.procesarListaCadenas(
            listaCadenas=listaCadenas, nombreArchivo=nombreArchivo, imprimirPantalla=imprimirPantalla)

    class nodo:
        def __init__(selfnodo, estado=None, cadena='', camino=''):
            selfnodo.estado = estado
            selfnodo.cadena = cadena
            selfnodo.next = []
            selfnodo.camino = camino
