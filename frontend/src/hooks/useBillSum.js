import { useState } from "react";

const useBillSum = () => {
    const [totalBolivares, setTotalBolivares] = useState(0); // Total en bolívares
    const [totalDolares, setTotalDolares] = useState(0); // Total en dólares

    // Función para agregar un nuevo valor al total correspondiente
    const addToTotal = (value, currency) => {
        if (currency === "bolivares") {
            setTotalBolivares((prevTotal) => prevTotal + value);
        } else if (currency === "dolares") {
            setTotalDolares((prevTotal) => prevTotal + value);
        }
    };

    // Función para reiniciar los totales
    const resetTotal = () => {
        setTotalBolivares(0);
        setTotalDolares(0);
    };

    return { totalBolivares, totalDolares, addToTotal, resetTotal };
};

export default useBillSum;