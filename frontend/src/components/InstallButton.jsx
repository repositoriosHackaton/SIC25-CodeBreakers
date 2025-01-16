import React, { useState, useEffect } from "react";

const InstallButton = () => {
    const [installEvent, setInstallEvent] = useState(null);

    useEffect(() => {
        const handleBeforeInstallPrompt = (event) => {
            event.preventDefault();
            setInstallEvent(event);
        };

        window.addEventListener("beforeinstallprompt", handleBeforeInstallPrompt);

        return () => {
            window.removeEventListener("beforeinstallprompt", handleBeforeInstallPrompt);
        };
    }, []);

    const handleInstallClick = () => {
        if (installEvent) {
            installEvent.prompt();
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
                fontSize: "1.5rem",
                backgroundColor: "#28a745",
                color: "#f8f9fa",
                border: "none",
                borderRadius: ".5rem",
                cursor: "pointer",
                boxShadow: "0 6px 8px var(--color-base-dark-shadow)",
            }}
        >
            Instalar App
        </button>
    );
};

export default InstallButton;
