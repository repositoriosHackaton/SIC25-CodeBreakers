import React, { useState, useEffect } from "react";
import { HELP_COMMANDS, HELP_INTERFACE } from "../constants/HELP_MESSAGE"; // Importar los nuevos mensajes
import useNarrator from "../hooks/useNarrator";
import "./Header.css";

const Header = () => {
    const [narration, setNarration] = useState("");
    const [isFirstVisit, setIsFirstVisit] = useState(true);

    // Verificar si es la primera visita al montar el componente
    seEffect(() => {
        const hasVisited = localStorage.getItem("hasVisited");
        if (!hasVisited) {
            // Mostrar la ayuda de la interfaz + instrucción adicional al inicio
            setNarration(`${HELP_INTERFACE} Si quieres conocer los comandos de voz, toca el centro de la pantalla y di 'Ayuda comandos'.`);
            localStorage.setItem("hasVisited", "true");
        }
        setIsFirstVisit(!hasVisited);
    }, []);

    // Hook del narrador
    const handleNarrationComplete = () => setNarration("");
    useNarrator(narration, handleNarrationComplete);

    // Handler del botón de ayuda
    const handleClick = () => {
        // Mostrar la ayuda de la interfaz + instrucción adicional al hacer clic
        setNarration(`${HELP_INTERFACE} Si quieres conocer los comandos de voz, toca el centro de la pantalla y di 'Ayuda comandos'.`);
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