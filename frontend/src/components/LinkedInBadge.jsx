import React, { useEffect, useRef } from "react";
import "./PageApp.css";

const LinkedInBadge = ({ profileVanity = "" }) => {
    return (
        <div className="linkedin-badge-container">
            <div
                className="badge-base LI-profile-badge"
                data-locale="es_ES"
                data-size="large"
                data-theme="light"
                data-type="VERTICAL"
                data-vanity={profileVanity}
                data-version="v1"
            >
                <a
                    className="badge-base__link LI-simple-link"
                    href={`https://www.linkedin.com/in/${profileVanity}`}
                    target="_blank"
                    rel="noopener noreferrer"
                ></a>
            </div>
        </div>
    );
};

export default LinkedInBadge;
