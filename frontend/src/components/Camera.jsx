import React, { useRef, useEffect, useState } from "react";
import axios from "axios";
import ActionButtons from "./ActionButtons";
import "./Camera.css";

const Camera = () => {
    const videoRef = useRef(null);
    const [photo, setPhoto] = useState(null);
    const [autoCaptureInterval, setAutoCaptureInterval] = useState(0); // Intervalo en segundos por defecto
    const autoCaptureRef = useRef(null); // Referencia para manejar el intervalo automático
    const videoTrackRef = useRef(null); // Referencia para el track de video

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
                        width: { exact: 416 },
                        height: { exact: 416 },
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
        const canvas = document.createElement("canvas");
        const video = videoRef.current;
        const context = canvas.getContext("2d");

        const size = 416;
        canvas.width = size;
        canvas.height = size;

        context.drawImage(video, 0, 0, video.videoWidth, video.videoHeight, 0, 0, size, size);

        const imageUrl = canvas.toDataURL("image/jpeg");
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
        } catch (error) {
            console.error("Error al enviar la imagen a la API:", error);
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
