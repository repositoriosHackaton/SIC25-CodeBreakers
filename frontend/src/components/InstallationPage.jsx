import React from "react";
import InstallButton from "./InstallButton";
import "./InstallationPage.css";

const InstallationPage = () => {
    return (
        <div className="container-home">
            <div className="logo-container">
                <img src="/favicon.svg" alt="Logo de la App" className="logo" />
                <h1 className="app-name">Cash Reader</h1>
            </div>
            <p className="description-home">
                CashReader es una app que te ayudará a reconocer billetes, tanto bolivares como dolares a traves del uso
                de un modelo de inteligencia artificial. La podras manejar a traves de su amigable interfaz o por
                comandos de voz
            </p>
            <InstallButton />
        </div>
    );
};

export default InstallationPage;
