import { useEffect } from 'react';

export const useSpeechRecognition = (onCommand) => {
  useEffect(() => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
      console.error('Speech Recognition API no está soportada en este navegador.');
      return;
    }

    const recognition = new SpeechRecognition();
    recognition.lang = 'es-ES'; // Configura el idioma
    recognition.interimResults = false;
    recognition.continuous = true; // Escucha continuamente

    recognition.onresult = (event) => {
      const command = event.results[0][0].transcript.toLowerCase();
      console.log('Comando reconocido:', command);
      onCommand(command); // Llama a la función pasada como parámetro
    };

    recognition.onerror = (event) => {
      console.error('Error en el reconocimiento:', event.error);
    };

    recognition.onend = () => {
      recognition.start(); // Reinicia el reconocimiento automáticamente
    };

    recognition.start(); // Inicia el reconocimiento al montar el hook

    return () => recognition.abort(); // Limpia el reconocimiento al desmontar
  }, [onCommand]);
};