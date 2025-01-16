import React from "react";
import InstallButton from "./InstallButton";

const InstallationPage = () => {
    return (
        <div style={{ textAlign: "center", padding: "2rem" }}>
            <h1>Mi App</h1>
            <p>Esta es una app que te ayudará a reconocer billetes de forma inteligente.</p>
            <InstallButton />
        </div>
    );
};

export default InstallationPage;
