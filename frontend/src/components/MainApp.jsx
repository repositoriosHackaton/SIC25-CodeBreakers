import React from "react";
import Header from "./Header";
import Camera from "./Camera";
import VoiceInterface from "./VoiceInterface";
import "./MainApp.css";

const App = () => {
    return (
        <div className="container">
            <header className="header">
                <Header />
            </header>
            <Camera />
        </div>
    );
};

export default App;
