import React, { useState, useEffect } from "react";
import useNarrator from "../hooks/useNarrator";
import "./Header.css";

const Header = () => {
    const [narration, setNarration] = useState("");

    // Función para limpiar la narración después de hablar
    const handleNarrationComplete = () => {
        setNarration("");
    };

    // Hook del narrador
    useNarrator(narration, handleNarrationComplete);

    const handleClick = () => {
        // Iniciar narración
        setNarration(
            "Ayuda para los comandos de voz. Puede pronunciar Tomar Foto para evaluar el valor de un billete."
        );
    };

    return (
        <button className={`header-button`} onClick={handleClick}>
            <div className="logo-container">
                <img src="/favicon.svg" alt="Logo de la App" className="logo" />
                <h1 className="app-name">Cash Reader</h1>
            </div>
        </button>
    );
};

export default Header;
