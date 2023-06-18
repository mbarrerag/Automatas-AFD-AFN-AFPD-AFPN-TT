from queue import LifoQueue
from AFN import AFN


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

            self.estadosInaccesibles = self.hallarEstadosInaccesibles()
            for estado in self.delta:
                if len(self.delta.get(estado)) == 0:
                    self.estadosLimbo.append(estado)

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
            print("Para calcular la lambda clausura, pasar, o solo un estado, o solo un conjunto de estados")

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
        return lambdaClosure  # Set para remover duplicados

    def procesarCadena(self, cadena: str, toPrint=False) -> bool:
        for character in cadena:
            if character not in self.alfabeto:
                raise Exception("En la cadena se introdujo el carácter " + character + ", pero ese "
                                "carácter no existe en el alfabeto del autómata: " + self.alfabeto.__str__())

        exploringStack = LifoQueue()  # Cuando la unidad de control tiene varios caminos posibles en un momento dado,
        # debe elegir uno. Los otros caminos que podría tomar deben ser recordados de alguna forma. En este programa,
        # esos caminos quedan guardados en esta pila. Si más adelante llegamos a un punto en el que no se puede seguir
        # procesando la cadena, iremos desapilando esta pila para poder optar por otro camino posible que esté apilado.

        printStack = LifoQueue()  # Una pila que recuerda las transiciones que llevamos, para poder luego imprimirlas

        currentState = self.estadoInicial
        index = -1  # El carácter que estamos procesando de la cadena
        transitionsDone = 0

        stringAccepted = False
        searchFinished = False

        def possibleTransitionsFromHere(char: str):
            deltaState = self.delta[currentState]
            return True if '$' in deltaState or char in deltaState else False

        while not searchFinished:
            if currentState in self.estadosAceptacion and index + 1 == len(cadena):
                # Estamos en un estado de aceptación, y ya procesamos todos los caracteres
                stringAccepted = True
                searchFinished = True
            # elif (currentState in noTransitionsFrom or index + 1 == len(cadena)) and exploringStack.empty():
            elif (not possibleTransitionsFromHere(cadena[index+1]) or index + 1 == len(cadena)) and exploringStack.empty():
                # Estamos en un estado de NO aceptación, desde este estado no hay transiciones a otros estados,
                # y no tenemos transiciones pendientes por explorar en la pila. La cadena es rechazada
                stringAccepted = False
                searchFinished = True
            # elif currentState in noTransitionsFrom or index + 1 == len(cadena):
            elif (not possibleTransitionsFromHere(cadena[index+1])) or index + 1 == len(cadena):
                # Como en el caso anterior, estamos en un estado de NO aceptación y desde este estado no hay
                # forma de ir a otro estado. Sin embargo, sí hay transiciones pendientes por hacer
                # Por tanto, tenemos que desapilar lo que esté en el tope de la pila, para volver allí.

                step = exploringStack.get()  # Nos devolvemos en el procesamiento y tomamos un nuevo camino
                currentState = step["state"]
                transitionsUntilNow = transitionsDone
                index = step["index"] + 1 if charToCurrentState != '$' else step["index"]
                transitionsDone = step["transitionsDone"] + 1

                for popTransition in range(0, transitionsUntilNow - transitionsDone + 1):
                    printStack.get()
                previousState = step["currentState"]
                charToCurrentState = step["character"]
                printStack.put("(" + previousState + "," + charToCurrentState + ") --> " + currentState)
            else:
                # En este caso vamos a hacer un paso computacional
                currentChar = cadena[index + 1]  # Avanzamos al siguiente carácter de la cadena

                # Guardermos en la pila todos los pasos posibles que podríamos dar desde acá
                # Esta función es útil para dicho propósito:
                def pushIntoList(stateList, char):
                    if stateList is not None:
                        for st in stateList:
                            pushStep = {
                                "currentState": currentState,
                                "character": char,
                                "state": st,
                                "index": index,
                                "transitionsDone": transitionsDone
                            }
                            exploringStack.put(pushStep)

                transitions = self.delta.get(currentState)
                lambdaStates, charStates = transitions.get('$'), transitions.get(currentChar)

                pushIntoList(lambdaStates, '$')
                pushIntoList(charStates, currentChar)

                # Una vez hemos apilado todas las transiciones posibles, desapilamos la que acabamos de poner de última,
                # y hacemos el paso computacional
                if not exploringStack.empty():
                    step = exploringStack.get()

                    # ------------- Primero hacemos esto para la pila de impresión de transiciones-------------------
                    previousState = step["currentState"]
                    charToCurrentState = step["character"]
                    currentState = step["state"]

                    printStack.put("(" + previousState + "," + charToCurrentState + ") --> " + currentState)
                    # --------------------------------------------------------------------------------------------------

                    # Ahora sí hacemos, como tal, el paso computacional:
                    index = step["index"] + 1 if charToCurrentState != '$' else step["index"]
                    transitionsDone = step["transitionsDone"] + 1

        if toPrint:
            print("Cadena '" + cadena + "': " + stringAccepted.__str__())
            auxStack = LifoQueue()
            while not printStack.empty():
                auxStack.put(printStack.get())
            while not auxStack.empty():
                print(auxStack.get())

        return stringAccepted

    def procesarCadenaConDetalles(self, cadena: str) -> bool:
        return self.procesarCadena(cadena=cadena, toPrint=True)

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
                            if type(target) is list:
                                for subTarget in target:
                                    intermediateStates.append(subTarget)
                            else:
                                intermediateStates.append(target)

                    targets = []
                    if len(intermediateStates) != 0:
                        # Tercer paso: calcular la lambda clausura de ese conjunto de estados:
                        targets = self.calcularLambdaClausura(states=intermediateStates)

                        # Cuarto paso: unir este nuevo target al delta de este estado con este carácter.
                        if len(targets) > 0:
                            deltaState[character] = targets[0] if len(targets) == 1 else targets

                    print('d\'(' + estado + ',' + character +
                          ') = $[d($[' + estado + '],' + character +
                          ') = $[d(' + printInSetFlavor(lambdaClosure) + ',' + character +
                          ') = ' + printInSetFlavor(targets))

            newDelta[estado] = deltaState

        print(newDelta)

# firstAFNL = AFN_Lambda(nombreArchivo="firstAFNLtest.NFE")
# print(firstAFNL.__str__())

secondAFNL = AFN_Lambda(nombreArchivo="secondAFNLtest.NFE")
# secondAFNL.AFN_LambdaToAFN()
# print(secondAFNL.calcularLambdaClausura('s0'))

# print(secondAFNL.procesarCadena("0111012", True))
print(secondAFNL.procesarCadena("0", True))
# print(secondAFNL.procesarCadena("2", True))
# print(secondAFNL.procesarCadena("11", True))
# print(secondAFNL.procesarCadena("102", True))

# print(secondAFNL.__str__())
# print(secondAFNL.imprimirAFNLSimplificado())
# secondAFNL.exportar("HolaMundo.nfe")


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
