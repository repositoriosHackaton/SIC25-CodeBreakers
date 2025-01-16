import React, { useEffect, useState } from "react";

const InstallButton = () => {
    const [installEvent, setInstallEvent] = useState(null);

    useEffect(() => {
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
        }

        // Manejar el evento 'beforeinstallprompt'
        const handleBeforeInstallPrompt = (event) => {
            event.preventDefault();
            setInstallEvent(event); // Guardar el evento para dispararlo después
        };

        window.addEventListener("beforeinstallprompt", handleBeforeInstallPrompt);

        return () => {
            window.removeEventListener("beforeinstallprompt", handleBeforeInstallPrompt);
        };
    }, []);

    const handleInstallClick = () => {
        if (installEvent) {
            installEvent.prompt(); // Mostrar el prompt de instalación
            installEvent.userChoice.then((choiceResult) => {
                if (choiceResult.outcome === "accepted") {
                    console.log("El usuario aceptó la instalación.");
                } else {
                    console.log("El usuario rechazó la instalación.");
                }
            });
        } else {
            alert("La instalación no está disponible en este momento.");
        }
    };

    return (
        <button
            onClick={handleInstallClick}
            style={{
                padding: "0.5rem 1rem",
                fontSize: "1rem",
                backgroundColor: "#007bff",
                color: "#fff",
                border: "none",
                borderRadius: "5px",
                cursor: "pointer",
            }}
        >
            Instalar App
        </button>
    );
};

export default InstallButton;
