import React, { useEffect } from "react";
import { useSpeechRecognition } from "../hooks/useSpeechRecognition";

const VoiceInterface = ({ callTakePhoto, additionalCommands = [] }) => {
    // Comando básico para "Tomar foto"
    const defaultCommands = [
        {
            keyword: "tomar foto", // Palabra clave para el comando
            callback: () => {
                callTakePhoto();
            },
        },
    ];

    // Combinar comandos básicos con adicionales
    const commands = [...defaultCommands, ...additionalCommands];

    // Hook para escuchar comandos de voz
    useSpeechRecognition((command) => {
        console.log("Comando detectado:", command);

        // Buscar el comando detectado en la lista de comandos
        const action = commands.find((c) => command.includes(c.keyword));
        if (action) {
            action.callback(); // Ejecutar la función asociada al comando
        }
    });

    return null; // Este componente no tiene UI visible
};

export default VoiceInterface;
