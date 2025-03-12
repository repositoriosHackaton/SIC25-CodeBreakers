export const useSpeechSynthesis = () => {
    const speak = (text, options = {}) => {
        if (!window.speechSynthesis) {
            console.error("Speech Synthesis API no está soportada en este navegador.");
            return;
        }

        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = options.lang || "es-ES";
        utterance.rate = options.rate || 1; // Velocidad normal
        utterance.pitch = options.pitch || 1; // Tono normal

        if (options.onend) {
            utterance.onend = options.onend;
        }

        window.speechSynthesis.speak(utterance);
    };

    return { speak };
};
