import React, { useState, useEffect } from "react";
import "./InstallButton.css";

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
            /*
            installEvent.userChoice.then((choiceResult) => {
                if (choiceResult.outcome === "accepted") {
                    console.log("El usuario aceptó la instalación.");
                } else {
                    console.log("El usuario rechazó la instalación.");
                }
            });
            */
        } else {
            alert("La instalación no está disponible en este momento.");
        }
    };

    return (
        <button className="install-button" onClick={handleInstallClick}>
            Instalar App
        </button>
    );
};

export default InstallButton;
