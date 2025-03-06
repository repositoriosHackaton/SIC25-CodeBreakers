import React, { useEffect, useRef } from "react";
import "./PageApp.css";

const LinkedInBadge = ({ profileVanity = ""}) => {
  const scriptLoaded = useRef(false);

  useEffect(() => {
    if (!scriptLoaded.current) {
      const script = document.createElement("script");
      script.src = "https://platform.linkedin.com/badges/js/profile.js";
      script.async = true;
      //script.defer = true;
      document.head.appendChild(script);
      scriptLoaded.current = true;
    }

    

    return () => {
      // No eliminamos el script para evitar que se vuelva a cargar innecesariamente
    };
  }, []);

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
        >
        </a>
      </div>
    </div>
  );
};

export default LinkedInBadge;
