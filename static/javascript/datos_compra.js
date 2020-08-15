var items = document.getElementById('items');
var precio = document.getElementById('total-precio');

const productos = document.getElementsByClassName('producto_precio');
var cantidad = document.getElementsByClassName('producto_cantidad');
const stock_disponible =  document.getElementsByClassName('stock_cantidad');

console.log(stock_disponible[0].textContent);

items.textContent = "Subtotal (" + productos.length + " items)";

function actualizar() {
    var precio_total = 0;
    for (var i = 0; i < productos.length; i++) {
        var cadena = productos[i].textContent.replace('$', '')
        var numero = parseInt(cadena)
        var cant = parseInt(cantidad[i].textContent)
        precio_total += numero * cant
    };
    precio.textContent = "$" + precio_total;
};

actualizar();


var stocks = document.getElementsByClassName('stock');

Array.from(stocks).forEach(element => {
    if (element.textContent == "Stock Disponible") {
        element.style.color = '#208f46';
    } else {
        element.style.color = '#F00';
    }
});




