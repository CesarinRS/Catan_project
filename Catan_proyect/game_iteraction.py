import random

class Juego:
    def __init__(self, jugadores):
        self.jugadores = jugadores
        self.turno = 0
    
    def lanzar_dados(self):
        dado1 = random.randint(1, 6)  # Primer dado
        dado2 = random.randint(1, 6)  # Segundo dado
        total = dado1 + dado2
        print(f"Lanzamiento de dados: {dado1} + {dado2} = {total}")
        return total
    
    def turno_jugador(self):
        jugador_actual = self.jugadores[self.turno]
        print(f"Es el turno de {jugador_actual.nombre}")
        
        # Lanzar los dados
        resultado = self.lanzar_dados()
        
        # Aquí podrías añadir la lógica para generar recursos según el resultado de los dados
        
        # Cambiar el turno al siguiente jugador
        self.turno = (self.turno + 1) % len(self.jugadores)

    def verificar_victoria(self):
        for jugador in self.jugadores:
            if jugador.puntos_victoria >= 10:  # Asumimos que 10 puntos de victoria es suficiente
                print(f"{jugador.nombre} ha ganado el juego!")
                return True
        return False

    def iniciar_juego(self):
        while True:
            self.turno_jugador()
            if self.verificar_victoria():
                break

