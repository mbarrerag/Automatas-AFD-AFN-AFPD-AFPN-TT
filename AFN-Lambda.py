from time import sleep
from queue import LifoQueue

class AFN_Lambda:
    def __init__(self, alfabeto=None, estados=None, estadoInicial=None, estadosAceptacion=None, delta=None,
                 nombreArchivo=None):
        if nombreArchivo:
            self.cargarDesdeArchivo(nombreArchivo)

        else:
            self.alfabeto = alfabeto
            self.estados = estados
            self.estadoInicial = estadoInicial
            self.estadosAceptacion = estadosAceptacion
            self.delta = delta
            self.estadosLimbo = []
            self.estadosInaccesibles = []


    def cargarDesdeArchivo(self, nombreArchivo):
        self.alfabeto = []
        self.estados = []
        self.estadoInicial = None
        self.estadosAceptacion = []
        # Guardaremos las transiciones desde cada estado en diccionarios,
        # donde la clave es la letra, y el valor es el destino
        self.delta: list[dict] = []
        self.estadosInaccesibles = []

        with open(nombreArchivo, 'r') as f:
            lines = f.readlines()

            for i in range(len(lines)):
                if lines[i].strip() == '#alphabet':
                    current = lines[i+1]
                    j = i+1
                    while current.strip() != "#states":
                        if current.strip().__contains__("-"):
                            start, end = current.split('-')
                            start = start.strip()
                            end = end.strip()
                            lettersRange = [chr(x) for x in range(ord(start), ord(end)+1)]
                            for letter in lettersRange:
                                self.alfabeto.append(letter)
                        else:
                            self.alfabeto.append(current.strip())
                        j += 1
                        current = lines[j].strip()

                if lines[i].strip() == '#states':
                    while lines[i + 1].strip() != '#initial':
                        self.estados.append(lines[i + 1].strip())
                        i += 1

                if lines[i].strip() == '#initial':
                    self.estadoInicial = lines[i + 1].strip()
                    i += 1

                if lines[i].strip() == '#accepting':
                    while lines[i + 1].strip() != '#transitions':
                        self.estadosAceptacion.append(lines[i + 1].strip())
                        i += 1

                if lines[i].strip() == '#transitions':
                    # Primero, llenaremos cada índice de delta con diccionarios
                    for estado in range(0, len(self.estados)):
                        self.delta.append({})

                    while i < len(lines) and lines[i + 1].strip() != '':
                        source, letter = lines[i + 1].strip().split(':')
                        letter, targets = letter.split('>')
                        state = self.estados.index(source)
                        if ';' not in targets:
                            self.delta[state][letter] = targets
                        else:
                            targets = targets.split(';')
                            self.delta[state][letter] = targets
                        i += 1

    def hallarEstadosInaccesibles(self):

        isAccesible = [False] * len(self.estados)  # Lista donde registramos cuáles estados son accesibles y cuáles no
        stack = LifoQueue()
        currentState = self.estadoInicial
        allInaccesibleFound = False

        while not allInaccesibleFound:
            currentStateIndex = self.estados.index(currentState)

            if not isAccesible[currentStateIndex]:  # Es decir, el estado no lo habíamos recorrido antes
                isAccesible[currentStateIndex] = True
                newAccesibleStates = []
                targets = list(self.delta[currentStateIndex].values())  # Hallamos los estados a los que hay transiciones desde este estado

                for target in targets:
                    if type(target) == list:  # Si se trata de una lista de estados, se deben individualizar
                        for individualState in target:
                            newAccesibleStates.append(individualState)
                    else:
                        newAccesibleStates.append(target)
                newAccesibleStates = list(dict.fromkeys(newAccesibleStates))

                if len(newAccesibleStates) >= 1:
                    for state in range(1, len(newAccesibleStates)):
                        stack.put(newAccesibleStates[state])
                    currentState = newAccesibleStates[0]
                else:
                    currentState = stack.get() if not stack.empty() else None  # Desapilamos
                    allInaccesibleFound = True if currentState is None else False  # No hay más estados por recorrer

            else:  # El estado ya había sido explorado. Desapilamos los estados buscando uno nuevo
                currentState = stack.get() if not stack.empty() else None
                allInaccesibleFound = True if currentState is None else False

        return isAccesibles


firstAFNL = AFN_Lambda(nombreArchivo="firstAFNLtest.NFE")
print(firstAFNL.alfabeto)
print(firstAFNL.estados)
print(firstAFNL.estadoInicial)
print(firstAFNL.estadosAceptacion)
print(firstAFNL.delta)


print(firstAFNL.hallarEstadosInaccesibles())



