from random import random

class Tablero:
    def __init__(self):
        self.hexagonos = []

    def inicializar_tablero(self):
        recursos = ['madera'] * 4 + ['ladrillo'] * 3 + ['trigo'] * 4 + ['lana'] * 4 + ['mineral'] * 3 + ['desierto']
        numeros = [2, 3, 3, 4, 4, 5, 5, 6, 6, 8, 8, 9, 9, 10, 10, 11, 11, 12]

        random.shuffle(recursos)
        random.shuffle(numeros)

        # Distribución de los 19 hexágonos
        posiciones = [
            [(0, 0)],                   # Fila 1
            [(1, 0), (1, 1)],           # Fila 2
            [(2, 0), (2, 1), (2, 2)],   # Fila 3
            [(3, 0), (3, 1), (3, 2), (3, 3)],  # Fila 4
            [(4, 0), (4, 1), (4, 2)],   # Fila 5
            [(5, 0), (5, 1)],           # Fila 6
            [(6, 0)]                    # Fila 7
        ]

        # Crear hexágonos con sus coordenadas (q, r)
        for fila in posiciones:
            for (q, r) in fila:
                recurso = recursos.pop()
                hexagono = Hexagono(recurso, q, r)
                self.hexagonos.append(hexagono)

        # Asignar números a los hexágonos (excepto al desierto)
        for hexagono in self.hexagonos:
            if hexagono.recurso != 'desierto':
                hexagono.asignar_numero(numeros.pop())
            else:
                hexagono.mover_ladron()

    def obtener_adyacentes(self, q, r):
        """Devuelve los hexágonos adyacentes dados las coordenadas q, r."""
        # Lista de posibles vecinos
        vecinos_posibles = [
            (q-1, r), (q+1, r), (q, r-1), (q, r+1), (q-1, r+1), (q+1, r-1)
        ]
        
        # Filtra aquellos vecinos que existan en el tablero
        vecinos = []
        for (q_adyacente, r_adyacente) in vecinos_posibles:
            for hexagono in self.hexagonos:
                if hexagono.q == q_adyacente and hexagono.r == r_adyacente:
                    vecinos.append(hexagono)
                    break
        return vecinos

    def mostrar_tablero(self):
        for hexagono in self.hexagonos:
            print(hexagono)

# Clase Hexágono que tiene las coordenadas (q, r)
class Hexagono:
    def __init__(self, recurso, q, r):
        self.recurso = recurso
        self.q = q  # Coordenada horizontal
        self.r = r  # Coordenada vertical
        self.numero = None  # El número asignado por el dado, si no es el desierto

    def asignar_numero(self, numero):
        self.numero = numero

    def mover_ladron(self):
        self.numero = 'Ladrón'

    def __str__(self):
        return f"Hexágono ({self.q}, {self.r}): {self.recurso}, Número: {self.numero}"

