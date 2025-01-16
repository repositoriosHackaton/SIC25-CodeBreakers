import { useCallback, useRef } from "react";

const useApiResponseProcessor = (narrate) => {
    const isNarratingRef = useRef(false); // Estado para bloquear múltiples llamadas

    const processResponse = useCallback(
        (apiResponse) => {
            if (isNarratingRef.current) return; // Evitar narrar si ya está activo
            isNarratingRef.current = true;

            const narrateWithUnlock = (message) => {
                narrate(message);
                setTimeout(() => {
                    isNarratingRef.current = false; // Desbloquear después de narrar
                }, 1000); // Ajusta este tiempo según la duración del mensaje
            };

            if (!apiResponse || apiResponse.message === "No objects detected") {
                narrateWithUnlock("No se ha detectado ningún billete.");
                return;
            }

            if (!apiResponse.detections || apiResponse.detections.length === 0) {
                narrateWithUnlock("No se encontró un billete válido en la imagen.");
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

            const validDetections = apiResponse.detections.filter(
                (detection) => detection.confidence >= 0.45 && labelMap[detection.label]
            );

            if (validDetections.length > 0) {
                const narration = labelMap[validDetections[0].label]; // Narrar el primer billete válido
                narrateWithUnlock(narration);
            } else {
                narrateWithUnlock("No se ha detectado el valor del billete correctamente.");
            }
        },
        [narrate]
    );

    return { processResponse };
};

export default useApiResponseProcessor;
