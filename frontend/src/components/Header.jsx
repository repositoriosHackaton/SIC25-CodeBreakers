import React, { useState, useEffect } from "react";
import { HELP_MESSAGE } from "../constants/HELP_MESSAGE";
import useNarrator from "../hooks/useNarrator";
import "./Header.css";

const Header = () => {
    const [narration, setNarration] = useState("");
    const [isFirstVisit, setIsFirstVisit] = useState(true); // Nuevo estado

    // Verificar si es la primera visita al montar el componente
    useEffect(() => {
        const hasVisited = localStorage.getItem("hasVisited");
        if (!hasVisited) {
            setNarration(HELP_MESSAGE);
            localStorage.setItem("hasVisited", "true");
        }
        setIsFirstVisit(!hasVisited);
    }, []);

    // Hook del narrador (existente)
    const handleNarrationComplete = () => setNarration("");
    useNarrator(narration, handleNarrationComplete);

    // Handler del botón (existente)
    const handleClick = () => setNarration(HELP_MESSAGE);

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
