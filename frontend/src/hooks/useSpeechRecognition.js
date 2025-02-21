// useSpeechRecognition.js
import { useEffect, useRef, useCallback } from "react";

// Tiempos configurables
const RETRY_DELAY = 1000; // 1 segundo entre reintentos
const MAX_RETRIES = 3; // Máximo de reintentos tras errores
const COMMAND_DEBOUNCE = 500; // Tiempo mínimo entre comandos procesados

export const useSpeechRecognition = (onCommand) => {
    const recognitionRef = useRef(null);
    const retryCount = useRef(0);
    const lastCommandTime = useRef(0);
    const commandQueue = useRef([]);
    const isProcessing = useRef(false);

    // Función para manejar cada comando, con debounce
    const handleCommand = useCallback(
        (command) => {
            const now = Date.now();
            if (now - lastCommandTime.current > COMMAND_DEBOUNCE) {
                lastCommandTime.current = now;
                onCommand(command);
            }
        },
        [onCommand]
    );

    // Procesamiento en cola para evitar sobrecarga
    const processQueue = useCallback(() => {
        if (!isProcessing.current && commandQueue.current.length > 0) {
            isProcessing.current = true;
            const command = commandQueue.current.shift();
            handleCommand(command);
            setTimeout(() => {
                isProcessing.current = false;
                processQueue();
            }, COMMAND_DEBOUNCE);
        }
    }, [handleCommand]);

    // Configuración inicial del reconocimiento
    const setupRecognition = useCallback(() => {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        if (!SpeechRecognition) {
            console.error("API no soportada");
            return null;
        }
        const recognition = new SpeechRecognition();
        recognition.lang = "es-ES";
        recognition.interimResults = false;
        // Usamos continuous=false para que se active solo durante la pulsación
        recognition.continuous = false;

        recognition.onresult = (event) => {
            try {
                const command = event.results[0][0].transcript.toLowerCase();
                console.log("Comando detectado:", command);
                commandQueue.current.push(command);
                processQueue();
            } catch (error) {
                console.error("Error procesando resultado:", error);
            }
        };

        recognition.onerror = (event) => {
            console.error("Error:", event.error);
            if (retryCount.current < MAX_RETRIES) {
                retryCount.current += 1;
                setTimeout(() => recognition.start(), RETRY_DELAY);
            }
        };

        recognition.onend = () => {
            console.log("Reconocimiento finalizado");
            // No reiniciamos automáticamente para que el control sea manual
        };

        return recognition;
    }, [processQueue]);

    useEffect(() => {
        const recognition = setupRecognition();
        if (!recognition) return;
        recognitionRef.current = recognition;
        // Eliminamos el start automático para que se invoque solo mediante la función expuesta.
        return () => {
            if (recognitionRef.current) {
                recognitionRef.current.abort();
                recognitionRef.current = null;
            }
        };
    }, [setupRecognition]);

    // Función para iniciar la escucha manualmente
    const start = useCallback(() => {
        if (recognitionRef.current) {
            try {
                recognitionRef.current.start();
            } catch (error) {
                console.error("Error iniciando reconocimiento:", error);
            }
        }
    }, []);

    // Función para detener la escucha manualmente
    const stop = useCallback(() => {
        if (recognitionRef.current) {
            recognitionRef.current.stop();
        }
    }, []);

    return { start, stop };
};
