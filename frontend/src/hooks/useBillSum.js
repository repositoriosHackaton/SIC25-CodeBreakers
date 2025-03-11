import { useState } from "react";
 
 const useBillSum = () => {
     const [total, setTotal] = useState(0); // Estado para almacenar el total acumulado
 
     // Función para agregar un nuevo valor al total
     const addToTotal = (value) => {
         setTotal((prevTotal) => prevTotal + value);
     };
 
     // Función para reiniciar el total a 0
     const resetTotal = () => {
         setTotal(0);
     };
 
     return { total, addToTotal, resetTotal };
 };
 
 export default useBillSum;