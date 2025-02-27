import React, { useRef, useEffect, useState, useCallback } from "react";
import axios from "axios";
import ActionButtons from "./ActionButtons";
import useApiResponseProcessor from "../hooks/useApiResponseProcessor";
import useNarrator from "../hooks/useNarrator";
import { useVoiceInterface } from "../hooks/useVoiceInterface";
import { HELP_MESSAGE } from "../constants/HELP_MESSAGE";
import "./Camera.css";

const Camera = () => {
    // Refs para el video, el intervalo automático y el track de video
    const videoRef = useRef(null);
    const autoCaptureRef = useRef(null);
    const videoTrackRef = useRef(null);
    const toggleModelRef = useRef(true);
    // Estados locales
    const [photo, setPhoto] = useState(null);
    const [autoCaptureInterval, setAutoCaptureInterval] = useState(0);
    const [narration, setNarration] = useState("");
    const [toggleModel, setToggleModel] = useState(true);
    // Nuevo estado para la respuesta visual de la API
    const [apiPrediction, setApiPrediction] = useState("");

    // Función para limpiar la narración cuando finaliza
    const handleNarrationComplete = () => {
        setNarration("");
    };

    useEffect(() => {
        toggleModelRef.current = toggleModel;
    }, [toggleModel]);

    // Hooks para narración y procesamiento de respuesta
    // Se pasa setApiPrediction para actualizar la referencia visual
    useNarrator(narration, handleNarrationComplete);
    const { processResponse } = useApiResponseProcessor((message) => setNarration(message), setApiPrediction);

    /**
     * Función unificada para controlar el flash.
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
                    setFlash(true);
                }
            } catch (error) {
                console.error("Error al acceder a la cámara:", error);
            }
        };

        getCameraStream();

        const handleVisibilityChange = () => {
            if (document.visibilityState === "visible") {
                handleNarrationComplete();
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

    useEffect(() => {
        const handleStateModel = () => {
            if (document.visibilityState === "visible") {
                setNarration(`Modo actual: ${toggleModelRef.current ? "Bolívares" : "Dólares"}`);
            }
        };

        document.addEventListener("visibilitychange", handleStateModel);
        if (document.visibilityState === "visible") {
            handleStateModel();
        }
        return () => document.removeEventListener("visibilitychange", handleStateModel);
    }, []);

    // Función para cambiar el modelo
    const toggleModelHandler = () => {
        setToggleModel((prev) => !prev);
        setNarration(`Modo cambiado a ${!toggleModel ? "Bolívares" : "Dólares"}`);
    };

    /**
     * Función para enviar la imagen capturada a la API.
     */
    const sendPhotoToAPI = useCallback(
        async (imageData) => {
            try {
                const blob = await (await fetch(imageData)).blob();
                const formData = new FormData();
                formData.append("image", blob, "captura.jpg");

                const endpoint = toggleModel ? "vef" : "usd";
                const url = `https://cashreader.share.zrok.io/detection/${endpoint}`;

                const response = await axios.post(url, formData, {
                    headers: { "Content-Type": "multipart/form-data" },
                });

                console.log("Respuesta de la API:", response.data);
                processResponse(response.data);
            } catch (error) {
                console.error("Error al enviar la imagen a la API:", error);
                setNarration("No se ha podido comunicar con el servidor, intentelo mas tarde");
            }
        },
        [processResponse, toggleModel]
    );

    /**
     * Función para tomar la foto en resolución nativa y enviar la imagen.
     */
    const takePhoto = useCallback(() => {
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

    const HelpMessage = () => setNarration(HELP_MESSAGE);

    // Usamos el hook de voz, el cual devuelve start y stop
    const {
        error: voiceError,
        start,
        stop,
    } = useVoiceInterface({
        callTakePhoto: takePhoto,
        callToggleModel: toggleModelHandler,
        callHelpMessage: HelpMessage,
        debug: true,
    });

    // Eventos de gesto para activar/desactivar el reconocimiento (touch y mouse)
    return (
        <section className="camera-section">
            <div
                className="camera-container"
                onTouchStart={start}
                onTouchEnd={stop}
                onMouseDown={start}
                onMouseUp={stop}
                onMouseLeave={stop}
            >
                <video ref={videoRef} autoPlay playsInline className="camera-video" />
                {/* Overlay visual para la respuesta de la API */}
                {apiPrediction && <div className="api-response-overlay">{apiPrediction}</div>}
            </div>
            <div className="scan-indicator" key={toggleModel ? "VEF" : "USD"}>
                Scan: {toggleModel ? "VEF" : "USD"}
            </div>
            <ActionButtons onCameraButton={takePhoto} onToggleModel={toggleModelHandler} />
        </section>
    );
};

export default Camera;
