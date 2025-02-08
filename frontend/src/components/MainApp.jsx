import React, { useRef } from "react";
import Header from "./Header";
import Camera from "./Camera";
import VoiceInterface from "./VoiceInterface";
import "./MainApp.css";

const MainApp = () => {
    const cameraRef = useRef(null); // Referencia para acceder a la cámara

    return (
        <div className="container">
            <header className="header">
                <Header />
            </header>

            {/* Montar la cámara con referencia */}
            <Camera ref={cameraRef} />

            {/* Montar la interfaz de voz (escucha comandos siempre) */}
            <VoiceInterface cameraRef={cameraRef} />
        </div>
    );
};

export default MainApp;
