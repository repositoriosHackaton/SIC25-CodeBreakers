import { useEffect, useRef, useCallback } from "react";

// Tiempos configurables para mejor mantenimiento
const RETRY_DELAY = 1000; // 1 segundo entre reintentos
const MAX_RETRIES = 3; // Máximo de reintentos tras errores
const COMMAND_DEBOUNCE = 500; // Tiempo mínimo entre comandos procesados

export const useSpeechRecognition = (onCommand) => {
    const recognitionRef = useRef(null);
    const retryCount = useRef(0);
    const lastCommandTime = useRef(0);
    const commandQueue = useRef([]);
    const isProcessing = useRef(false);

    // Usamos useCallback para memoizar el handler y evitar recreaciones
    const handleCommand = useCallback(
        (command) => {
            const now = Date.now();

            // Debounce para evitar comandos demasiado cercanos en el tiempo
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

    // Configuración inicial del reconocimiento de voz
    const setupRecognition = useCallback(() => {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

        if (!SpeechRecognition) {
            console.error("API no soportada");
            return null;
        }

        const recognition = new SpeechRecognition();
        recognition.lang = "es-ES";
        recognition.interimResults = false;
        recognition.continuous = false; // Cambiado a false para mejor control

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
            // Reinicio seguro con delay
            setTimeout(() => {
                if (!recognitionRef.current || recognitionRef.current === recognition) {
                    try {
                        recognition.start();
                    } catch (error) {
                        console.error("Error al reiniciar:", error);
                    }
                }
            }, 500);
        };

        return recognition;
    }, [processQueue]);

    useEffect(() => {
        const recognition = setupRecognition();
        if (!recognition) return;

        recognitionRef.current = recognition;

        try {
            recognition.start();
        } catch (error) {
            console.error("Error inicializando reconocimiento:", error);
        }

        return () => {
            if (recognitionRef.current) {
                recognitionRef.current.abort();
                recognitionRef.current = null;
            }
        };
    }, [setupRecognition]);

    // Actualización en caliente del handler de comandos
    const savedHandler = useRef(onCommand);
    useEffect(() => {
        savedHandler.current = onCommand;
    }, [onCommand]);
};
