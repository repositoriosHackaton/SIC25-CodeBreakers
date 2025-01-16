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

{
    /*style={{
    padding: "0.5rem 1rem",
    fontSize: "1rem",
    backgroundColor: "#007bff",
    color: "#fff",
    border: "none",
    borderRadius: "5px",
    cursor: "pointer",
}}*/
}
