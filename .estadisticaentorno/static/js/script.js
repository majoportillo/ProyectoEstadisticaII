document.addEventListener("DOMContentLoaded", function () {
    const select = document.getElementById("probabilidad");

    // Ejecutar al cargar
    mostrarCampos();

    // Ejecutar cada vez que se cambie la opción
    select.addEventListener("change", mostrarCampos);
});

function mostrarCampos() {
    const seleccion = document.getElementById("probabilidad").value;
    const contenedor = document.getElementById("campos");

    contenedor.innerHTML = "";

    if (seleccion === "DosRangos") {
        contenedor.innerHTML = `
            <input type="number" placeholder="Valor mínimo" class="w-full p-2 border border-gray-300 rounded mt-2">
            <input type="number" placeholder="Valor máximo" class="w-full p-2 border border-gray-300 rounded mt-2">
        `;
    } else {
        contenedor.innerHTML = `
            <input type="number" placeholder="Valor" class="w-full p-2 border border-gray-300 rounded mt-2">
        `;
    }
}

function mostrarContenido() {
    document.getElementById("caratula").style.display = "none";
    document.getElementById("contenido").style.display = "block";
}
