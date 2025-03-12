import React from "react";
import "./ActionButtons.css";
import cameraButtonIcon from "/src/assets/camera_button.svg";
import sumButtonIcon from "/src/assets/mas.svg";
import pauseButtonIcon from "/src/assets/pausa.svg";

const ActionButtons = ({ onCameraButton, isCameraDisabled, onToggleSum, isSumActive }) => {
    return (
        <div className="action-buttons">
            <button
                onClick={onCameraButton}
                disabled={isCameraDisabled} // Deshabilitar el botón si isCameraDisabled es true
            >
                {isCameraDisabled ? "Procesando..." : "Tomar Foto"}
            </button>
            <button onClick={onToggleSum}>
                {isSumActive ? "Detener Conteo" : "Iniciar Conteo"}
            </button>
        </div>
    );
};

export default ActionButtons;
