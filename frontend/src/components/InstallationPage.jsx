import React, { useEffect } from "react";

const InstallationPage = () => {
    useEffect(() => {
        let installPromptEvent = null;

        const handleBeforeInstallPrompt = (event) => {
            event.preventDefault(); // Evitar el prompt automático
            installPromptEvent = event;
        };

        window.addEventListener("beforeinstallprompt", handleBeforeInstallPrompt);

        return () => {
            window.removeEventListener("beforeinstallprompt", handleBeforeInstallPrompt);
        };
    }, []);

    const handleInstallClick = () => {
        if (installPromptEvent) {
            installPromptEvent.prompt(); // Disparar el prompt manualmente
            installPromptEvent.userChoice.then((choiceResult) => {
                if (choiceResult.outcome === "accepted") {
                    console.log("Usuario aceptó la instalación.");
                } else {
                    console.log("Usuario rechazó la instalación.");
                }
            });
        } else {
            alert("La instalación no está disponible en este momento.");
        }
    };

    return (
        <div style={{ textAlign: "center", padding: "2rem" }}>
            <h1>Mi App</h1>
            <p>Esta es una app que te ayudará a reconocer billetes de forma inteligente.</p>
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
        </div>
    );
};

export default InstallationPage;
