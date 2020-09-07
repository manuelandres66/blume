var stock = document.getElementById('stock');

if (stock.textContent == "Stock Disponible") {
    stock.style.color = '#208f46';
} else {
    stock.style.color = '#F00';
}

const boton_carrito = document.getElementById('boton_carrito');
const boton_ahora = document.getElementById('boton_comprar');
const joya_id = document.getElementById('id_joya');

boton_carrito.onclick = function() {
    window.location.href="/carro/?add=" + joya_id.textContent;
};

boton_ahora.onclick = function() {
    window.location.href="/carro/ahora/?joya=" + joya_id.textContent;
}

