// components/LinkedInBadge.jsx
import React, { useEffect } from "react";
import "./PageApp.css";

const LinkedInBadge = ({ profileVanity, name }) => {
  useEffect(() => {
    // Cargar script dinámicamente
    const script = document.createElement("script");
    script.src = "https://platform.linkedin.com/badges/js/profile.js";
    script.async = true;
    script.defer = true;
    document.head.appendChild(script);

    return () => {
      document.head.removeChild(script);
    };
  }, []);

  return (
    <div
      className="badge-base LI-profile-badge"
      data-locale="es_ES"
      data-size="medium"
      data-theme="light"
      data-type="VERTICAL"
      data-vanity={profileVanity}
      data-version="v1"
    >
      <a
        className="badge-base__link LI-simple-link"
        href={`https://ve.linkedin.com/in/${profileVanity}`}
      >
        {name}
      </a>
    </div>
  );
};

export default LinkedInBadge;