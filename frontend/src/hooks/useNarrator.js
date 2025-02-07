// useNarrator.js
import { useEffect, useRef } from "react";
import { useSpeechSynthesis } from "./useSpeechSynthesis";

const useNarrator = (text, onNarrationComplete) => {
    const { speak } = useSpeechSynthesis();
    const lastTextRef = useRef(""); // Almacena el último texto narrado

    useEffect(() => {
        if (text) {
            speak(text);
            lastTextRef.current = text; // Actualiza el texto narrado
            console.log("Narración:", text);

            // Limpiar el valor de `narration` después de la narración
            const handleNarrationEnd = () => {
                if (onNarrationComplete) {
                    onNarrationComplete(); // Llama a la función para limpiar `narration`
                }
            };

            // Escuchar el evento de finalización de la narración
            const utterance = new SpeechSynthesisUtterance(text);
            utterance.onend = handleNarrationEnd;
            window.speechSynthesis.speak(utterance);
        }
    }, [text, speak, onNarrationComplete]);
};

export default useNarrator;
