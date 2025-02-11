import React from "react";
import "./PageApp.css";
import backgroundSvg from "../assets/page/bg/bg_front_page.svg";
import portadaImage from "../assets/page/hand_phone_front_page.png";
import iconInfo from "../assets/page/icons/info.svg";

const PageApp = () => {
    return (
        <div className="page-app">
            {/* Sección 1: Portada (front-page) – 2 columnas x 4 filas */}
            <section className="front-page" style={{ backgroundImage: `url(${backgroundSvg})` }}>
                <div className="front-content">
                    <div className="head-container">
                        <img src="/favicon.svg" alt="Logo Cash Reader" width="100" />
                        <h1>Cash Reader</h1>
                    </div>

                    <p className="text-front">
                        Nuestra app está pensada para brindarle independencia en el manejo del dinero en efectivo a
                        personas invidentes o con discapacidad visual.
                    </p>
                    <p className="text-phrase">
                        <em>Transforma la manera en que interactúas con el dinero</em>
                    </p>
                    <a href="#" className="cta-button">
                        ¡Empieza hoy mismo!
                    </a>
                </div>

                <img src={portadaImage} alt="App en teléfono" className="front-image" />
            </section>
            <section className="about-us">
                <div className="title-about">
                    <h2>Sobre Nosotros</h2>
                    <img src={iconInfo} alt="info" />
                </div>
                <div className="container-mission">
                    <h3>Misión</h3>
                    <p>
                        Presentamos una aplicación PWA accesible que cumple con los estándares WCAG, fácil de usar,
                        permitiendo a personas invidentes y con problemas de vista en Venezuela identificar de manera
                        rápida y efectiva los billetes en circulación.
                    </p>
                </div>
                <div className="container-vision">
                    <h3>Visión</h3>
                    <p>
                        Promover la igualdad de oportunidades, contribuyendo a mejorar la autonomía y calidad de vida
                        ofreciéndoles la capacidad de manejar su propio dinero a las personas invidentes o con problemas
                        de vista de forma independiente.
                    </p>
                </div>
            </section>
        </div>
    );
};

export default PageApp;
