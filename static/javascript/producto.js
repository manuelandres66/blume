var stock = document.getElementById('stock');

if (stock.textContent == "Stock Disponible") {
    stock.style.color = '#208f46';
} else {
    stock.style.color = '#F00';
}

var boton_uno = document.getElementById('boton_carrito');

boton_uno.onclick = function() {
    alert('En proceso');
}