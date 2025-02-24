import React, { useEffect } from "react";
import Header from "./Header";
import Camera from "./Camera";
import "./MainApp.css";

const App = () => {
    useEffect(() => {
        // Al montar, añade la clase "no-overscroll" al body
        document.body.classList.add("no-overscroll");
        return () => {
            // Al desmontar, remuévela
            document.body.classList.remove("no-overscroll");
        };
    }, []);
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
