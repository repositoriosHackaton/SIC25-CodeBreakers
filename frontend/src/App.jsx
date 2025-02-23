import React, { useState, useEffect } from "react";
import InstallationPage from "./components/InstallationPage";
import PageApp from "./components/PageApp";
import MainApp from "./components/MainApp";
import "./App.css";

const App = () => {
    const [isStandalone, setIsStandalone] = useState(false);
    const [updateAvailable, setUpdateAvailable] = useState(false);

    useEffect(() => {
        // Registra el Service Worker y escucha actualizaciones
        if ("serviceWorker" in navigator) {
            navigator.serviceWorker.register("/sw.js").then((registration) => {
                registration.addEventListener("updatefound", () => {
                    const newWorker = registration.installing;
                    newWorker.addEventListener("statechange", () => {
                        if (newWorker.state === "activated") {
                            setUpdateAvailable(true); // Notifica al usuario
                        }
                    });
                });
            });
        }

        // Verificar modo standalone
        const checkStandalone = () => {
            const standalone = window.matchMedia("(display-mode: standalone)").matches || window.navigator.standalone;
            setIsStandalone(standalone);
        };
        checkStandalone();
        window.addEventListener("resize", checkStandalone);
        return () => window.removeEventListener("resize", checkStandalone);
    }, []);

    // Recargar cuando haya una actualización
    useEffect(() => {
        if (updateAvailable) {
            if (confirm("¡Nueva versión disponible! ¿Recargar ahora?")) {
                window.location.reload();
            }
        }
    }, [updateAvailable]);

    return isStandalone ? <MainApp /> : <PageApp />;
};

export default App;
