import React from "react";
import "./ActionButtons.css";
import cameraButtonIcon from "/src/assets/camera_button.svg";
import sumButtonIcon from "/src/assets/mas.svg";
import pauseButtonIcon from "/src/assets/pausa.svg";

const ActionButtons = ({ onCameraButton, onToggleSum, isSumActive }) => {
    return (
        <div className="action-buttons-container">
            <button className="action-button green-button" onClick={onToggleSum}>
            <img src={isSumActive ? pauseButtonIcon : sumButtonIcon} alt={isSumActive ? "Pausar suma" : "Iniciar suma"} />
            </button>
            <button className="action-button camera-button" onClick={onCameraButton}>
                <img src={cameraButtonIcon} alt="Tomar foto" />
            </button>
        </div>
    );
};

export default ActionButtons;
