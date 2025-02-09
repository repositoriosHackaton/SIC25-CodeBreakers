import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import { VitePWA } from "vite-plugin-pwa";

const version = (() => {
    const now = new Date();
    const day = String(now.getDate()).padStart(2, "0");
    const month = String(now.getMonth() + 1).padStart(2, "0");
    const year = now.getFullYear();
    const hours = String(now.getHours()).padStart(2, "0");
    const minutes = String(now.getMinutes()).padStart(2, "0");
    return `${day}.${month}.${year}.${hours}.${minutes}`;
})();

// https://vite.dev/config/
export default defineConfig({
    plugins: [
        react(),
        VitePWA({
            registerType: "autoUpdate",
            manifest: {
                display: "standalone",
                display_override: ["window-controls-overlay"],
                lang: "es-ES",
                name: `Cash reader v${version}`,
                short_name: "CashReader",
                description: "PWA Cash Reader para la identificacion de billetes",
                version: version,
                theme_color: "#28a745",
                background_color: "#343a40",
                icons: [
                    {
                        src: "/pwa-64x64.png",
                        sizes: "64x64",
                        type: "image/png",
                    },
                    {
                        src: "/pwa-192x192.png",
                        sizes: "192x192",
                        type: "image/png",
                        purpose: "any",
                    },
                    {
                        src: "/pwa-512x512.png",
                        sizes: "512x512",
                        type: "image/png",
                        purpose: "maskable",
                    },
                ],
                screenshots: [
                    {
                        src: "/form_factor_320x320.png",
                        sizes: "320x320",
                        type: "image/png",
                        form_factor: "wide",
                    },
                    {
                        src: "/form_factor_640x640_mobile.png",
                        sizes: "640x640",
                        type: "image/png",
                        form_factor: "narrow",
                    },
                ],
            },
        }),
    ],
});
