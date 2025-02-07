import React, { useRef, useEffect, useState } from "react";
import axios from "axios";
import ActionButtons from "./ActionButtons";
import VoiceInterface from "./VoiceInterface";
import useApiResponseProcessor from "../hooks/useApiProcessResponse";
import useNarrator from "../hooks/useNarrator";
import "./Camera.css";

const Camera = () => {
    const videoRef = useRef(null);
    const [photo, setPhoto] = useState(null);
    const [autoCaptureInterval, setAutoCaptureInterval] = useState(0);
    const autoCaptureRef = useRef(null);
    const videoTrackRef = useRef(null);
    const [narration, setNarration] = useState("");

    useNarrator(narration);

    const { processResponse } = useApiResponseProcessor((message) => {
        if (message !== narration) {
            setNarration(message); // Actualizar solo si el mensaje cambia
        }
    });

    const activateFlash = async () => {
        if (videoTrackRef.current) {
            const capabilities = videoTrackRef.current.getCapabilities();
            if (capabilities.torch) {
                try {
                    await videoTrackRef.current.applyConstraints({
                        advanced: [{ torch: true }],
                    });
                    console.log("Flash activado.");
                } catch (error) {
                    console.error("Error al activar el flash:", error);
                }
            } else {
                console.warn("El dispositivo no soporta el control del flash.");
            }
        }
    };

    const deactivateFlash = async () => {
        if (videoTrackRef.current) {
            try {
                await videoTrackRef.current.applyConstraints({
                    advanced: [{ torch: false }],
                });
                console.log("Flash desactivado.");
            } catch (error) {
                console.error("Error al desactivar el flash:", error);
            }
        }
    };

    useEffect(() => {
        // Obtener acceso a la cámara
        const getCameraStream = async () => {
            try {
                const stream = await navigator.mediaDevices.getUserMedia({
                    video: {
                        facingMode: "environment", // Para usar la cámara trasera
                    },
                });

                if (videoRef.current) {
                    videoRef.current.srcObject = stream;

                    // Guardar el primer track de video
                    const [videoTrack] = stream.getVideoTracks();
                    videoTrackRef.current = videoTrack;

                    // Activar el flash inicialmente
                    activateFlash();
                }
            } catch (error) {
                console.error("Error al acceder a la cámara:", error);
            }
        };

        getCameraStream();

        const handleVisibilityChange = () => {
            if (document.visibilityState === "visible") {
                console.log("La app volvió al primer plano.");
                activateFlash(); // Reactivar el flash al volver al primer plano
            } else {
                console.log("La app pasó al segundo plano.");
                deactivateFlash(); // Desactivar el flash al ir al segundo plano
            }
        };

        document.addEventListener("visibilitychange", handleVisibilityChange);

        return () => {
            // Limpiar recursos al desmontar el componente
            if (videoRef.current && videoRef.current.srcObject) {
                const stream = videoRef.current.srcObject;
                const tracks = stream.getTracks();
                tracks.forEach((track) => track.stop());
            }

            deactivateFlash(); // Apagar el flash antes de detener el track

            if (videoTrackRef.current) {
                videoTrackRef.current.stop();
            }

            clearInterval(autoCaptureRef.current); // Limpiar el intervalo automático
            document.removeEventListener("visibilitychange", handleVisibilityChange);
        };
    }, []);

    // Manejar el intervalo automático
    useEffect(() => {
        if (autoCaptureInterval > 0) {
            clearInterval(autoCaptureRef.current); // Limpiar el intervalo existente
            autoCaptureRef.current = setInterval(() => {
                takePhoto();
            }, autoCaptureInterval * 1000);
        } else {
            clearInterval(autoCaptureRef.current); // Detener el intervalo si es 0
        }
    }, [autoCaptureInterval]);

    const takePhoto = () => {
        const video = videoRef.current;

        if (!video) {
            console.error("Video no disponible.");
            return;
        }

        const nativeWidth = video.videoWidth;
        const nativeHeight = video.videoHeight;

        const canvas = document.createElement("canvas");
        canvas.width = nativeWidth;
        canvas.height = nativeHeight;

        const context = canvas.getContext("2d");
        context.drawImage(video, 0, 0, nativeWidth, nativeHeight);

        // Crear un segundo canvas para reescalar la imagen
        const resizedCanvas = document.createElement("canvas");
        const size = 416;
        resizedCanvas.width = size;
        resizedCanvas.height = size;

        const resizedContext = resizedCanvas.getContext("2d");
        resizedContext.drawImage(canvas, 0, 0, nativeWidth, nativeHeight, 0, 0, size, size);

        const imageUrl = resizedCanvas.toDataURL("image/jpeg");
        setPhoto(imageUrl);
        console.log("Captura tomada");
        sendPhotoToAPI(imageUrl);
    };

    const sendPhotoToAPI = async (imageData) => {
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
            setNarration("Error al procesar la imagen.");
        }
    };

    return (
        <section className="camera-section">
            <div className="camera-container">
                <video ref={videoRef} autoPlay playsInline className="camera-video"></video>
                {photo && (
                    <div className="download-container">
                        <a href={photo} download="captura.jpg">
                            <button className="download-button">Descargar Foto</button>
                        </a>
                    </div>
                )}
            </div>
            <ActionButtons onRedClick={takePhoto} />
        </section>
    );
};

export default Camera;
