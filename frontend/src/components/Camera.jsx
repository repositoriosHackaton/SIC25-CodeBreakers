import React, { useRef, useEffect, useState, useCallback } from "react";
import axios from "axios";
import ActionButtons from "./ActionButtons";
import useApiResponseProcessor from "../hooks/useApiResponseProcessor";
import useNarrator from "../hooks/useNarrator";
import { useVoiceInterface } from "../hooks/useVoiceInterface";
import "./Camera.css";

const Camera = () => {
    // Refs para el video, el intervalo automático y el track de video
    const videoRef = useRef(null);
    const autoCaptureRef = useRef(null);
    const videoTrackRef = useRef(null);

    // Estados locales
    const [photo, setPhoto] = useState(null);
    const [autoCaptureInterval, setAutoCaptureInterval] = useState(0);
    const [narration, setNarration] = useState("");

    // Función para limpiar la narración cuando finaliza
    const handleNarrationComplete = () => {
        setNarration("");
    };

    // Hooks personalizados para la narración y el procesamiento de respuesta de la API
    useNarrator(narration, handleNarrationComplete);
    const { processResponse } = useApiResponseProcessor((message) => {
        setNarration(message);
    });

    /**
     * Función unificada para controlar el flash.
     * Recibe un booleano enabled para activar (true) o desactivar (false) el flash.
     */
    const setFlash = async (enabled) => {
        if (videoTrackRef.current) {
            const capabilities = videoTrackRef.current.getCapabilities();
            if (capabilities.torch) {
                try {
                    await videoTrackRef.current.applyConstraints({
                        advanced: [{ torch: enabled }],
                    });
                    console.log(`Flash ${enabled ? "activado" : "desactivado"}.`);
                } catch (error) {
                    console.error(`Error al ${enabled ? "activar" : "desactivar"} el flash:`, error);
                }
            } else {
                console.warn("El dispositivo no soporta el control del flash.");
            }
        }
    };

    // Obtener el stream de la cámara y gestionar el flash según la visibilidad
    useEffect(() => {
        const getCameraStream = async () => {
            try {
                const stream = await navigator.mediaDevices.getUserMedia({
                    video: {
                        facingMode: "environment",
                        width: { ideal: 416 },
                        height: { ideal: 416 },
                    },
                });
                if (videoRef.current) {
                    videoRef.current.srcObject = stream;
                    const [videoTrack] = stream.getVideoTracks();
                    videoTrackRef.current = videoTrack;
                    // Activar el flash inicialmente
                    setFlash(true);
                }
            } catch (error) {
                console.error("Error al acceder a la cámara:", error);
            }
        };

        getCameraStream();

        const handleVisibilityChange = () => {
            if (document.visibilityState === "visible") {
                setFlash(true);
            } else {
                setFlash(false);
            }
        };

        document.addEventListener("visibilitychange", handleVisibilityChange);

        return () => {
            if (videoRef.current && videoRef.current.srcObject) {
                const stream = videoRef.current.srcObject;
                stream.getTracks().forEach((track) => track.stop());
            }
            clearInterval(autoCaptureRef.current);
            document.removeEventListener("visibilitychange", handleVisibilityChange);
        };
    }, []);

    /**
     * Función para enviar la imagen capturada a la API.
     * Se utiliza useCallback para que su referencia sea estable.
     */
    const sendPhotoToAPI = useCallback(
        async (imageData) => {
            try {
                const blob = await (await fetch(imageData)).blob();
                const formData = new FormData();
                formData.append("image", blob, "captura.jpg");

                const response = await axios.post("https://cashreader.share.zrok.io/detection", formData, {
                    headers: { "Content-Type": "multipart/form-data" },
                });

                console.log("Respuesta de la API:", response.data);
                processResponse(response.data);
            } catch (error) {
                console.error("Error al enviar la imagen a la API:", error);
                setNarration("No se ha podido comunicar con el servidor, intentelo mas tarde");
            }
        },
        [processResponse]
    );

    /**
     * Función para tomar la foto en resolución nativa y enviar la imagen.
     * Se utiliza useCallback para estabilizar su referencia y evitar recreaciones innecesarias.
     */
    const takePhoto = useCallback(() => {
        const video = videoRef.current;
        if (!video) {
            console.error("Video no disponible.");
            return;
        }

        const nativeWidth = video.videoWidth;
        const nativeHeight = video.videoHeight;

        // Canvas para capturar la imagen en tamaño nativo
        const canvas = document.createElement("canvas");
        canvas.width = nativeWidth;
        canvas.height = nativeHeight;
        const context = canvas.getContext("2d");
        context.drawImage(video, 0, 0, nativeWidth, nativeHeight);

        // Obtenemos la imagen en la máxima calidad posible.
        // Se puede especificar la calidad (de 0 a 1) en el toDataURL; usamos 1 para máxima calidad.
        const imageUrl = canvas.toDataURL("image/jpeg", 1.0);
        setPhoto(imageUrl);
        console.log("Foto tomada");
        sendPhotoToAPI(imageUrl);
    }, [sendPhotoToAPI]);

    // Manejar el intervalo automático de captura según autoCaptureInterval
    useEffect(() => {
        if (autoCaptureInterval > 0) {
            clearInterval(autoCaptureRef.current);
            autoCaptureRef.current = setInterval(() => {
                takePhoto();
            }, autoCaptureInterval * 1000);
        } else {
            clearInterval(autoCaptureRef.current);
        }
        return () => clearInterval(autoCaptureRef.current);
    }, [autoCaptureInterval, takePhoto]);

    // Configurar el hook useVoiceInterface
    const { error, isListening } = useVoiceInterface({
        callTakePhoto: takePhoto,
        debug: true, // Puedes desactivar el modo debug si no lo necesitas
    });

    return (
        <section className="camera-section">
            <div className="camera-container">
                <video ref={videoRef} autoPlay playsInline className="camera-video" />
                {photo && (
                    <div className="download-container">
                        <a href={photo} download="captura.jpg">
                            <button className="download-button">Descargar Foto</button>
                        </a>
                    </div>
                )}
            </div>
            <ActionButtons onCameraButton={takePhoto} />
        </section>
    );
};

export default Camera;
