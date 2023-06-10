import random

class Alfabeto:
    def __init__(self, simbolos):
        self.simbolos = simbolos

    def generar_cadena_aleatoria(self, n):
        return ''.join(random.choice(self.simbolos) for _ in range(n))



#simbolos = ['0','1']

#sigma = Alfabeto(simbolos)
#print(sigma.generar_cadena_aleatoria(10))