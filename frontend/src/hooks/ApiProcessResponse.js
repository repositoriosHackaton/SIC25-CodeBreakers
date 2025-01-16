import { useCallback } from "react";

const useApiResponseProcessor = (narrate) => {
    const processResponse = useCallback(
        (apiResponse) => {
            if (!apiResponse) {
                narrate("No se pudo procesar la respuesta de la API.");
                return;
            }

            // Manejo del caso cuando la API devuelve un mensaje indicando "No objects detected"
            if (apiResponse.message === "No objects detected") {
                narrate("No se ha detectado ningún billete.");
                return;
            }

            if (!apiResponse.detections) {
                narrate("No se pudo procesar la respuesta de la API.");
                return;
            }

            for (const detection of apiResponse.detections) {
                const { confidence, label } = detection;

                if (confidence < 0.3) {
                    narrate("No se ha detectado el valor del billete correctamente.");
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
                    narrate(narration);
                    return;
                }
            }

            narrate("No se encontró un billete válido en la imagen.");
        },
        [narrate]
    );

    return { processResponse };
};

export default useApiResponseProcessor;
