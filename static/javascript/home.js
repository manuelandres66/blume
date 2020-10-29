
var cual_imagen = 1;

setInterval(cambiar_imagen, 3000);

function cambiar_imagen() {
    var img_str = "img_" + cual_imagen;
    var img = document.getElementById(img_str);
    img.style.color = "rgba(0,0,0,.5)";

    var imagen_str = "imagen_" + cual_imagen;
    var imagen = document.getElementById(imagen_str);
    imagen.style.display = "none";

    if (cual_imagen == 4) {
        cual_imagen = 1;
    } else {
        cual_imagen++;
    };

    var img_str = "img_" + cual_imagen;
    var img = document.getElementById(img_str);
    img.style.color = "#447ab6";

    var imagen_str = "imagen_" + cual_imagen;
    var imagen = document.getElementById(imagen_str);
    imagen.style.display = "block";
};

function cambiar(direcion) {
    var img_str = "img_" + cual_imagen;
    var img = document.getElementById(img_str);
    img.style.color = "rgba(0,0,0,.5)";

    var imagen_str = "imagen_" + cual_imagen;
    var imagen = document.getElementById(imagen_str);
    imagen.style.display = "none";

    if (direcion) {
        if (cual_imagen == 4) {
            cual_imagen = 1;
        } else {
            cual_imagen++;
        };
    } else {
        if (cual_imagen == 1) {
            cual_imagen = 4;
        } else {
            cual_imagen -= 1;
        };
    };

    var img_str = "img_" + cual_imagen;
    var img = document.getElementById(img_str);
    img.style.color = "#447ab6";

    var imagen_str = "imagen_" + cual_imagen;
    var imagen = document.getElementById(imagen_str);
    imagen.style.display = "block";
}