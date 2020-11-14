var stock = document.getElementById('stock');

if (stock.textContent == "Stock Disponible") {
    stock.style.color = '#208f46';
} else {
    stock.style.color = '#F00';
}

var precio = document.getElementById('precio_precio');
const nombre = document.getElementById('titulo_informacion').textContent;

const boton_carrito = document.getElementById('boton_carrito');
var boton_ahora = document.getElementById('boton_comprar');
const joya_id = document.getElementById('id_joya');

if (precio.textContent === "$0") {
    precio.textContent = "Cotizar";
    boton_carrito.textContent = "Contactar";
    boton_carrito.style.marginLeft = "0";
    boton_carrito.style.width = "36.5vw";
    boton_ahora.style.display = "none";

    const nombre_url = nombre.replaceAll(' ', '%20');

    boton_carrito.onclick = function() {
        window.location.href = "https://wa.me/+573006535061?text=Hola%20blume%2C%20me%20interesa%20saber%20sobre%20%3A%20" + nombre_url;
    };
} else {
    boton_carrito.onclick = function() {
        window.location.href="/carro/?add=" + joya_id.textContent;
    };

    boton_ahora.onclick = function() {
        window.location.href="/carro/ahora/?joya=" + joya_id.textContent;
    }
};

