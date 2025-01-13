import React, { useState } from "react";
import "./Header.css";

const Header = () => {
    const [isActive, setIsActive] = useState(false);

    const handleClick = () => {
        setIsActive(true); // Añade la clase "active"
        console.log("Botón de información clickeado");

        // Remueve la clase "active" después de ejecutar la función
        setTimeout(() => {
            setIsActive(false);
        }, 200); // Ajusta el tiempo según sea necesario
    };

    return (
        <button className={`header-button ${isActive ? "active" : ""}`} onClick={handleClick}>
            <div className="logo-container">
                <img src="/favicon.svg" alt="Logo de la App" className="logo" />
                <h1 className="app-name">Cash Reader</h1>
            </div>
        </button>
    );
};

export default Header;
