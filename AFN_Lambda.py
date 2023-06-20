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

        secciones = {"#alphabet": [], "#states": [], "#initial": [], "#accepting": [], "#transitions": [], "#limbo": [],
                     "#inaccessible": []}
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
            self.alfabeto.sort()  # Por comodidad, para que estén ordenados lexicográficamente los caracteres

            for line in secciones['#states']:
                self.estados.append(line)

            for line in secciones['#initial']:
                self.estadoInicial = line

            for line in secciones['#accepting']:
                self.estadosAceptacion.append(line)

            for line in secciones['#transitions']:
                source, letter = line.strip().split(':')
                letter, targets = letter.split('>')

                targets: list[str] = targets.split(';')
                if letter == '$' and source in targets:
                    targets.remove(source)
                    print("Transición lambda del estado " + source + " a sí mismo. ¡Ignorada!")

                if source not in self.delta:
                    self.delta[source] = {}
                if len(targets) != 0:
                    self.delta[source][letter] = targets

            for estado in self.estados:
                self.delta.update({estado: {}}) if estado not in self.delta else None

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

    def calcularLambdaClausura(self, individualState: str = None, states: list[str] = None) -> list[str]:
        if individualState is not None and states is not None:
            raise Exception("Para calcular la lambda clausura, pasar, o solo un estado, o solo un conjunto de estados")

        if individualState is not None:
            states = [individualState]

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
                print("Cadena '" + cadena + "' Aceptada")
                for transition in processing:
                    print("(" + transition[0] + "," + transition[1] + ") --> " + transition[2])
            else:
                print("Cadena '" + cadena + "' Rechazada")

        return isAccepted

    def procesarCadenaConDetalles(self, cadena: str) -> bool:
        return self.procesarCadena(cadena=cadena, toPrint=True)

    def computarTodosLosProcesamientos(self, cadena: str, simpleProcessing: bool = False,
                                       variousCadenas: bool = False, nombreArchivo: str = "AFNL") -> int or [str, bool] or [str]:
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

                processings = list(iterator.printStack.queue)
                processingString = ''
                for step in processings:
                    stepString = step[0] + "," + step[1] + "-->"
                    processingString += stepString

                if not variousCadenas:
                    processingString += iterator.currentState  #  + '. ' + statusOfProcessing
                    listOfProcessings.append([processingString, statusOfProcessing])
                else:
                    processingString += iterator.currentState
                    listOfProcessings.append([processingString, statusOfProcessing])

                numberOfProcessings += 1

        searchFinished = False

        while not searchFinished:
            goBack = True
            if iterator.cadenaFullyCovered():
                status = "Aceptada" if iterator.currentStateIsAcceptable() else "Rechazada"
                saveProcessingInfo(status)

                iterator.calculateTransitionsFromHere(weAreInLastCharacter=True)
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
            return None, False
        elif not variousCadenas:
            accepted = []
            rejected = []
            aborted = []

            print("Procesando cadena '" + cadena + "': ")
            for processing in listOfProcessings:
                string = processing[0] + ". " + processing[1]
                accepted.append(string) if processing[1] == "Aceptada" else None
                rejected.append(string) if processing[1] == "Rechazada" else None
                aborted.append(string) if processing[1] == "Abortada" else None
                print(string)

            archivoAceptadas = open(f"{nombreArchivo}Aceptadas.txt", 'w')
            archivoRechazadas = open(f"{nombreArchivo}Rechazadas.txt", 'w')
            archivoAbortadas = open(f"{nombreArchivo}Abortadas.txt", 'w')

            accepted = [proc + '\n' for proc in accepted]
            rejected = [proc + '\n' for proc in rejected]
            aborted = [proc + '\n' for proc in aborted]
            accepted = ''.join(accepted)
            rejected = ''.join(rejected)
            aborted = ''.join(aborted)

            archivoAceptadas.write(accepted)
            archivoRechazadas.write(rejected)
            archivoAbortadas.write(aborted)

            return numberOfProcessings
        else:
            return [listOfProcessings, numberOfProcessings]

    def procesarListaCadenas(self, listaCadenas: list[str], nombreArchivo: str, imprimirPantalla: bool):

        archivo = open(f"{nombreArchivo}.txt", 'w')
        output: str = ''

        for cadena in listaCadenas:

            cadenaProcessed: [list[str], int] = self.computarTodosLosProcesamientos(cadena, variousCadenas=True)
            allProcessings = cadenaProcessed[0]
            numProcessings = cadenaProcessed[1]
            acceptances = []
            rejections = []
            abortions = []

            for processing in allProcessings:
                acceptances.append(processing[0]) if processing[1] == "Aceptada" else None
                rejections.append(processing[0]) if processing[1] == "Rechazada" else None
                abortions.append(processing[0]) if processing[1] == "Abortada" else None

            numAcceptances = len(acceptances)
            numRejections = len(rejections)
            numAbortions = len(abortions)

            if len(acceptances) > 0:
                processingToPrint = min(acceptances, key=len) + '   Aceptada'
            elif len(rejections) > 0:
                processingToPrint = min(rejections, key=len) + '    Rechazada'
            elif len(abortions) > 0:
                processingToPrint = min(abortions, key=len) + '    Abortada'
            else:
                processingToPrint = "No hay procesamientos posibles"

            status = 'Sí' if len(acceptances) > 0 else 'No'

            reportString = (f"Cadena:                         {cadena} \n" +
                            f"Procesamiento:                  {processingToPrint} \n" +
                            f"Número de procesamientos:       {numProcessings.__str__()} \n" +
                            f"Procesamientos de aceptación    {numAcceptances.__str__()} \n" +
                            f"Procesamientos de rechazo       {numRejections.__str__()} \n" +
                            f"Procesamientos abortados        {numAbortions.__str__()} \n" +
                            f"¿Aceptada?                      {status}  \n" +
                            "----------------------------------------------\n"
                            )

            output += reportString

        if imprimirPantalla:
            print(output)

        archivo.write(output)
        archivo.close()

    def AFN_LambdaToAFN(self) -> AFN:

        def printInSetFlavor(
                listToString: list[str]) -> str:  # Un método para obtener un string de una lista como un set
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
                          ')] = $[d(' + printInSetFlavor(lambdaClosure) + ',' + character +
                          ')] = $[' + printInSetFlavor(intermediateStates) +
                          '] = ' + printInSetFlavor(targets))

            newDelta[estado] = deltaState

        AFNtoReturn = AFN(alfabeto=self.alfabeto, estados=self.estados, estadoInicial=self.estadoInicial,
                          estadosAceptacion=self.estadosAceptacion, delta=newDelta)
        return AFNtoReturn

    def AFN_LambdaToAFD(self):
        AFNo = self.AFN_LambdaToAFN()
        print("\nPaso a AFD:")
        AFDe = AFNo.AFNtoAFD()
        return AFDe

    def procesarCadenaConversion(self, cadena: str) -> bool:
        AFDe = self.AFN_LambdaToAFD()
        return AFDe.procesar_cadena(cadena)

    def procesarCadenaConDetallesConversion(self, cadena:str) -> bool:
        AFDe = self.AFN_LambdaToAFD()
        print(AFDe.__str__())
        return AFDe.procesar_cadena_con_detalles(cadena)


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

    def calculateTransitionsFromHere(self, weAreInLastCharacter: bool = False) -> None:  # Averiguar los posibles procesamientos desde el estado y el carácter
        # actual, y guardarlos en la pila exploringStack (la de los caminos posibles)

        currentChar = self.cadena[self.index] if not weAreInLastCharacter else None # Avanzamos al siguiente carácter de la cadena

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

        if not weAreInLastCharacter:
            charStates = transitions.get(currentChar)
            pushIntoList(charStates, currentChar)

        lambdaStates = transitions.get('$')
        pushIntoList(lambdaStates, '$')


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


# firstAFNL = AFN_Lambda(nombreArchivo="LambdafFirstTest.NFE")

secondAFNL = AFN_Lambda(nombreArchivo="LambdaSecondTest.NFE")
testingAlphabet = Alfabeto(secondAFNL.alfabeto)
print("Creado desde archivo")

print("\n-----------------------------------")

print("Lambda Clausuras")
for estado in secondAFNL.estados:
    print(f"{estado}: {secondAFNL.calcularLambdaClausura(individualState=estado)}")

print("\n-----------------------------------")

print("Lambda Clausuras de Conjuntos de estados")
listsOfTesting = [['s0', 's3', 's6'], ['s1', 's2', 's3'], ['s0', 's1', 's6', 's7']]
for test in listsOfTesting:
    print(f"{test}:  {secondAFNL.calcularLambdaClausura(states=test)}")

print("\n-----------------------------------")

print("Hallas estados inaccesibles")
print(secondAFNL.hallarEstadosInaccesibles())

print("\n-----------------------------------")

print("Imprimir autómata simplificado y completo")
print("Simplificado:")
print(secondAFNL.imprimirAFNLSimplificado())
print("Completo:")
print(secondAFNL.__str__())

print("\n-----------------------------------")

print("Exportar a archivo")
secondAFNL.exportar(nombreArchivo="ExportedTest.txt")

print("\n-----------------------------------")
print("Procesar en detalle")
secondAFNL.procesarCadenaConDetalles("0111012")
print('\n')
secondAFNL.procesarCadenaConDetalles(testingAlphabet.generar_cadena_aleatoria(5))

print("\n-----------------------------------")
print("Computar todos los procesamientos")

randomString = testingAlphabet.generar_cadena_aleatoria(5)
isAccepted = secondAFNL.computarTodosLosProcesamientos(randomString, nombreArchivo="allProcessings2")
print(f"{isAccepted.__str__()} Procesamientos")

print("\n-----------------------------------")
print("Procesar lista de cadenas")
listOfStrings = []
for i in range(0,5):
    listOfStrings.append(testingAlphabet.generar_cadena_aleatoria(n=5))
secondAFNL.procesarListaCadenas(listOfStrings, nombreArchivo="cesarAFNLTest", imprimirPantalla=True)

print("-----------------------------------")
print("Convertir a AFN:")
AFNFrom = secondAFNL.AFN_LambdaToAFN()

print("\n-----------------------------------")
print("Convertir a AFD:")
AFDFrom = secondAFNL.AFN_LambdaToAFD()

print("\n-----------------------------------")
print("Procesar con detalles a AFD:")
print(secondAFNL.procesarCadenaConDetallesConversion(cadena=testingAlphabet.generar_cadena_aleatoria(n=5)))

def testingAutomatas(afn: AFN_Lambda):
    alphabet = Alfabeto(afn.alfabeto)
    counterSuccess = 0
    trueFalsePairs = []

    archivo = open(f"AFNL-AFD-Results.txt", 'w')

    for i in range(0, 5000):
        cadena = alphabet.generar_cadena_aleatoria(i % 12)
        boolLambda = afn.procesarCadena(cadena)
        boolAfd = afn.procesarCadenaConversion(cadena)
        if boolAfd == boolLambda:
            counterSuccess += 1
        trueFalsePairs.append([boolLambda, boolAfd, cadena])
    archivo.write(f"Número de éxitos: {counterSuccess}\n")
    archivo.write(f"Número de fracasos: {5000-counterSuccess}\n\n")
    for pair in trueFalsePairs:
        archivo.write(pair[0].__str__() + ' ' + pair[1].__str__() + ', ' + pair[2] + '\n')


lTest = AFN_Lambda(nombreArchivo="LambdafFirstTest.NFE")
testingAutomatas(secondAFNL)



