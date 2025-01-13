// ActionButtons.jsx
import React from "react";
import "./ActionButtons.css";

const ActionButtons = ({ onRedClick }) => {
    const handleGreenClick = () => {
        console.log("Botón verde presionado");
    };

    return (
        <div className="action-buttons-container">
            <button className="action-button green-button" onClick={handleGreenClick}>
                <img src="/src/assets/change_button.svg" alt="Vuelto" />
            </button>
            <button className="action-button camera-button" onClick={onRedClick}>
                <img src="/src/assets/camera_button.svg" alt="Tomar foto" />
            </button>
        </div>
    );
};

export default ActionButtons;
