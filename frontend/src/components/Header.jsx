import React, { useState, useEffect } from "react";
import useNarrator from "../hooks/useNarrator";
import "./Header.css";

// Mensaje de ayuda inicial
const HELP_MESSAGE = `
    Instrucciones de uso de la aplicación: 
    
    En la parte inferior de la pantalla: 
    - Botón izquierdo: Seleccionar tipo de billete a escanear.
    - Botón derecho: Tomar foto para evaluación.
    
    En la parte superior: 
    - Botón de ayuda: Escuchar estas instrucciones nuevamente.

    Comandos de voz alternativos (mantenga presionado el centro de la pantalla):
    - "Tomar Foto": Iniciar evaluación del billete.
    - "Cambiar Moneda": Alternar entre bolívares y dólares.
    - "Ayuda": Repetir instrucciones.
`;

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
