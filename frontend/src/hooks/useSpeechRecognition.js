import { useEffect, useRef, useCallback } from "react";

// Tiempos configurables
const INACTIVITY_TIMEOUT = 15000; // 15 segundos de inactividad
const COMMAND_DEBOUNCE = 500; // Tiempo mínimo entre comandos procesados

export const useSpeechRecognition = (onCommand) => {
    const recognitionRef = useRef(null);
    const inactivityTimerRef = useRef(null);
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
        recognition.continuous = false; // No es necesario mantenerlo activo continuamente

        recognition.onresult = (event) => {
            try {
                const command = event.results[0][0].transcript.toLowerCase();
                console.log("Comando detectado:", command);
                commandQueue.current.push(command);
                processQueue();
                resetInactivityTimer(); // Reiniciar el temporizador de inactividad
            } catch (error) {
                console.error("Error procesando resultado:", error);
            }
        };

        recognition.onerror = (event) => {
            console.error("Error:", event.error);
            stopRecognition(); // Detener el reconocimiento en caso de error
        };

        recognition.onend = () => {
            console.log("Reconocimiento finalizado");
            // No reiniciamos automáticamente para que el control sea manual
        };

        return recognition;
    }, [processQueue]);

    // Función para reiniciar el temporizador de inactividad
    const resetInactivityTimer = useCallback(() => {
        if (inactivityTimerRef.current) {
            clearTimeout(inactivityTimerRef.current);
        }
        inactivityTimerRef.current = setTimeout(() => {
            stopRecognition(); // Detener el reconocimiento después de 15 segundos de inactividad
        }, INACTIVITY_TIMEOUT);
    }, []);

    // Función para detener el reconocimiento
    const stopRecognition = useCallback(() => {
        if (recognitionRef.current) {
            recognitionRef.current.stop();
        }
        if (inactivityTimerRef.current) {
            clearTimeout(inactivityTimerRef.current);
        }
    }, []);

    // Función para iniciar el reconocimiento
    const startRecognition = useCallback(() => {
        if (recognitionRef.current) {
            try {
                recognitionRef.current.start();
                resetInactivityTimer(); // Reiniciar el temporizador de inactividad
            } catch (error) {
                console.error("Error iniciando reconocimiento:", error);
            }
        }
    }, [resetInactivityTimer]);

    useEffect(() => {
        const recognition = setupRecognition();
        if (!recognition) return;
        recognitionRef.current = recognition;
        return () => {
            stopRecognition(); // Limpiar al desmontar el componente
        };
    }, [setupRecognition, stopRecognition]);

    return { start: startRecognition, stop: stopRecognition };
};