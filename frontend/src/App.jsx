import React from "react";
import Header from "./components/Header";
import Camera from "./components/Camera";
import "./App.css";

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
