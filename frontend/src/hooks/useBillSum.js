import { useState, useEffect } from "react";

const useBillSum = () => {
    // Obtener los totales guardados en localStorage (si existen)
    const initialBolivares = parseInt(localStorage.getItem("CumSum_bs")) || 0;
    const initialDolares = parseInt(localStorage.getItem("CumSum_usd")) || 0;

    const [totalBolivares, setTotalBolivares] = useState(initialBolivares);
    const [totalDolares, setTotalDolares] = useState(initialDolares);

    // Guardar los totales en localStorage cada vez que cambien
    useEffect(() => {
        localStorage.setItem("CumSum_bs", totalBolivares);
    }, [totalBolivares]);

    useEffect(() => {
        localStorage.setItem("CumSum_usd", totalDolares);
    }, [totalDolares]);

    const addToTotal = (value, currency) => {
        if (currency === "bolivares") {
            setTotalBolivares((prevTotal) => prevTotal + value);
        } else if (currency === "dolares") {
            setTotalDolares((prevTotal) => prevTotal + value);
        }
    };

    const resetTotal = () => {
        // Guardar los totales actuales en CumSum_old antes de reiniciar
        localStorage.setItem("CumSum_old_bs", totalBolivares);
        localStorage.setItem("CumSum_old_usd", totalDolares);

        // Reiniciar los totales
        setTotalBolivares(0);
        setTotalDolares(0);
        localStorage.removeItem("CumSum_bs");
        localStorage.removeItem("CumSum_usd");
    };

    return { totalBolivares, totalDolares, addToTotal, resetTotal };
};

export default useBillSum;