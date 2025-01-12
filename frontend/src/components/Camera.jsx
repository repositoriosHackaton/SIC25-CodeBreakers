import React, { useRef, useEffect, useState } from "react";
import "./Camera.css"; // Archivo CSS para los estilos

const Camera = () => {
    const videoRef = useRef(null);
    const [photo, setPhoto] = useState(null);

    useEffect(() => {
        // Acceder a la cámara cuando el componente se monta
        const getCameraStream = async () => {
            try {
                const stream = await navigator.mediaDevices.getUserMedia({
                    video: {
                        width: { exact: 180 },
                        height: { exact: 180 },
                    },
                });
                if (videoRef.current) {
                    videoRef.current.srcObject = stream;
                }
            } catch (error) {
                console.error("Error al acceder a la cámara:", error);
            }
        };

        getCameraStream();

        return () => {
            // Detener el stream cuando el componente se desmonta
            if (videoRef.current && videoRef.current.srcObject) {
                const stream = videoRef.current.srcObject;
                const tracks = stream.getTracks();
                tracks.forEach((track) => track.stop());
            }
        };
    }, []);

    // Función para tomar la foto
    const takePhoto = () => {
        const canvas = document.createElement("canvas");
        const video = videoRef.current;
        const context = canvas.getContext("2d");

        // Establecer la resolución deseada para la foto (480x480)
        const size = 416;

        // Establecer el tamaño del canvas a 480x480
        canvas.width = size;
        canvas.height = size;

        // Dibujar la imagen del video redimensionada al tamaño del canvas
        context.drawImage(video, 0, 0, video.videoWidth, video.videoHeight, 0, 0, size, size);

        // Convertir la imagen a JPEG
        const imageUrl = canvas.toDataURL("image/jpeg");

        // Almacenar la imagen (solo por ahora, la podrás enviar más tarde al backend)
        setPhoto(imageUrl);
        console.log("Captura tomada");
    };

    return (
        <div className="camera-container">
            <video ref={videoRef} autoPlay playsInline className="camera-video"></video>
            <button className="camera-button" onClick={takePhoto}>
                <img src="/src/assets/camera_button.svg" alt="Capturar" />
            </button>

            {/* Si hay una foto, mostrar un botón para descargarla */}
            {photo && (
                <div className="download-container">
                    <a href={photo} download="captura.jpg">
                        <button className="download-button">Descargar Foto</button>
                    </a>
                </div>
            )}
        </div>
    );
};

export default Camera;
