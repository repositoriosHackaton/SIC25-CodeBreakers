import React, { useState, useEffect } from "react";
import { HELP_COMMANDS, HELP_INTERFACE } from "../constants/HELP_MESSAGE"; // Importar los nuevos mensajes
import useNarrator from "../hooks/useNarrator";
import "./Header.css";

const Header = () => {
    const [narration, setNarration] = useState("");
    const [isFirstVisit, setIsFirstVisit] = useState(true);

    // Verificar si es la primera visita al montar el componente
    useEffect(() => {
        const hasVisited = localStorage.getItem("hasVisited");
        if (!hasVisited) {
            // Mostrar ambos mensajes al inicio (interfaz + comandos)
            setNarration(`${HELP_INTERFACE} ${HELP_COMMANDS}`);
            localStorage.setItem("hasVisited", "true");
        }
        setIsFirstVisit(!hasVisited);
    }, []);

    // Hook del narrador
    const handleNarrationComplete = () => setNarration("");
    useNarrator(narration, handleNarrationComplete);

    // Handler del botón de ayuda
    const handleClick = () => {
        // Mostrar solo la ayuda de la interfaz al hacer clic
        setNarration(HELP_INTERFACE);
    };

    return (
        <button className={`header-button`} onClick={handleClick}>
            <div className="logo-container">
                <img src="/favicon.svg" alt="Logo de la App" className="logo" />
                <h1 className="app-name">Cash Reader</h1>

                {/* Indicador visual para primera visita */}
                {isFirstVisit && <div className="pulsing-dot" />}
            </div>
        </button>
    );
};

export default Header;