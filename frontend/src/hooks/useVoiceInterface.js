import { useMemo, useCallback, useState } from "react";
import { useSpeechRecognition } from "./useSpeechRecognition";
import { HELP_INTERFACE, HELP_COMMANDS } from "../constants/HELP_MESSAGE"; 

/**
 * Hook para manejar comandos de voz.
 * @param {Object} config - Configuración de la interfaz de voz.
 * @param {Function} config.callTakePhoto - Función para capturar foto.
 * @param {Function} config.callToggleModel - Función para cambiar modelo.
 * @param {Array} [config.additionalCommands=[]] - Comandos adicionales.
 * @param {boolean} [config.debug=false] - Modo debug.
 * @returns {Object} { error, isListening, start, stop, commands }
 */
export const useVoiceInterface = ({
    callTakePhoto,
    callToggleModel,
    callHelpInterface, // Nueva función
    callHelpCommands, // Nueva función
    callStartSum,
    callStopSum,
    callLastSum,
    callCurrentSum,
    additionalCommands = [],
    debug = false,
}) => {
    const mergedCommands = useMemo(() => {
        const defaults = [
            {
                keyword: "tomar foto",
                callback: callTakePhoto,
                description: "Captura una foto usando la cámara",
            },
            {
                keyword: "cambiar moneda",
                callback: callToggleModel,
                description: "Cambia el modelo de IA usado",
            },
            {
                keyword: "ayuda interfaz", // Nuevo comando
                callback: callHelpInterface, // Función que explica la interfaz gráfica
                description: "Explica qué hay en la interfaz gráfica",
            },
            {
                keyword: "ayuda comandos", // Nuevo comando
                callback: callHelpCommands, // Función que explica los comandos de voz
                description: "Explica todos los comandos de voz disponibles",
            },
            {
                keyword: "contar",
                callback: callStartSum,
                description: "Activa o desactiva la suma",
            },
            {
                keyword: "detener conteo",
                callback: callStopSum,
                description: "Detiene la suma y narra el total acumulado",
            },
            {
                keyword: "suma anterior", // Nuevo comando
                callback: callLastSum, // Función que se ejecutará
                description: "Repite la última suma almacenada",
            },
            {
                keyword: "Total actual", // Nuevo comando
                callback: callCurrentSum, // Función que se ejecutará
                description: "Muestra la suma actual acumulada",
            },

        ];
        return [...defaults, ...additionalCommands];
    }, [additionalCommands, callTakePhoto, callToggleModel, callHelpInterface, callHelpCommands, callStartSum, callStopSum, callLastSum, callCurrentSum]);

    const [error, setError] = useState(null);

    // Handler para procesar el comando reconocido
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

    // Uso del hook de reconocimiento, el cual no se inicia automáticamente
    const { start, stop } = useSpeechRecognition(handleVoiceCommand);

    return { error, start, stop, commands: mergedCommands };
};
