import { useEffect, useRef } from "react";
import { useSpeechSynthesis } from "./useSpeechSynthesis";

const useNarrator = (text) => {
    const { speak } = useSpeechSynthesis();
    const lastTextRef = useRef(""); // Almacena el último texto narrado

    useEffect(() => {
        if (text && text !== lastTextRef.current) {
            speak(text);
            lastTextRef.current = text; // Actualiza el texto narrado
            console.log("Narración:", text);
        }
    }, [text, speak]);
};

export default useNarrator;
