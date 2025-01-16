import React, { useEffect, useRef } from "react";
import { useSpeechSynthesis } from "../hooks/useSpeechSynthesis";

const Narrator = ({ text }) => {
    const { speak } = useSpeechSynthesis();
    const lastTextRef = useRef(""); // Almacena el último texto narrado

    useEffect(() => {
        if (text && text !== lastTextRef.current) {
            speak(text);
            lastTextRef.current = text; // Actualiza el texto narrado
            console.log("Narración:", text);
        }
    }, [text, speak]);

    return null; // Este componente no tiene UI
};

export default Narrator;
