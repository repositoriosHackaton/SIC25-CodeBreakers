import React from "react";
import "./PageApp.css";
import creator1 from "../assets/page/creators/creator1.png"; // Ajusta las rutas según tu proyecto
import creator2 from "../assets/page/creators/creator2.png"; // Ajusta las rutas según tu proyecto
import creator3 from "../assets/page/creators/creator3.png"; // Ajusta las rutas según tu proyecto
import creator4 from "../assets/page/creators/creator4.png"; // Ajusta las rutas según tu proyecto
import backgroundSvg from "../assets/page/bg/bg_front_page.svg";
import backgroundTwoSvg from "../assets/page/bg/bg_neural.svg";
import portadaImage from "../assets/page/hand_phone_front_page.png";
import iconInfo from "../assets/page/icons/info.svg";
import iconWcag from "../assets/page/icons/wcag.png";
import iconGears from "../assets/page/icons/gears.svg";
import iconBocina from "../assets/page/icons/bocina.svg";
import iconCamera from "../assets/page/icons/camera.svg";
import iconGithub from "../assets/page/icons/github.svg";
import iconSamsung from "../assets/page/samsung.jpg";
import iconUmc from "../assets/page/umc.png";
import iconSteam from "../assets/page/steam.svg";
import InstallButton from "./InstallButton";

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
                    <div className="install-button-container">
                        <InstallButton />
                    </div>
                </div>
                <div className="image-container">
                    <img src={portadaImage} alt="App en teléfono" className="front-image" />
                </div>
            </section>
            {/* Sección 2: Sobre nosotros (about-us)*/}
            <section className="about-us" style={{ backgroundImage: `url(${backgroundTwoSvg})` }}>
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
                <div className="container-mission">
                    <h3>Visión</h3>
                    <p>
                        Promover la igualdad de oportunidades, contribuyendo a mejorar la autonomía y calidad de vida
                        ofreciéndoles la capacidad de manejar su propio dinero a las personas invidentes o con problemas
                        de vista de forma independiente.
                    </p>
                </div>
                <div className="features">
                    <div className="feature">
                        <img src={iconCamera} alt="Cámara" />
                        <h3>Identificación instantánea</h3>
                        <p>Captura una imagen del billete y obtén resultados en segundos.</p>
                    </div>
                    <div className="feature">
                        <img src={iconGears} alt="Gears" />
                        <h3>Modelo de IA</h3>
                        <p>Clasifica billetes en bolívares y dólares con alta precisión.</p>
                    </div>
                    <div className="feature">
                        <img src={iconWcag} alt="Wcag" style={{ width: '35%', height: '35%' }} />
                        <h3>Diseño inclusivo</h3>
                        <p>Una interfaz pensada para todos, priorizando la usabilidad.</p>
                    </div>
                    <div className="feature">
                        <img src={iconBocina} alt="Bocina" />
                        <h3>Narrador integrado</h3>
                        <p>Recibe respuestas claras y detalladas en tiempo real.</p>
                    </div>
                </div>
            </section>

            <section className="creators-page" style={{ backgroundImage: `url(${backgroundSvg})` }}>
                <h2 className="creators-title">Nuestros Creadores</h2>
                <p className="creators-description">Conoce al equipo que hizo posible este proyecto.</p>
                <div className="creators-grid">
                    {/* Creador 1 */}
                    <div className="creator-card">
                        <img src={creator1} alt="Creador 1" className="creator-image" />
                        <h3 className="creator-name">Nombre del Creador 1</h3>
                        <p className="creator-role">Rol del Creador 1</p>
                    </div>
                    {/* Creador 2 */}
                    <div className="creator-card">
                        <img src={creator2} alt="Creador 2" className="creator-image" />
                        <h3 className="creator-name">Nombre del Creador 2</h3>
                        <p className="creator-role">Rol del Creador 2</p>
                    </div>
                    {/* Creador 3 */}
                    <div className="creator-card">
                        <img src={creator3} alt="Creador 3" className="creator-image" />
                        <h3 className="creator-name">Nombre del Creador 3</h3>
                        <p className="creator-role">Rol del Creador 3</p>
                    </div>
                    {/* Creador 4 */}
                    <div className="creator-card">
                        <img src={creator4} alt="Creador 4" className="creator-image" />
                        <h3 className="creator-name">Nombre del Creador 4</h3>
                        <p className="creator-role">Rol del Creador 4</p>
                    </div>
                </div>
            </section>

            <section className="donations-page" style={{ backgroundImage: `url(${backgroundTwoSvg})` }}>
                <h2 className="donations-title">Apoya Nuestro Proyecto</h2>
                <p className="donations-description">
                    Tu contribución nos ayuda a seguir mejorando y manteniendo esta aplicación gratuita para todos.
                </p>
                <a href="https://tudominio.com/donar" target="_blank" rel="noopener noreferrer" className="donate-button"> Hacer una Donación</a>
            </section>

            <footer className="footer">
                <div className="left-column">
                    <a href="https://github.com/Fran2310/cash_reader" target="_blank" rel="noopener noreferrer">
                        <img src={iconGithub} alt="Github" />
                        Visita Nuestro Repositorio
                    </a>
                    <p>Desarrollado por CodeBreakers Team’s</p>
                    <a href="mailto:cashreader.info@gmail.com" className="contact-button">
                        Contacto: cashreader.info@gmail.com
                    </a>
                </div>
                <div className="right-column">
                    <div className="partner-logos">
                        <img src={iconUmc} alt="UMC" />
                        <img src={iconSteam} alt="Steam" />
                        <img src={iconSamsung} alt="Samsung" />
                    </div>
                </div>
            </footer>
        </div>
    );
};

export default PageApp;
