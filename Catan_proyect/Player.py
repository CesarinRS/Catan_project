class Jugador:
    def __init__(self, nombre):
        self.nombre = nombre
        self.recursos = {'madera': 0, 'ladrillo': 0, 'trigo': 0, 'lana': 0, 'mineral': 0}
        self.puntos_victoria = 0
        self.caminos = []
        self.asentamientos = []
        self.ciudades = []
        self.cartas_desarrollo = []
        self.puertos = []  # Lista de puertos que posee el jugador
        self.historial_jugadas = []
    
    def verificar_recursos(self, recursos_a_intercambiar):
        for recurso, cantidad in recursos_a_intercambiar.items():
            if self.recursos.get(recurso, 0) < cantidad:
                return False  # No tiene suficientes recursos
        return True

    def comerciar(self, otro_jugador, recursos_a_intercambiar):
        if not self.verificar_recursos(recursos_a_intercambiar):
            print(f"Error: {self.nombre} no tiene suficientes recursos para el intercambio.")
            return
        if not otro_jugador.verificar_recursos(recursos_a_intercambiar):
            print(f"Error: {otro_jugador.nombre} no tiene suficientes recursos para el intercambio.")
            return

        # Realiza el intercambio
        for recurso, cantidad in recursos_a_intercambiar.items():
            self.recursos[recurso] -= cantidad
            otro_jugador.recursos[recurso] += cantidad
        print(f"Intercambio realizado entre {self.nombre} y {otro_jugador.nombre}")

    def construir_camino(self, posicion):
        self.caminos.append(posicion)
        print(f"{self.nombre} construyó un camino en {posicion}")

    def construir_asentamiento(self, posicion):
        self.asentamientos.append(posicion)
        print(f"{self.nombre} construyó un asentamiento en {posicion}")

    def construir_ciudad(self, posicion):
        if posicion in self.asentamientos:
            self.asentamientos.remove(posicion)
            self.ciudades.append(posicion)
            print(f"{self.nombre} mejoró un asentamiento a una ciudad en {posicion}")

    def recibir_recursos(self, tipo_recurso, cantidad):
        self.recursos[tipo_recurso] += cantidad
        print(f"{self.nombre} recibió {cantidad} de {tipo_recurso}")

    def comerciar_marítimo(self, recurso_dar, recurso_recibir, tasa):
        if self.recursos[recurso_dar] >= tasa:
            self.recursos[recurso_dar] -= tasa
            self.recursos[recurso_recibir] += 1
            print(f"{self.nombre} intercambió {tasa} de {recurso_dar} por 1 de {recurso_recibir} en el comercio marítimo.")
        else:
            print(f"{self.nombre} no tiene suficientes {recurso_dar} para comerciar.")

    def comerciar_con_jugador(self, otro_jugador, recurso_dar, recurso_recibir, cantidad_dar, cantidad_recibir):
        """
        Permite que el jugador comercie con otro jugador.
        """
        if self.recursos[recurso_dar] >= cantidad_dar and otro_jugador.recursos[recurso_recibir] >= cantidad_recibir:
            self.recursos[recurso_dar] -= cantidad_dar
            self.recursos[recurso_recibir] += cantidad_recibir
            otro_jugador.recursos[recurso_dar] += cantidad_dar
            otro_jugador.recursos[recurso_recibir] -= cantidad_recibir
            print(f"{self.nombre} ha intercambiado {cantidad_dar} de {recurso_dar} con {otro_jugador.nombre} por {cantidad_recibir} de {recurso_recibir}")
        else:
            print(f"No se puede realizar el comercio. Verifica los recursos disponibles de ambos jugadores.")

    def comprar_carta_desarrollo(self):
        """
        Permite al jugador comprar una carta de desarrollo si tiene los recursos necesarios.
        """
        # Verificar si el jugador tiene los recursos necesarios
        if (self.recursos['trigo'] >= 1 and self.recursos['lana'] >= 1 and self.recursos['mineral'] >= 1):
            # Realizar la compra de la carta de desarrollo
            self.recursos['trigo'] -= 1
            self.recursos['lana'] -= 1
            self.recursos['mineral'] -= 1
            self.cartas_desarrollo.append("Carta de Desarrollo")
            print(f"{self.nombre} compró una carta de desarrollo.")
        else:
            print(f"{self.nombre} no tiene suficientes recursos para comprar una carta de desarrollo.")

    def usar_carta_desarrollo(self, carta, jugadores):
        if carta in self.cartas_desarrollo:
            if carta == 'Caballero':
                self.cartas_desarrollo.remove(carta)
                self.caballeros += 1
                print(f"{self.nombre} usó un Caballero para mover al ladrón.")
            elif carta == 'Carretera':
                self.cartas_desarrollo.remove(carta)
                # Aquí puedes agregar la lógica de construcción de una carretera (2 caminos adicionales)
                print(f"{self.nombre} usó una carta de Carretera para construir dos caminos.")
            elif carta == 'Punto de Victoria':
                self.cartas_desarrollo.remove(carta)
                self.puntos_victoria += 1
                print(f"{self.nombre} usó una carta de Punto de Victoria y ahora tiene {self.puntos_victoria} puntos de victoria.")
            elif carta == 'Progreso':
                self.cartas_desarrollo.remove(carta)
                recurso_1 = input(f"{self.nombre}, elige el primer recurso para recibir (madera, ladrillo, trigo, lana, mineral): ")
                recurso_2 = input(f"{self.nombre}, elige el segundo recurso para recibir (madera, ladrillo, trigo, lana, mineral): ")
                if recurso_1 in self.recursos and recurso_2 in self.recursos:
                    self.recibir_recursos(recurso_1, 1)
                    self.recibir_recursos(recurso_2, 1)
                print(f"{self.nombre} usó una carta de Progreso y recibió 1 de {recurso_1} y 1 de {recurso_2}.")
            elif carta == 'Monopolio':
                self.cartas_desarrollo.remove(carta)
                recurso = input(f"{self.nombre}, elige el recurso para robar (madera, ladrillo, trigo, lana, mineral): ")
                if recurso in self.recursos:
                    for jugador in jugadores:
                        if jugador != self:
                            if recurso in jugador.recursos and jugador.recursos[recurso] > 0:
                                cantidad_robada = jugador.recursos[recurso]
                                self.recursos[recurso] += cantidad_robada
                                jugador.recursos[recurso] = 0
                                print(f"{self.nombre} usó Monopolio y robó {cantidad_robada} de {recurso} a {jugador.nombre}.")
                else:
                    print(f"{self.nombre} no tiene el recurso {recurso} para robar.")
        else:
            print(f"{self.nombre} no tiene una carta de desarrollo de tipo {carta} para usar.")
    
    def deshacer_ultima_jugada(self):
        # Solo se deshacen las jugadas constructivas
        if self.historial_jugadas:
            ultima_jugada = self.historial_jugadas.pop()
            tipo, accion, posicion = ultima_jugada

            # Dependiendo del tipo de acción, deshacerla
            if tipo == 'camino' and accion == 'agregar':
                self.caminos.remove(posicion)
                print(f"{self.nombre} deshizo la construcción del camino en {posicion}")
            elif tipo == 'asentamiento' and accion == 'agregar':
                self.asentamientos.remove(posicion)
                print(f"{self.nombre} deshizo la construcción del asentamiento en {posicion}")
            elif tipo == 'ciudad' and accion == 'agregar':
                self.ciudades.remove(posicion)
                self.asentamientos.append(posicion)  # Volver a poner el asentamiento
                print(f"{self.nombre} deshizo la construcción de la ciudad en {posicion}")
            elif tipo == 'asentamiento' and accion == 'eliminar':
                self.asentamientos.append(posicion)
                print(f"{self.nombre} deshizo la eliminación del asentamiento en {posicion}")

        else:
            print(f"{self.nombre} no tiene jugadas para deshacer.")

    def recibir_recursos_iniciales(self, tablero, asentamiento):
        """Asigna recursos según los hexágonos adyacentes al asentamiento"""
        recursos_recibidos = []
        
        # Suponiendo que 'tablero' es un objeto que contiene todos los hexágonos
        # y que 'asentamiento' es una tupla con las coordenadas de la posición
        for hexagono in tablero.obtener_adyacentes(asentamiento[0],asentamiento[1]):
            tipo_recurso = hexagono.recurso
            self.recibir_recursos(tipo_recurso, 1)
            recursos_recibidos.append(tipo_recurso)

    def pasar_turno(jugadores, indice_turno):
        """
        Función para pasar el turno entre los jugadores.
        """
        # Se pasa al siguiente jugador cíclicamente
        indice_turno = (indice_turno + 1) % len(jugadores)
        print(f"Es el turno de {jugadores[indice_turno].nombre}.")
        return indice_turno  # Corregir el nombre de la variable a 'indice_turno'

    def mostrar_resumen(jugadores):
        for jugador in jugadores:
         print(jugador)
        print("\n")

           
    def __str__(self):
        return f"Jugador: {self.nombre}, Puntos de Victoria: {self.puntos_victoria}, Recursos: {self.recursos}, Cartas de Desarrollo: {len(self.cartas_desarrollo)}, Puertos: {self.puertos}"





