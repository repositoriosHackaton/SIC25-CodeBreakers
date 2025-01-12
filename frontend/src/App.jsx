import React from "react";
import Header from "./components/Header";
import Camera from "./components/Camera";
import ActionButtons from "./components/ActionButtons";
import "./App.css";

const App = () => {
    return (
        <div className="container">
            <header className="header">
                <Header />
            </header>
            <section className="camera-section">
                <Camera />
            </section>
            <section className="buttons-section">
                <ActionButtons />
            </section>
        </div>
    );
};

export default App;
