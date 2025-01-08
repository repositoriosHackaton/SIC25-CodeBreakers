import React, { useEffect } from "react";

const InstallButton2 = () => {
    useEffect(() => {
        // Asegurarnos de que el navegador soporte service worker
        if ("serviceWorker" in navigator) {
            // Registra el service worker
            navigator.serviceWorker
                .register("/serviceworker.js", { scope: "/" })
                .then((registration) => {
                    registration.unregister(); // Esto normalmente no se necesita, pero lo dejaremos para pruebas
                })
                .catch((error) => {
                    console.error("Error al registrar el service worker", error);
                });

            // Agregar evento para mostrar el prompt de instalación
            window.addEventListener("beforeinstallprompt", (event) => {
                // Prevenir el comportamiento por defecto del navegador
                event.preventDefault();

                // Guardamos el evento para poder dispararlo manualmente
                let installEvent = event;

                // Crear y agregar el botón de instalación al DOM
                const installDiv = document.getElementById("divInstallApp");
                installDiv.innerHTML = `
          <button id="installApp" class="btn btn-outline-secondary ms-1">
            Instalar App
          </button>
        `;

                // Manejar clic en el botón para mostrar el prompt de instalación
                installDiv.addEventListener("click", () => {
                    installEvent.prompt(); // Mostrar el prompt
                    installDiv.innerHTML = ""; // Limpiar el contenido del div después de la interacción
                });
            });
        }
    }, []); // Este useEffect solo se ejecuta una vez cuando el componente se monta

    return <div id="divInstallApp"></div>;
};

export default InstallButton2;
