var contenedor = document.getElementById('contenedor');
var oscuro = document.getElementById('oscuro');
var boton_uno = document.getElementById('boton_comprar');

boton_uno.onclick = function() {
    contenedor.classList.remove("pop_inactivo");
    oscuro.classList.remove("pop_inactivo")
}

oscuro.onclick = function() {
    contenedor.classList.add("pop_inactivo");
    oscuro.classList.add("pop_inactivo")
}