import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import { VitePWA } from "vite-plugin-pwa";

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
                name: "Cash reader",
                short_name: "CashReader",
                description: "PWA Cash Reader para la identificacion de billetes",
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
                ],
            },
        }),
    ],
});
