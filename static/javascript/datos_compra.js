var items = document.getElementById('items');
var precio = document.getElementById('total-precio');

const productos = document.getElementsByClassName('producto_precio');

items.textContent = "Subtotal (" + productos.length + " items)";

var precio_total = 0;

Array.from(productos).forEach(element => {
    var cadena = element.textContent.replace('$', '')
    var numero = parseInt(cadena)
    precio_total += numero
});

precio.textContent = "$" + precio_total
