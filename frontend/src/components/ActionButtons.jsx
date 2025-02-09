import React from "react";
import "./ActionButtons.css";
import cameraButtonIcon from "/src/assets/camera_button.svg";
import changeButtonIcon from "/src/assets/change_button.svg";

const ActionButtons = ({ onCameraButton }) => {
    const handleGreenClick = () => {
        console.log("Botón verde presionado");
    };

    return (
        <div className="action-buttons-container">
            <button className="action-button green-button" onClick={handleGreenClick}>
                <img src={changeButtonIcon} alt="Vuelto" />
            </button>
            <button className="action-button camera-button" onClick={onCameraButton}>
                <img src={cameraButtonIcon} alt="Tomar foto" />
            </button>
        </div>
    );
};

export default ActionButtons;
