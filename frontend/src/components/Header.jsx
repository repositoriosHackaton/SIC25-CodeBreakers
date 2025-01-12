import React from "react";
import "./Header.css";

const Header = () => {
    return (
        <header className="header">
            <div className="logo-container">
                <img src="/favicon.svg" alt="Logo de la App" className="logo" />
                <h1 className="app-name">Cash Reader</h1>
            </div>
        </header>
    );
};

export default Header;
