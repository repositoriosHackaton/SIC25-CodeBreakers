import os

# Cambiar las etiquetas de los archivos .txt

def main():
    try:
        # Solicitar números de reemplazo
        even = int(input("Número para reemplazar cifras pares: "))
        odd = int(input("Número para reemplazar cifras impares: "))
    except ValueError:
        print("¡Error! Debes ingresar números enteros.")
        return

    # Pedir directorio
    dir_path = input("Ruta de la carpeta (deja vacío para actual): ").strip()
    if not dir_path:
        dir_path = os.getcwd()

    # Procesar archivos .txt
    for filename in os.listdir(dir_path):
        if not filename.endswith(".txt"):
            continue
            
        filepath = os.path.join(dir_path, filename)
        
        with open(filepath, 'r+') as file:
            lines = file.readlines()  # Leer todas las líneas
            file.seek(0)  # Volver al inicio del archivo
            file.truncate()  # Limpiar el archivo para sobrescribir

            for line in lines:
                if not line.strip():  # Si la línea está vacía, la ignoramos
                    file.write(line)
                    continue

                # Extraer el primer número de la línea
                parts = line.split()
                if not parts:
                    file.write(line)
                    continue

                try:
                    cifra = int(parts[0])  # Convertir el primer elemento a número
                except ValueError:
                    file.write(line)  # Si no es un número, dejamos la línea como está
                    continue

                # Determinar reemplazo
                replacement = str(even if cifra % 2 == 0 else odd)

                # Reemplazar el primer número en la línea
                parts[0] = replacement
                nueva_linea = " ".join(parts) + "\n"

                # Escribir la línea modificada
                file.write(nueva_linea)

    print("¡Proceso completado!")

if __name__ == "__main__":
    main()