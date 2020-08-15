var items = document.getElementById('items');
var precio = document.getElementById('total-precio');

const productos = document.getElementsByClassName('producto_precio');
var cantidad = document.getElementsByClassName('producto_cantidad');
const stock_disponible = document.getElementsByClassName('stock_cantidad');
var stocks = document.getElementsByClassName('stock');

items.textContent = "Subtotal (" + productos.length + " items)";

var precio_total = 0;
for (var i = 0; i < productos.length; i++) {
    var cadena = productos[i].textContent.replace('$', '');

    productos[i].textContent = productos[i].textContent.replace(/\B(?=(\d{3})+(?!\d))/g, ","); //Formateando no influye en la funcion

    var numero = parseInt(cadena);
    var cant = parseInt(cantidad[i].textContent);
    var stock_dispon = parseInt(stock_disponible[i].textContent); //Check si es es posible

    if (cant > stock_dispon) {
        stocks[i].textContent = "No hay stock suficiente."
        cantidad[i].style.color = "#F00" //Si no lo es lo pone en rojo
    }
    precio_total += numero * cant
};
    
precio.textContent = ("$" + precio_total).replace(/\B(?=(\d{3})+(?!\d))/g, ",");

Array.from(stocks).forEach(element => {
    if (element.textContent == "Stock Disponible") {
        element.style.color = '#208f46';
    } else {
        element.style.color = '#F00';
    }
});




