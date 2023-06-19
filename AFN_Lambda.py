from queue import LifoQueue
from AFN import AFN
from Alfabeto import Alfabeto

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

        self.estadosInaccesibles = self.hallarEstadosInaccesibles()
        for estado in self.delta:
            if len(self.delta.get(estado)) == 0:
                self.estadosLimbo.append(estado)

        print("¡Autómata creado!")

    def cargarDesdeArchivo(self, nombreArchivo) -> None:
        self.alfabeto = []
        self.estados = []
        self.estadoInicial = None
        self.estadosAceptacion = []
        self.delta = {}
        self.estadosInaccesibles = []
        self.estadosLimbo = []

        with open(nombreArchivo, 'r') as f:
            lines = f.readlines()

            for i in range(len(lines)):
                if lines[i].strip() == '#alphabet':
                    current = lines[i + 1]
                    j = i + 1
                    while current.strip() != "#states":
                        if current.strip().__contains__("-"):
                            start, end = current.split('-')
                            start = start.strip()
                            end = end.strip()
                            lettersRange = [chr(x) for x in range(ord(start), ord(end) + 1)]
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
                    for estado in self.estados:
                        self.delta.update({estado: {}})

                    while i < len(lines) and lines[i + 1].strip() != '':
                        source, letter = lines[i + 1].strip().split(':')
                        letter, targets = letter.split('>')

                        targets: list[str] = targets.split(';')
                        if letter == '$' and source in targets:
                            targets.remove(source)
                            print("Transición lambda del estado " + source + " a sí mismo. ¡Ignorada!")

                        if len(targets) != 0:
                            self.delta[source][letter] = targets

                        i += 1


    def _simplePrintIteration(self, listToPrint: list[str],
                              title: str) -> str:  # Para ahorrarnos unas líneas de código en los métodos de imprimir el autómata
        output = title + '\n'
        for obj in listToPrint:
            output += obj + '\n'
        return output

    def __str__(self):
        output = self.imprimirAFNLSimplificado()

        output += self._simplePrintIteration(self.estadosInaccesibles, '#inaccesible')
        output += self._simplePrintIteration(self.estadosLimbo, '#limbo')

        return output

    def imprimirAFNLSimplificado(self):
        output = '#!nfe\n'

        output += self._simplePrintIteration(self.alfabeto, '#alphabet')
        output += self._simplePrintIteration(self.estados, '#states')
        output += '#initial \n' + self.estadoInicial + '\n'
        output += self._simplePrintIteration(self.estadosAceptacion, '#accepting')

        output += '#transitions \n'
        for estado in self.delta:
            transitions = self.delta.get(estado)
            listOfTransitions = list(transitions.items())

            for transition in listOfTransitions:
                target = transition[1]
                auxTarget = target.copy()
                target = ""
                for i in range(0, len(auxTarget)):
                    target += auxTarget[i] + ";"
                target = target.removesuffix(';')

                output += estado + ":" + transition[0] + ">" + target + "\n"

        return output

    def exportar(self, nombreArchivo):
        with open(nombreArchivo, 'w') as f:
            f.write(str(self))

    def hallarEstadosInaccesibles(self) -> list[str]:
        isAccesible = {}
        for estado in self.estados:
            isAccesible.update({estado: False})
        stack = LifoQueue()
        currentState = self.estadoInicial

        allInaccesibleFound = False
        while not allInaccesibleFound:

            isAccesible[currentState] = True
            newAccesibleStates = []
            stateDelta = self.delta[currentState]
            targets = list(stateDelta.values())  # Hallamos los estados a los que hay transiciones desde este estado

            for target in targets:
                for individualState in target:
                    newAccesibleStates.append(individualState)
            newAccesibleStates = list(dict.fromkeys(newAccesibleStates))

            for accesibleState in newAccesibleStates:
                if not isAccesible[accesibleState]:
                    stack.put(accesibleState)

            currentState = stack.get() if not stack.empty() else None  # Desapilamos
            allInaccesibleFound = True if currentState is None else False  # No hay más estados por recorrer

        inaccesibleStates = [state for state in isAccesible if not isAccesible[state]]
        return inaccesibleStates

    def calcularLambdaClausura(self, st: str = None, states: list[str] = None) -> list[str]:
        if st is not None and states is not None:
            raise Exception("Para calcular la lambda clausura, pasar, o solo un estado, o solo un conjunto de estados")

        if st is not None:
            states = [st]

        lambdaClosure = states.copy()  # Los estados mismos pertenecen a su lambda clausura
        for state in states:
            stack = LifoQueue()

            currentState = state
            allStatesFound = False
            while not allStatesFound:
                transitions = self.delta.get(currentState)
                lambdaStates = transitions.get('$')

                if lambdaStates is not None:
                    for targetState in lambdaStates:
                        if not lambdaClosure.__contains__(targetState):
                            lambdaClosure.append(targetState)
                            stack.put(targetState)

                currentState = stack.get() if not stack.empty() else None
                allStatesFound = True if currentState is None else False

        lambdaClosure = list(set(lambdaClosure))  # Remover duplicados
        lambdaClosure.sort()  # Para que aparezcan en orden los estados
        return lambdaClosure


    def procesarCadena(self, cadena: str, toPrint=False) -> bool:

        """
        ProcesarCadena. Toma la cadena, evalúa si es aceptada o no.
        El argumento toPrint sirve para determinar si se quiere imprimir el procesamiento de la cadena (en caso de ser
        aceptada)
        """

        completeProcessing = self.computarTodosLosProcesamientos(cadena, simpleProcessing=True)
        processing: list = completeProcessing[0]  # El procesamiento de la cadena
        isAccepted: bool = completeProcessing[1]

        if toPrint:
            if isAccepted:
                print("Cadena " + cadena + " Aceptada")
                for transition in processing:
                    print("(" + transition[0] + "," + transition[1] + ") --> " + transition[2])
            else:
                print("Cadena " + cadena + "Rechazada")

        return isAccepted


    def procesarCadenaConDetalles(self, cadena: str) -> bool:
        return self.procesarCadena(cadena=cadena, toPrint=True)

    def computarTodosLosProcesamientos(self, cadena: str, simpleProcessing: bool = False) -> int or [str, bool]:
        """
            Argumentos:
                cadena: La cadena para ser procesada
                simpleProcessing: Si está activada como cierto, hará el algoritmo de la función procesarCadena.
                                  Eso significa que, apenas encuentre un procesamiento en el que se acepte la cadena,
                                  la función parará.
                                  Si está en falso, la función buscará todos los cómputos posibles, sea cual sea el
                                  resultado de cada uno de esos cómputos
        """

        iterator = Iterator(self, cadena)  # Por legibilidad, creamos un iterador para la cadena
        listOfProcessings = []  # Aquí guardamos todos los posibles procedimientos de esta cadena, para poder imprimirlos
                                # en pantalla luego.
        numberOfProcessings = 0

        def saveProcessingInfo(statusOfProcessing: str) -> None:  #
            """
            Esta función guarda los procesamientos en la lista de procesamientos (listOfProcessings)
            statusOfProcessing = Aceptada, Rechazada o abortada
            """
            if not simpleProcessing:
                nonlocal numberOfProcessings
                processingString = ''

                processings = list(iterator.printStack.queue)
                for step in processings:
                    stepString = step[0] + "," + step[1] + "-->"
                    processingString += stepString
                processingString += iterator.currentState + '. ' + statusOfProcessing

                listOfProcessings.append(processingString)

                numberOfProcessings += 1

        searchFinished = False

        while not searchFinished:
            goBack = True
            if iterator.cadenaFullyCovered():
                status = "Aceptada" if iterator.currentStateIsAcceptable() else "Rechazada"
                saveProcessingInfo(status)
                if status == "Aceptada" and simpleProcessing:
                    return [list(iterator.printStack.queue), True]
            else:
                if iterator.possibleTransitionsFromHere():
                    iterator.calculateTransitionsFromHere()
                    goBack = False
                else:
                    saveProcessingInfo("Abortada")

            if not iterator.exploringStack.empty():
                iterator.doStep(isComingBack=goBack)
            else:
                searchFinished = True

        if simpleProcessing:
            return False, None
        else:
            print("Procesando cadena '" + cadena + "': ")
            for processing in listOfProcessings:
                print(processing)

            return numberOfProcessings

    def AFN_LambdaToAFN(self) -> AFN:

        def printInSetFlavor(listToString: list[str]) -> str:  # Un método para obtener un string de una lista como un set
            listCommas = [elem + ',' for elem in listToString]
            return '{' + ''.join(listCommas)[:-1] + '}'

        # Primer paso: calcular las lambda clausuras:

        lambdaClosures = {}  # Aquí guardaremos la lambda clausura de cada estado

        print("Lambda Clausuras:")
        for estado in self.estados:
            lambdaClosure = self.calcularLambdaClausura(estado)
            lambdaClosures[estado] = lambdaClosure

            print('$[' + estado + '] = ' + printInSetFlavor(
                lambdaClosure))  # Imprimimos la lambda clausura de cada estado

        newDelta = {}  # El delta del nuevo autómata

        print("\nTransiciones:")

        for estado in self.estados:

            lambdaClosure = lambdaClosures[estado]

            deltaState = {}  # Aquí guardaremos el delta del estado particular

            for character in self.alfabeto:
                # Segundo paso: calcular el delta de cada estado de la lambda clausura con el carácter

                if character != '$':
                    intermediateStates = []

                    for state in lambdaClosure:
                        targets = self.delta[state]
                        if character in targets:
                            target = targets[character]
                            for subTarget in target:
                                intermediateStates.append(subTarget)

                    targets = []
                    if len(intermediateStates) != 0:
                        # Tercer paso: calcular la lambda clausura de ese conjunto de estados:
                        targets = self.calcularLambdaClausura(states=intermediateStates)

                        # Cuarto paso: unir este nuevo target al delta de este estado con este carácter.
                        if len(targets) > 0:
                            deltaState[character] = targets

                    print('d\'(' + estado + ',' + character +
                          ') = $[d($[' + estado + '],' + character +
                          ') = $[d(' + printInSetFlavor(lambdaClosure) + ',' + character +
                          ') = ' + printInSetFlavor(targets))

            newDelta[estado] = deltaState

        AFNtoReturn = AFN(alfabeto=self.alfabeto, estados=self.estados, estadoInicial=self.estadoInicial, estadosAceptacion=self.estadosAceptacion, delta=newDelta)
        return AFNtoReturn


class Iterator:
    """
    Clase que sirve para recorrer el autómata. Se usa en computarTodosLosProcesamientos.
    """
    def __init__(self, AFNL, cadena):
        self.AFNL: AFN_Lambda = AFNL
        self.cadena: str = cadena


        for character in cadena:
            if character not in self.AFNL.alfabeto:
                raise Exception("En la cadena se introdujo el carácter " + character + ", pero ese "
                                "carácter no existe en el alfabeto del autómata: " + self.AFNL.alfabeto.__str__())

        # El estado actual del autómata se puede determinar por dos cosas: El estado actual, y el índice del carácter
        # que acabamos de leer.

        # Ahora bien, otra variable que necesitamos es la cantidad transiciones, sean o no lambda, que hemos hecho hasta
        # el momento. Más adelante se explica por qué

        self.currentState = self.AFNL.estadoInicial
        self.index = 0
        self.transitionsDone = 0

        self.exploringStack = LifoQueue()  # Pila de caminos. Cuando se hace un paso computacional, es muy probable que haya otros
        # caminos posibles. Esos otros caminos hay que guardarlos porque puede ser necesario volver a ellos. Por eso,
        # se guardan en esta pila, para volver a ellos cuando haga falta.
        self.printStack = LifoQueue()  # Pila de impresión. Guarda la información de los procesamientos que
        # se han hecho en el camino que se está recorriendo ahora mismo. Hace falta para poder imprimir en la consola
        # y en los .txt los procesamientos por los que pasa la cadena. Es una pila porque, cuando nos devolvamos en la pila
        # de caminos, también tendremos que desapilar transiciones guardadas acá.

    def calculateTransitionsFromHere(self) -> None:  # Averiguar los posibles procesamientos desde el estado y el carácter
        # actual, y guardarlos en la pila exploringStack (la de los caminos posibles)
        currentChar = self.cadena[self.index]  # Avanzamos al siguiente carácter de la cadena

        # Guardamos en la pila todos los pasos posibles que podríamos dar desde acá
        def pushIntoList(stateList, char):
            if stateList is not None:
                for st in stateList:
                    pushStep = {
                        "currentState": self.currentState,
                        "character": char,
                        "targetState": st,
                        "index": self.index,
                        "transitionsDone": self.transitionsDone
                    }
                    self.exploringStack.put(pushStep)

        transitions = self.AFNL.delta.get(self.currentState)
        lambdaStates, charStates = transitions.get('$'), transitions.get(currentChar)

        pushIntoList(lambdaStates, '$')
        pushIntoList(charStates, currentChar)


    def doStep(self, isComingBack: bool) -> None:  # Dar el paso computacional.

        """
        isComingBack: Este booleano sirve para saber si nos estamos devolviendo.
        Devolvernos no significa que nos vamos a quedar en el estado en el que estábamos cuando apilamos esta transición,
        si no que vamos a hacer la transición que estaba apilada
        """

        step = self.exploringStack.get()

        self.currentState = step["targetState"]
        self.index = step["index"] + 1 if step["character"] != '$' else step["index"]
        transitionsUntilNow = self.transitionsDone
        self.transitionsDone = step["transitionsDone"] + 1

        previousState = step["currentState"]
        charToCurrentState = step["character"]
        toPrintStack = [previousState, charToCurrentState, self.currentState]

        if isComingBack:  # Esto significa que nos estamos devolviendo a un camino que antes no se había tomado.
            # La pila que de impresión debe actualizarse:
            for popTransition in range(0, transitionsUntilNow - self.transitionsDone + 1):
                self.printStack.get()

        self.printStack.put(toPrintStack)

    def possibleTransitionsFromHere(self) -> bool:  # Averiguar si, desde el estado en que estamos, se pueden hacer
        # transiciones con el carácter actual que está siendo procesado
        char = self.cadena[self.index]
        deltaState = self.AFNL.delta[self.currentState]
        return True if '$' in deltaState or char in deltaState else False

    def currentStateIsAcceptable(self) -> bool:
        return True if self.currentState in self.AFNL.estadosAceptacion else False

    def cadenaFullyCovered(self) -> bool:
        return True if self.index == len(self.cadena) else False



# firstAFNL = AFN_Lambda(nombreArchivo="firstAFNLtest.NFE")
# print(firstAFNL.__str__())

#secondAFNL = AFN_Lambda(nombreArchivo="secondAFNLtest.NFE")
# secondAFNL.AFN_LambdaToAFN()
# print(secondAFNL.calcularLambdaClausura('s0'))

print(secondAFNL.computarTodosLosProcesamientos("0111012").__str__() + " procesamientos")
# print(secondAFNL.computarTodosLosProcesamientos("102").__str__() + " procesamientos")
print(secondAFNL.procesarCadena("0111012", True))
# print(secondAFNL.procesarCadena("0", True))
# print(secondAFNL.procesarCadena("2", True))
# print(secondAFNL.procesarCadena("11", True))
# print(secondAFNL.procesarCadena("102", True))

# print(secondAFNL.__str__())
# print(secondAFNL.imprimirAFNLSimplificado())
# secondAFNL.exportar("HolaMundo.nfe")

# print(secondAFNL.procesarCadena("0111012"))
# print(secondAFNL.procesarCadena("0"))
# print(secondAFNL.procesarCadena("2"))
# print(secondAFNL.procesarCadena("11"))
# print(secondAFNL.procesarCadena("102"))
#
# print("----------------")
#

#afnFrom = secondAFNL.AFN_LambdaToAFN()

# print(afnFrom.procesarCadena("0111012"))
# print(afnFrom.procesarCadena("0"))
# print(afnFrom.procesarCadena("2"))
# print(afnFrom.procesarCadena("11"))
# print(afnFrom.procesarCadena("102"))


#alphabet: Alfabeto = Alfabeto(secondAFNL.alfabeto)
"""""
for i in range(0, 10):
    cadena = alphabet.generar_cadena_aleatoria(5)
    strLambda = secondAFNL.procesarCadena(cadena)
    strAFNNl = afnFrom.procesarCadena(cadena)
    if strLambda != strAFNNl:
        print("Discrepancia:")
        print("Cadena: " + cadena)
        print(strLambda)
        print(strAFNNl)
        print("---------------------------")
    print(i)
"""

# print(secondAFNL.calcularLambdaClausura(states=['s0', 's6']))

# lambdaClosureAFNL = AFN_Lambda(nombreArchivo="lambdaClausuraTest.NFE")

# print(lambdaClosureAFNL.__str__())
# print(lambdaClosureAFNL.calcularLambdaClausura(st='s0'))
# lambdaClosureAFNL.AFN_LambdaToAFN()
# print(lambdaClosureAFNL.procesarCadenaConDetalles('ba'))

'''
for state in lambdaClosureAFNL.estados:
    print(state + ":")
    print(lambdaClosureAFNL.calcularLambdaClausura(st=state))

print(lambdaClosureAFNL.calcularLambdaClausura(states=['s0', 's3']))
print(lambdaClosureAFNL.calcularLambdaClausura(states=['s5', 's6']))
'''

# toStringTestAFNL = AFN_Lambda(nombreArchivo="toStringTestAFNL")
# print(toStringTestAFNL.__str__())

# bifucationANFL = AFN_Lambda(nombreArchivo="bifurcationTest.NFE")
# print(bifucationANFL.__str__())
# print(bifucationANFL.procesarCadenaConDetalles('b'))
