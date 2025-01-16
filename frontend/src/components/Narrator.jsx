import React, { useEffect } from 'react';
import { useSpeechSynthesis } from '../hooks/useSpeechSynthesis';

const Narrator = ({ text }) => {
  const { speak } = useSpeechSynthesis();

  useEffect(() => {
    if (text) {
      speak(text); // Narra el texto recibido como prop
    }
  }, [text, speak]); // Solo se ejecuta cuando cambia el texto

  return null; // Este componente no tiene UI
};

export default Narrator;
