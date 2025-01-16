import React, { useEffect } from "react";
import Narrator from "./Narrator"; // Importa tu componente Narrador

const TextProcessor = ({ apiResponse }) => {
    // Función para procesar la respuesta y obtener el texto
    const getNarrationText = () => {
        if (!apiResponse || !apiResponse.detencions || apiResponse.detencions.length === 0) {
            return "No se ha detectado el valor del billete correctamente";
        }

        // Procesamos el primer objeto de detección
        const { confidence, label } = apiResponse.detencions[0];

        if (confidence < 0.3) {
            return "No se ha detectado el valor del billete correctamente";
        }

        // Mapeo de etiquetas a mensajes
        const labelToTextMap = {
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

        return labelToTextMap[label] || "Etiqueta no reconocida";
    };

    const narrationText = getNarrationText();

    // Renderiza el componente Narrador con el texto procesado
    return <Narrator text={narrationText} />;
};

export default TextProcessor;
