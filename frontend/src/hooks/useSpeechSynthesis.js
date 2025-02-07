export const useSpeechSynthesis = () => {
    const speak = (text) => {
        if (!window.speechSynthesis) {
            console.error("Speech Synthesis API no está soportada en este navegador.");
            return;
        }

        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = "es-ES";
        utterance.rate = 1; // Velocidad normal
        utterance.pitch = 1; // Tono normal

        //window.speechSynthesis.speak(utterance);
    };

    return { speak };
};
