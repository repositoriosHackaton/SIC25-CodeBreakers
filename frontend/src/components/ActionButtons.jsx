import React from "react";
import "./ActionButtons.css";

const ActionButtons = () => {
    const handleGreenClick = () => {
        console.log("Botón verde presionado");
    };

    const handleRedClick = () => {
        console.log("Botón rojo presionado");
    };

    return (
        <div className="action-buttons-container">
            <button className="action-button green-button" onClick={handleGreenClick}>
                <img src="/src/assets/change_button.svg" alt="Vuelto" />
            </button>
            <button className="action-button red-button" onClick={handleRedClick}>
                <img src="/src/assets/info_button.svg" alt="Comandos" />
            </button>
        </div>
    );
};

export default ActionButtons;
