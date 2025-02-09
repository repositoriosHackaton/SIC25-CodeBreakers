// useApiResponseProcessor.js
import { useCallback, useRef } from "react";

const useApiResponseProcessor = (narrate) => {
    const isNarratingRef = useRef(false);

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
                "fifty-back": "cincuenta dólares", //USD
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
                "fifty-back-vef": "cincuenta bolívares", //VEF
                "fifty-front-vef": "cincuenta bolívares",
                "five-back-vef": "cinco bolívares",
                "five-front-vef": "cinco bolívares",
                "ten-back-vef": "diez bolívares",
                "ten-front-vef": "diez bolívares",
                "twenty-back-vef": "veinte bolívares",
                "twenty-front-vef": "veinte bolívares",
                "one_hundred-back-vef": "cien bolívares",
                "one_hundred-front-vef": "cien bolívares",
                "two_hundred-back-vef": "dos cientos bolívares",
                "two_hundred-front-vef": "dos cientos bolívares",
            };

            const validDetections = apiResponse.detections.filter(
                (detection) => detection.confidence >= 0.45 && labelMap[detection.label]
            );

            if (validDetections.length > 0) {
                const narration = labelMap[validDetections[0].label];
                narrateWithUnlock(narration); // Forzar la narración
            } else {
                narrateWithUnlock("No se ha detectado el valor del billete correctamente.");
            }
        },
        [narrate]
    );

    return { processResponse };
};

export default useApiResponseProcessor;
