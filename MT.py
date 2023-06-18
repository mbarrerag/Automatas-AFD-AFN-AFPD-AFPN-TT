class MT:
    def __init__(self, states=None, initial_state=None, accepting_states=None, input_alphabet=None, tape_alphabet=None, transitions=None, nombreArchivo=None):
    
        if nombreArchivo:
            self.cargar_desde_archivo(nombreArchivo)
            
        else:
            self.states = states
            self.current_state = initial_state
            self.accepting_states = accepting_states
            self.input_alphabet = input_alphabet
            self.tape_alphabet = tape_alphabet
            self.transitions = transitions
            self.tape = list()

    def cargar_desde_archivo(self, nombreArchivo):
        self.states = []
        self.current_state = None
        self.accepting_states = []
        self.input_alphabet = []
        self.tape_alphabet = []
        self.transitions = {}
        self.tape = list()

        secciones = {"#tapeAlphabet": [], "#states": [], "#initial": [], "#accepting": [], "#transitions": [], "#inputAlphabet": []}
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
            for line in secciones['#inputAlphabet']:
                # Validar si es un rango o un caracter individual
                if '-' in line and len(line.split('-')) == 2:  # Asegurarse de que la línea solo contenga dos partes
                    start, end = line.split('-')
                    self.input_alphabet += [chr(x) for x in range(ord(start), ord(end) + 1) if chr(x) != '$']
                else:
                    if line != '$':
                        self.input_alphabet.append(line)

            # Convertir el alfabeto a un conjunto para eliminar duplicados, y luego volver a una lista
            self.input_alphabet = list(set(self.input_alphabet))

            for line in secciones['#tapeAlphabet']:
                # Validar si es un rango o un caracter individual
                if '-' in line and len(line.split('-')) == 2:  # Asegurarse de que la línea solo contenga dos partes
                    start, end = line.split('-')
                    self.tape_alphabet += [chr(x) for x in range(ord(start), ord(end) + 1) if chr(x) != '$']
                else:
                    if line != '$':
                        self.tape_alphabet.append(line)

            # Convertir el alfabeto a un conjunto para eliminar duplicados, y luego volver a una lista
            self.tape_alphabet = list(set(self.tape_alphabet))

            for line in secciones['#states']:
                self.states.append(line)

            for line in secciones['#initial']:
                self.current_state = line

            for line in secciones['#accepting']:
                self.accepting_states.append(line)

            for line in secciones['#transitions']:
                if line:
                    first_part, second_part = line.split('?') # Separar la transición en dos partes
                    state_current, symbol_read = first_part.split(':') # Separar la primera parte en estado actual y símbolo leído
                    state_next, symbol_write, direction = second_part.split(':') # Separar la segunda parte en estado siguiente, símbolo a escribir y dirección
                    key = (state_current.strip(), symbol_read) # Crear la llave de la transición
                    value = (state_next, symbol_write, direction.strip()) # Crear el valor de la transición
                    self.transitions[key] = value

    def __str__(self):
        output = "!TM\n"

        output += "#states\n"
        output += "\n".join(self.states) + "\n"

        output += "#initial\n"
        output += self.current_state + "\n"

        output += "#accepting\n"
        output += "\n".join(self.accepting_states) + "\n"

        output += "#inputAlphabet\n"
        
                # Ordenar el alfabeto eliminando duplicados
        sorted_alfabeto = sorted(set(self.input_alphabet), key=ord)
        
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

        output += "#tapeAlphabet\n"
        
                # Ordenar el alfabeto eliminando duplicados
        sorted_alfabeto = sorted(set(self.tape_alphabet), key=ord)
        
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

        output += "#transitions\n"
        for transition_key, transition_value in self.transitions.items():
            (state, symbol), (new_state, new_symbol, direction) = transition_key, transition_value
            output += f"{state}:{symbol}?{new_state}:{new_symbol}:{direction}\n"

        return output
 


    def procesarCadenaConDetalles(self, cadena):
        current_state = self.current_state
        tape = list(cadena)
        posicion = 0

        # Imprimir el estado inicial
        print("(" + current_state + ")" + "".join(tape))

        while True:
            # leer el símbolo actual de la cinta
            if posicion < len(tape):
                simbolo_actual = tape[posicion]
            else:
                simbolo_actual = '!'  # '!' representa un espacio en blanco

            # obtener la transición para el estado actual y el símbolo actual
            transicion = self.transitions.get((current_state, simbolo_actual))

            if transicion is None:  # si no hay transición, la cadena es rechazada
                return False

            # realizar la transición: cambiar al estado siguiente, escribir en la cinta y mover la cinta
            current_state, simbolo_escritura, direccion = transicion
            if posicion < len(tape):
                tape[posicion] = simbolo_escritura
            else:
                tape.append(simbolo_escritura)

            # imprimir el estado actual y la cinta
            cinta_string = "".join(tape)
            print(cinta_string[:posicion] + "(" + current_state + ")" + cinta_string[posicion + 1:])

            # mover la cinta
            if direccion == '>':
                posicion += 1
            elif direccion == '<':
                posicion = max(0, posicion - 1)
            else:
                break  # si la dirección es '-', terminamos el procesamiento

        # al final, la cadena es aceptada si la máquina está en un estado de aceptación
        return current_state in self.accepting_states
    
    def procesarCadenaConDetallesPrint(self, cadena):
        current_state = self.current_state
        tape = list(cadena)
        posicion = 0

        # Inicializar la cadena de salida con el estado inicial
        output = "(" + current_state + ")" + "".join(tape) + '\t'

        while True:
            if posicion < len(tape):
                simbolo_actual = tape[posicion]
            else:
                simbolo_actual = '!'

            transicion = self.transitions.get((current_state, simbolo_actual))

            if transicion is None:  
                print(output.rstrip('\t'))  # imprimir la cadena de salida sin la última tabulación
                return (False, "".join(tape)) 

            current_state, simbolo_escritura, direccion = transicion
            if posicion < len(tape):
                tape[posicion] = simbolo_escritura
            else:
                tape.append(simbolo_escritura)

            # añadir el estado actual y la cinta a la cadena de salida
            cinta_string = "".join(tape)
            output += cinta_string[:posicion] + "(" + current_state + ")" + cinta_string[posicion + 1:] + '\t'

            if direccion == '>':
                posicion += 1
            elif direccion == '<':
                posicion = max(0, posicion - 1)
            else:
                break  

        print(output.rstrip('\t'))  # imprimir la cadena de salida sin la última tabulación
        return (current_state in self.accepting_states, "".join(tape))


    def procesarCadena(self, cadena):
        current_state = self.current_state
        tape = list(cadena)
        posicion = 0

        while True:
            # leer el símbolo actual de la cinta
            if posicion < len(tape):
                simbolo_actual = tape[posicion]
            else:
                simbolo_actual = '!'  # '!' representa un espacio en blanco

            # obtener la transición para el estado actual y el símbolo actual
            transicion = self.transitions.get((current_state, simbolo_actual))

            if transicion is None:  # si no hay transición, la cadena es rechazada
                return False

            # realizar la transición: cambiar al estado siguiente, escribir en la cinta y mover la cinta
            current_state, simbolo_escritura, direccion = transicion
            if posicion < len(tape):
                tape[posicion] = simbolo_escritura
            else:
                tape.append(simbolo_escritura)

            # mover la cinta
            if direccion == '>':
                posicion += 1
            elif direccion == '<':
                posicion = max(0, posicion - 1)
            else:
                break  # si la dirección es '-', terminamos el procesamiento

        # al final, la cadena es aceptada si la máquina está en un estado de aceptación
        return current_state in self.accepting_states
    
    def procesarFuncion(self, cadena):
        current_state = self.current_state
        cinta = list(cadena)
        posicion = 0

        while True:
            # leer el símbolo actual de la cinta
            if posicion < len(cinta):
                simbolo_actual = cinta[posicion]
            else:
                simbolo_actual = '!'  # asumimos que ! representa un espacio en blanco

            # obtener la transición para el estado actual y el símbolo actual
            transicion = self.transitions.get((current_state, simbolo_actual))

            if transicion is None:  # si no hay transición, la cadena es rechazada
                break

            # realizar la transición: cambiar al estado siguiente, escribir en la cinta y mover la cinta
            current_state, simbolo_escritura, direccion = transicion
            if posicion < len(cinta):
                cinta[posicion] = simbolo_escritura
            else:
                cinta.append(simbolo_escritura)

            if direccion == '>':
                posicion += 1
            elif direccion == '<':
                posicion = max(0, posicion - 1)
            else:
                break  # si la dirección es '-', terminamos el procesamiento

        # al final, retornamos la cinta como una cadena
        return "".join(cinta)

    def procesarListaCadenas(self, listaCadenas, nombreArchivo, imprimirPantalla):
        try:
            file = open(nombreArchivo, 'w')
        except:
            file = open('resultados.txt', 'w')  # nombre por defecto

        for cadena in listaCadenas:
            final_cinta = self.procesarFuncion(cadena) 
            es_aceptada = self.procesarCadena(cadena) 

            resultado = '\t'.join([cadena, final_cinta, 'yes' if es_aceptada else 'no'])

            file.write(resultado + '\n')
            if imprimirPantalla:
                print(resultado)

        file.close()


#prueba usando TM de palindromes pares

#Turing = MT(nombreArchivo="MT.tm")  
#print(Turing.procesarCadenaConDetalles("ababa"))
#print(Turing.procesarCadena("ababa"))
#print(Turing.procesarFuncion("aabbaa"))
#Turing.procesarListaCadenas(["aaaa", "aabbaa", "ababa"], "resultadosTM.txt", True)
#print(Turing)

      