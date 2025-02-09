import React, { useRef, useEffect, useState, useCallback } from "react";
import axios from "axios";
import ActionButtons from "./ActionButtons";
import useApiResponseProcessor from "../hooks/useApiResponseProcessor";
import useNarrator from "../hooks/useNarrator";
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
     * Recibe un booleano `enabled` para activar (true) o desactivar (false) el flash.
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

    // Estado para obtener el stream de la cámara y gestionar el flash según la visibilidad
    useEffect(() => {
        const getCameraStream = async () => {
            try {
                const stream = await navigator.mediaDevices.getUserMedia({
                    video: { facingMode: "environment" },
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

        // Función para reactivar o desactivar el flash según la visibilidad de la página
        const handleVisibilityChange = () => {
            if (document.visibilityState === "visible") {
                //console.log("La app volvió al primer plano.");
                setFlash(true);
            } else {
                //console.log("La app pasó al segundo plano.");
                setFlash(false);
            }
        };

        document.addEventListener("visibilitychange", handleVisibilityChange);

        return () => {
            // Detener todos los tracks del stream de video
            if (videoRef.current && videoRef.current.srcObject) {
                const stream = videoRef.current.srcObject;
                stream.getTracks().forEach((track) => track.stop());
            }
            // Limpiar el intervalo de auto-captura
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

                const response = await axios.post("https://more-tough-herring.ngrok-free.app/detection", formData, {
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
     * Función para tomar la foto, redimensionarla y enviar la imagen.
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

        // Canvas para redimensionar la imagen a 416x416
        const resizedCanvas = document.createElement("canvas");
        const size = 416;
        resizedCanvas.width = size;
        resizedCanvas.height = size;
        const resizedContext = resizedCanvas.getContext("2d");
        resizedContext.drawImage(canvas, 0, 0, nativeWidth, nativeHeight, 0, 0, size, size);

        const imageUrl = resizedCanvas.toDataURL("image/jpeg");
        setPhoto(imageUrl);
        console.log("Foto tomada");
        sendPhotoToAPI(imageUrl);
    }, [sendPhotoToAPI]);

    // Estado para manejar el intervalo automático de captura según autoCaptureInterval
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
