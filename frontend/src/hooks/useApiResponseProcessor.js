import { useCallback, useRef } from "react";

const responseMapping = {
    "fifty-back": { visual: "50$", narrator: "cincuenta dólares" },
    "fifty-front": { visual: "50$", narrator: "cincuenta dólares" },
    "five-back": { visual: "5$", narrator: "cinco dólares" },
    "five-front": { visual: "5$", narrator: "cinco dólares" },
    "one-back": { visual: "1$", narrator: "un dólar" },
    "one-front": { visual: "1$", narrator: "un dólar" },
    "ten-back": { visual: "10$", narrator: "diez dólares" },
    "ten-front": { visual: "10$", narrator: "diez dólares" },
    "twenty-back": { visual: "20$", narrator: "veinte dólares" },
    "twenty-front": { visual: "20$", narrator: "veinte dólares" },
    "one_hundred-back": { visual: "100$", narrator: "cien dólares" },
    "one_hundred-front": { visual: "100$", narrator: "cien dólares" },
    "fifty-back-vef": { visual: "Bs. 50", narrator: "cincuenta bolívares" },
    "fifty-front-vef": { visual: "Bs. 50", narrator: "cincuenta bolívares" },
    "five-back-vef": { visual: "Bs. 5", narrator: "cinco bolívares" },
    "five-front-vef": { visual: "Bs. 5", narrator: "cinco bolívares" },
    "ten-back-vef": { visual: "Bs. 10", narrator: "diez bolívares" },
    "ten-front-vef": { visual: "Bs. 10", narrator: "diez bolívares" },
    "twenty-back-vef": { visual: "Bs. 20", narrator: "veinte bolívares" },
    "twenty-front-vef": { visual: "Bs. 20", narrator: "veinte bolívares" },
    "one_hundred-back-vef": { visual: "Bs. 100", narrator: "cien bolívares" },
    "one_hundred-front-vef": { visual: "Bs. 100", narrator: "cien bolívares" },
    "two_hundred-back-vef": { visual: "Bs. 200", narrator: "dos cientos bolívares" },
    "two_hundred-front-vef": { visual: "Bs. 200", narrator: "dos cientos bolívares" },
    "Repetir Foto": { visual: "Repetir Foto", narrator: "No se ha detectado el valor del billete correctamente." },
    "": { visual: "", narrator: "No se ha detectado ningún billete." },
};

const useApiResponseProcessor = (narrate, setVisualRef) => {
    const isNarratingRef = useRef(false);

    const processResponse = useCallback(
        (apiResponse) => {
            if (isNarratingRef.current) return; // Evitar narrar si ya está activo
            isNarratingRef.current = true;

            const narrateWithUnlock = (message, visualMessage) => {
                narrate(message);
                if (setVisualRef) {
                    setVisualRef(visualMessage);
                }
                setTimeout(() => {
                    isNarratingRef.current = false;
                }, 1000); // Ajusta según la duración del mensaje
            };

            if (!apiResponse || apiResponse.message === "No objects detected") {
                narrateWithUnlock("No se ha detectado ningún billete.", "");
                return;
            }

            if (!apiResponse.detections || apiResponse.detections.length === 0) {
                narrateWithUnlock("No se encontró un billete válido en la imagen.", "Repetir Foto");
                return;
            }

            const validDetections = apiResponse.detections.filter(
                (detection) => detection.confidence >= 0.7 && responseMapping[detection.label]
            );

            if (validDetections.length > 0) {
                const label = validDetections[0].label;
                const mapping = responseMapping[label];
                narrateWithUnlock(mapping.narrator, mapping.visual);
            } else {
                narrateWithUnlock("No se ha detectado el valor del billete correctamente.", "Repetir Foto");
            }
        },
        [narrate, setVisualRef]
    );

    return { processResponse };
};

export default useApiResponseProcessor;
