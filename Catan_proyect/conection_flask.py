from flask import Flask, request, jsonify
from Exagons import Tablero
from game_iteraction import Juego
from Exagons import Hexagono
from Player import Jugador

app = Flask(__name__)

# Inicializa el juego
tablero = Tablero()
tablero.inicializar_tablero()
jugadores = [Jugador('Jugador 1'), Jugador('Jugador 2')]
juego = Juego(jugadores)

# Endpoint para lanzar los dados
@app.route('/lanzar_dados', methods=['GET'])
def lanzar_dados():
    resultado = juego.lanzar_dados()
    return jsonify({"resultado": resultado})

# Endpoint para realizar el turno de un jugador
@app.route('/turno_jugador', methods=['GET'])
def turno_jugador():
    juego.turno_jugador()
    return jsonify({"mensaje": "Turno completado"})

# Endpoint para iniciar el juego
@app.route('/iniciar_juego', methods=['GET'])
def iniciar_juego():
    juego.iniciar_juego()
    return jsonify({"mensaje": "Juego iniciado"})

# Endpoint para verificar la victoria
@app.route('/verificar_victoria', methods=['GET'])
def verificar_victoria():
    victoria = juego.verificar_victoria()
    return jsonify({"victoria": victoria})

# Endpoint para verificar los recursos disponibles
@app.route('/verificar_recursos', methods=['POST'])
def verificar_recursos():
    data = request.json
    recursos_a_intercambiar = data.get('recursos')
    recursos = juego.verificar_recursos(recursos_a_intercambiar)
    return jsonify({"recursos": recursos})

# Endpoint para comerciar con otro jugador
@app.route('/comerciar', methods=['POST'])
def comerciar():
    data = request.json
    jugador_nombre = data.get('jugador')
    recursos_a_intercambiar = data.get('recursos')
    jugador = next((j for j in jugadores if j.nombre == jugador_nombre), None)
    if jugador:
        otro_jugador = next((j for j in jugadores if j.nombre != jugador_nombre), None)
        if otro_jugador:
            resultado = juego.comerciar(otro_jugador, recursos_a_intercambiar)
            return jsonify({"mensaje": f"Comercio realizado: {resultado}"})
    return jsonify({"error": "Jugador no encontrado o comercio inválido"}), 404

# Endpoint para construir un camino
@app.route('/construir_camino', methods=['POST'])
def construir_camino():
    data = request.json
    jugador_nombre = data.get('jugador')
    posicion = data.get('posicion')
    jugador = next((j for j in jugadores if j.nombre == jugador_nombre), None)
    if jugador:
        jugador.construir_camino(posicion)
        return jsonify({"mensaje": f"{jugador_nombre} construyó un camino en {posicion}"})
    return jsonify({"error": "Jugador no encontrado"}), 404

# Endpoint para construir un asentamiento
@app.route('/construir_asentamiento', methods=['POST'])
def construir_asentamiento():
    data = request.json
    jugador_nombre = data.get('jugador')
    posicion = data.get('posicion')
    jugador = next((j for j in jugadores if j.nombre == jugador_nombre), None)
    if jugador:
        jugador.construir_asentamiento(posicion)
        return jsonify({"mensaje": f"{jugador_nombre} construyó un asentamiento en {posicion}"})
    return jsonify({"error": "Jugador no encontrado"}), 404

# Endpoint para construir una ciudad
@app.route('/construir_ciudad', methods=['POST'])
def construir_ciudad():
    data = request.json
    jugador_nombre = data.get('jugador')
    posicion = data.get('posicion')
    jugador = next((j for j in jugadores if j.nombre == jugador_nombre), None)
    if jugador:
        jugador.construir_ciudad(posicion)
        return jsonify({"mensaje": f"{jugador_nombre} construyó una ciudad en {posicion}"})
    return jsonify({"error": "Jugador no encontrado"}), 404

# Endpoint para recibir recursos
@app.route('/recibir_recursos', methods=['POST'])
def recibir_recursos():
    data = request.json
    jugador_nombre = data.get('jugador')
    tipo_recurso = data.get('tipo_recurso')
    cantidad = data.get('cantidad')
    jugador = next((j for j in jugadores if j.nombre == jugador_nombre), None)
    if jugador:
        jugador.recibir_recursos(tipo_recurso, cantidad)
        return jsonify({"mensaje": f"{jugador_nombre} recibió {cantidad} de {tipo_recurso}"})
    return jsonify({"error": "Jugador no encontrado"}), 404

# Endpoint para comerciar marítimamente
@app.route('/comerciar_maritimo', methods=['POST'])
def comerciar_maritimo():
    data = request.json
    recurso_dar = data.get('recurso_dar')
    recurso_recibir = data.get('recurso_recibir')
    tasa = data.get('tasa')
    resultado = juego.comerciar_marítimo(recurso_dar, recurso_recibir, tasa)
    return jsonify({"mensaje": f"Comercio marítimo realizado: {resultado}"})

# Endpoint para comerciar con otro jugador
@app.route('/comerciar_con_jugador', methods=['POST'])
def comerciar_con_jugador():
    data = request.json
    jugador_nombre = data.get('jugador')
    otro_jugador_nombre = data.get('otro_jugador')
    recurso_dar = data.get('recurso_dar')
    recurso_recibir = data.get('recurso_recibir')
    cantidad_dar = data.get('cantidad_dar')
    cantidad_recibir = data.get('cantidad_recibir')
    jugador = next((j for j in jugadores if j.nombre == jugador_nombre), None)
    otro_jugador = next((j for j in jugadores if j.nombre == otro_jugador_nombre), None)
    if jugador and otro_jugador:
        resultado = juego.comerciar_con_jugador(otro_jugador, recurso_dar, recurso_recibir, cantidad_dar, cantidad_recibir)
        return jsonify({"mensaje": f"Comercio realizado entre {jugador_nombre} y {otro_jugador_nombre}: {resultado}"})
    return jsonify({"error": "Jugador o otro jugador no encontrado"}), 404

# Endpoint para comprar una carta de desarrollo
@app.route('/comprar_carta_desarrollo', methods=['POST'])
def comprar_carta_desarrollo():
    resultado = juego.comprar_carta_desarrollo()
    return jsonify({"mensaje": f"Carta de desarrollo comprada: {resultado}"})

# Endpoint para usar una carta de desarrollo
@app.route('/usar_carta_desarrollo', methods=['POST'])
def usar_carta_desarrollo():
    data = request.json
    carta = data.get('carta')
    resultado = juego.usar_carta_desarrollo(carta, jugadores)
    return jsonify({"mensaje": f"Carta de desarrollo usada: {resultado}"})

# Endpoint para deshacer la última jugada
@app.route('/deshacer_ultima_jugada', methods=['POST'])
def deshacer_ultima_jugada():
    juego.deshacer_ultima_jugada()
    return jsonify({"mensaje": "Última jugada deshecha"})

# Endpoint para recibir recursos iniciales
@app.route('/recibir_recursos_iniciales', methods=['POST'])
def recibir_recursos_iniciales():
    data = request.json
    asentamiento = data.get('asentamiento')
    juego.recibir_recursos_iniciales(tablero, asentamiento)
    return jsonify({"mensaje": "Recursos iniciales recibidos"})

# Endpoint para pasar el turno
@app.route('/pasar_turno', methods=['POST'])
def pasar_turno():
    data = request.json
    indice_turno = data.get('indice_turno')
    juego.pasar_turno(jugadores, indice_turno)
    return jsonify({"mensaje": f"Turno de {jugadores[indice_turno].nombre} pasado"})

# Endpoint para mostrar el resumen de los jugadores
@app.route('/mostrar_resumen', methods=['GET'])
def mostrar_resumen():
    resumen = juego.mostrar_resumen(jugadores)
    return jsonify({"resumen": resumen})

# Endpoint para mostrar el tablero
@app.route('/mostrar_tablero', methods=['GET'])
def mostrar_tablero():
    tablero = juego.mostrar_tablero()
    return jsonify({"tablero": tablero})

# Endpoint para mover el ladrón
@app.route('/mover_ladron', methods=['POST'])
def mover_ladron():
    juego.mover_ladron()
    return jsonify({"mensaje": "Ladrón movido"})

if __name__ == '__main__':
    app.run(debug=True)


