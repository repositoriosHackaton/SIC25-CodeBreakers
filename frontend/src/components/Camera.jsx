import React, { useRef, useEffect, useState, useCallback } from "react";
import axios from "axios";
import ActionButtons from "./ActionButtons";
import useApiResponseProcessor from "../hooks/useApiResponseProcessor";
import useNarrator from "../hooks/useNarrator";
import { useVoiceInterface } from "../hooks/useVoiceInterface";
import { HELP_MESSAGE } from "../constants/HELP_MESSAGE";
import "./Camera.css";

const Camera = () => {
    /* ================================
     REFS
     ================================ */
    // Referencia al elemento de video
    const videoRef = useRef(null);
    // Referencia para el intervalo automático de captura
    const autoCaptureRef = useRef(null);
    // Referencia para el primer track del stream de video
    const videoTrackRef = useRef(null);
    // Referencia mutable para mantener el valor actual del modelo
    const toggleModelRef = useRef(true);

    /* ================================
     ESTADOS LOCALES
     ================================ */
    const [photo, setPhoto] = useState(null);
    const [autoCaptureInterval, setAutoCaptureInterval] = useState(0);
    const [narration, setNarration] = useState("");
    const [toggleModel, setToggleModel] = useState(true);
    // Estado para mostrar la respuesta visual de la API sobre el stream
    const [apiPrediction, setApiPrediction] = useState("");

    /* ================================
     FUNCIONES AUXILIARES
     ================================ */
    // Limpia el estado de narración (usado tras finalizar la narración)
    const handleNarrationComplete = () => {
        setNarration("");
    };

    // Mantener sincronizado toggleModelRef con el estado toggleModel
    useEffect(() => {
        toggleModelRef.current = toggleModel;
    }, [toggleModel]);

    /* ================================
     HOOKS DE NARRACIÓN Y RESPUESTA DE LA API
     ================================ */
    // Configura el narrador
    useNarrator(narration, handleNarrationComplete);
    // Configura el procesamiento de la respuesta de la API.
    // Se pasa setApiPrediction para actualizar la referencia visual (overlay).
    const { processResponse } = useApiResponseProcessor((message) => setNarration(message), setApiPrediction);

    /* ================================
     CONTROL DEL FLASH
     ================================ */
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

    /* ================================
     CONFIGURACIÓN DEL STREAM DE VIDEO Y GESTIÓN DE VISIBILIDAD
     ================================ */
    useEffect(() => {
        // Función asíncrona para obtener el stream de la cámara
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
                    // Activar el flash cuando se inicia el stream
                    setFlash(true);
                }
            } catch (error) {
                console.error("Error al acceder a la cámara:", error);
            }
        };

        // Obtener el stream al montar el componente
        getCameraStream();

        // Handler para gestionar cambios en la visibilidad (primer plano/segundo plano)
        const handleVisibilityChange = () => {
            if (document.visibilityState === "visible") {
                // Al volver al primer plano, limpiar la narración y reiniciar la cámara si es necesario
                handleNarrationComplete();
                if (!videoRef.current.srcObject) {
                    getCameraStream();
                }
            } else {
                // Al ir a segundo plano, detener todos los tracks del stream y limpiar la referencia
                if (videoRef.current && videoRef.current.srcObject) {
                    const stream = videoRef.current.srcObject;
                    stream.getTracks().forEach((track) => track.stop());
                    videoRef.current.srcObject = null;
                }
                setFlash(false);
            }
        };

        document.addEventListener("visibilitychange", handleVisibilityChange);

        return () => {
            document.removeEventListener("visibilitychange", handleVisibilityChange);
            if (videoRef.current && videoRef.current.srcObject) {
                const stream = videoRef.current.srcObject;
                stream.getTracks().forEach((track) => track.stop());
            }
            clearInterval(autoCaptureRef.current);
        };
    }, []);

    // Efecto adicional para notificar el estado del modelo al volver al primer plano
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

    /* ================================
     CAMBIAR MODELO
     ================================ */
    const toggleModelHandler = () => {
        setToggleModel((prev) => !prev);
        setNarration(`Modo cambiado a ${!toggleModel ? "Bolívares" : "Dólares"}`);
    };

    /* ================================
     LIMPIEZA DEL OVERLAY DE LA RESPUESTA DE LA API
     ================================ */
    useEffect(() => {
        if (apiPrediction) {
            const timer = setTimeout(() => {
                setApiPrediction("");
            }, 10000); // El overlay se limpia a los 10 segundos
            return () => clearTimeout(timer);
        }
    }, [apiPrediction]);

    /* ================================
     CAPTURA Y ENVÍO DE FOTO A LA API
     ================================ */
    // Función para enviar la imagen a la API
    const sendPhotoToAPI = useCallback(
        async (imageData) => {
            try {
                const blob = await (await fetch(imageData)).blob();
                const formData = new FormData();
                formData.append("image", blob, "captura.jpg");

                // Seleccionar el endpoint según el modelo actual
                const endpoint = toggleModel ? "vef" : "usd";
                const url = `https://cashreaderapi.share.zrok.io/detection/${endpoint}`;

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

    // Función para capturar la imagen en resolución nativa y enviarla a la API
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

    /* ================================
     CAPTURA AUTOMÁTICA (SI SE CONFIGURA)
     ================================ */
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

    /* ================================
     MENSAJE DE AYUDA
     ================================ */
    const HelpMessage = () => setNarration(HELP_MESSAGE);

    /* ================================
     CONFIGURACIÓN DE LA INTERFAZ DE VOZ
     ================================ */
    // El hook de voz devuelve start y stop para gestionar la activación mediante gestos.
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

    /* ================================
     RENDERIZADO DEL COMPONENTE
     ================================ */
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
                {/* Video en vivo */}
                <video ref={videoRef} autoPlay playsInline className="camera-video" />
                {/* Overlay visual para la respuesta de la API */}
                {apiPrediction && <div className="api-response-overlay">{apiPrediction}</div>}
            </div>
            {/* Indicador visual del modo actual */}
            <div className="scan-indicator" key={toggleModel ? "VEF" : "USD"}>
                Scan: {toggleModel ? "VEF" : "USD"}
            </div>
            {/* Botones de acción */}
            <ActionButtons onCameraButton={takePhoto} onToggleModel={toggleModelHandler} />
        </section>
    );
};

export default Camera;
