import { useCallback } from "react";

const useApiResponseProcessor = (narrate) => {
    const processResponse = useCallback(
        (apiResponse) => {
            let narrationCalled = false; // Bandera para evitar múltiples narraciones

            const safeNarrate = (message) => {
                if (!narrationCalled) {
                    narrate(message);
                    narrationCalled = true; // Marcar que ya se narró
                }
            };

            // Manejo del caso cuando la API devuelve un mensaje indicando "No objects detected"
            if (apiResponse.message === "No objects detected") {
                safeNarrate("No se ha detectado ningún billete.");
                return;
            }

            if (!apiResponse || !apiResponse.detections) {
                safeNarrate("No se pudo procesar la respuesta de la API.");
                return;
            }

            for (const detection of apiResponse.detections) {
                const { confidence, label } = detection;

                if (confidence < 0.45) {
                    safeNarrate("No se ha detectado el valor del billete correctamente.");
                    return;
                }

                const labelMap = {
                    "fifty-back": "cincuenta dólares",
                    "fifty-front": "cincuenta dólares",
                    "five-back": "cinco dólares",
                    "five-front": "cinco dólares",
                    "one-back": "un dólar",
                    "one-front": "un dólar",
                    "ten-back": "diez dólares",
                    "ten-front": "diez dólares",
                    "twenty-back": "veinte dólares",
                    "twenty-front": "veinte dólares",
                    "one_hundred-back": "cien dólares",
                    "one_hundred-front": "cien dólares",
                };

                const narration = labelMap[label];
                if (narration) {
                    safeNarrate(narration);
                    return;
                }
            }

            safeNarrate("No se encontró un billete válido en la imagen.");
        },
        [narrate]
    );

    return { processResponse };
};

export default useApiResponseProcessor;
