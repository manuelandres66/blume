var precios = document.getElementsByClassName('precios');
for (let i = 0; i < precios.length; i++) {
    if (precios[i].textContent == "0") {
        precios[i].textContent = "Cotizar";
    } else {
        precios[i].textContent = "$" + precios[i].textContent.replace(/\B(?=(\d{3})+(?!\d))/g, ".");
    };
};

const joyaSubmit = () => {
    document.getElementById('buscador').submit();
}