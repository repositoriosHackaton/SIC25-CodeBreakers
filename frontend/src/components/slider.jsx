import React from "react";
import pytorchicon from "../assets/page/pytorch.png";
import FastIcon from "../assets/page/fastapi.svg"
import ReactIcon from "../assets/page/react.png"
import PytIcon from "../assets/page/python.png"
import CssIcon from "../assets/page/css.png"
import HtmlIcon from "../assets/page/html.png"
import JavaIcon from "../assets/page/javascript.png"
import YoloIcon from "../assets/page/yolo.png"
const InfiniteSlider = () => {
    const logos = [pytorchicon, FastIcon, ReactIcon, PytIcon,CssIcon,HtmlIcon,JavaIcon,YoloIcon];

    return (
        <div className="infinite-slider">
            <div className="slider-track">
                {/* Se repite el array 3 veces para asegurarnos de que no haya huecos en pantallas grandes */}
                {[...logos, ...logos, ...logos].map((logo, index) => (
                    <div className="slide" key={index}>
                        <img src={logo} alt={`Logo ${index}`} />
                    </div>
                ))}
            </div>
        </div>
        
    );
};


export default InfiniteSlider;