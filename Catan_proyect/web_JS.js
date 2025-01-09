document.addEventListener('DOMContentLoaded', () => {
    const iniciarJuegoBtn = document.getElementById('iniciar-juego');
    const lanzarDadosBtn = document.getElementById('lanzar-dados');
    const tablero = document.getElementById('tablero');

    // Crear hexágonos
    function crearHexagono(recurso, numero) {
        const hexagono = document.createElement('div');
        hexagono.classList.add('hexagono');
        hexagono.innerHTML = `
            <span>${recurso}</span><br>
            <span>${numero ? numero : ''}</span>
        `;
        return hexagono;
    }

    // Inicializar tablero (este método puede ser modificado dependiendo de los datos del servidor)
    function inicializarTablero(tableroData) {
        tablero.innerHTML = ''; // Limpiar el tablero
        tableroData.forEach( hex => {
            const { recurso, numero } = hex;
            tablero.appendChild(crearHexagono(recurso, numero));
        });
    }

    // Llamada al endpoint de iniciar juego
    iniciarJuegoBtn.addEventListener('click', async () => {
        const response = await fetch('/iniciar_juego');
        const data = await response.json();
        alert(data.mensaje);  // Muestra el mensaje de éxito
    });

    // Llamada al endpoint para lanzar dados
    lanzarDadosBtn.addEventListener('click', async () => {
        const response = await fetch('/lanzar_dados');
        const data = await response.json();
        alert(`Resultado: ${data.resultado}`); // Muestra el resultado de los dados
    });

    // Llamada al endpoint para mostrar el tablero
    async function mostrarTablero() {
        const response = await fetch('/mostrar_tablero');
        const data = await response.json();
        inicializarTablero(data.tablero);
    }

    // Inicializa el tablero al cargar la página
    mostrarTablero();
});
