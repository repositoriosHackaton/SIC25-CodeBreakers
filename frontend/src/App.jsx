import React, { useState, useEffect } from "react";
import InstallationPage from "./components/InstallationPage";
import PageApp from "./components/PageApp";
import MainApp from "./components/MainApp";
import "./App.css";

const App = () => {
    const [isStandalone, setIsStandalone] = useState(false);
    const [updateAvailable, setUpdateAvailable] = useState(false);

    const setVhProperty = () => {
        const vh = window.innerHeight * 0.01;
        document.documentElement.style.setProperty("--vh", `${vh}px`);
    };

    // Establecer al cargar la app
    setVhProperty();

    // Actualizar la variable al cambiar el tamaño de la ventana
    window.addEventListener("resize", setVhProperty);

    useEffect(() => {
        // Registrar el Service Worker y escucha actualizaciones
        if ("serviceWorker" in navigator) {
            navigator.serviceWorker.register("/sw.js").then((registration) => {
                registration.addEventListener("updatefound", () => {
                    const newWorker = registration.installing;
                    newWorker.addEventListener("statechange", () => {
                        if (newWorker.state === "activated") {
                            setUpdateAvailable(true); // Notificar al usuario
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
            window.location.reload();
        }
    }, [updateAvailable]);

    return isStandalone ? <MainApp /> : <PageApp />;
};

export default App;
