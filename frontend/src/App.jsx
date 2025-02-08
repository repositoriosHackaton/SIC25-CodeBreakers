import React, { useState, useEffect } from "react";
import InstallationPage from "./components/InstallationPage";
import MainApp from "./components/MainApp";
import Camera from './components/Camera';
import VoiceInterface from './components/VoiceInterface';
import "./App.css";

const App = () => {
    const [isStandalone, setIsStandalone] = useState(false);

    const cameraRef = useRef(null); // Referencia a la cámara
    
    useEffect(() => {
        // Verificar si la app está en modo standalone
        const checkStandalone = () => {
            const standalone = window.matchMedia("(display-mode: standalone)").matches || window.navigator.standalone; // Para iOS
            setIsStandalone(standalone);
        };

        checkStandalone();

        // Escuchar cambios en el estado del display-mode (si el navegador soporta)
        window.addEventListener("resize", checkStandalone);

        return () => {
            window.removeEventListener("resize", checkStandalone);
        };
    }, []);

    return isStandalone ? <MainApp /> : <InstallationPage />;

    return (
        <div>
          <h1>Aplicación de Reconocimiento de Billetes</h1>
          
          {/* Cámara */}
          <Camera ref={cameraRef} />
          
          {/* Interfaz de Voz (siempre activa) */}
          <VoiceInterface cameraRef={cameraRef} />
        </div>
      );
    
    
};

export default App;
