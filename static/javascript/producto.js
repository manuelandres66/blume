var stock = document.getElementById('stock');

if (stock.textContent == "Stock Disponible") {
    stock.style.color = '#208f46';
} else {
    stock.style.color = '#F00';
}

const boton_uno = document.getElementById('boton_carrito');
const joya_id = document.getElementById('id_joya');

boton_uno.onclick = function() {
    window.location.href="/carro/?add=" + joya_id.textContent;
}