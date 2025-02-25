// useVoiceInterface.js
import { useMemo, useCallback, useState } from "react";
import { useSpeechRecognition } from "./useSpeechRecognition";

export const useVoiceInterface = ({
    callTakePhoto = null,
    callToggleModel = null,
    callHelpMessage = null,
    additionalCommands = [],
    debug = false,
} = {}) => {
    // Generar comandos base condicionalmente
    const baseCommands = useMemo(() => {
        const commands = [];

        if (callTakePhoto) {
            commands.push({
                keyword: "tomar foto",
                callback: callTakePhoto,
                description: "Captura una foto usando la cámara",
            });
        }

        if (callToggleModel) {
            commands.push({
                keyword: "cambiar moneda",
                callback: callToggleModel,
                description: "Cambia el modelo de divisa",
            });
        }

        if (callHelpMessage) {
            commands.push({
                keyword: "ayuda",
                callback: callHelpMessage,
                description: "Muestra las instrucciones de uso",
            });
        }

        return commands;
    }, [callTakePhoto, callToggleModel, callHelpMessage]);

    const mergedCommands = useMemo(() => {
        return [...baseCommands, ...additionalCommands];
    }, [baseCommands, additionalCommands]);

    // Resto del hook permanece igual
    const [error, setError] = useState(null);

    const handleVoiceCommand = useCallback(
        (command) => {
            if (debug) console.debug("[Voice] Comando detectado:", command);
            try {
                const matchedCommand = mergedCommands.find((c) =>
                    command.toLowerCase().includes(c.keyword.toLowerCase())
                );
                if (matchedCommand) {
                    if (debug) console.info(`[Voice] Ejecutando comando: ${matchedCommand.keyword}`);
                    matchedCommand.callback();
                }
            } catch (e) {
                setError(`Error procesando comando: ${e.message}`);
                console.error("[Voice Error]", e);
            }
        },
        [mergedCommands, debug]
    );

    const { start, stop } = useSpeechRecognition(handleVoiceCommand);

    return { error, start, stop, commands: mergedCommands };
};
