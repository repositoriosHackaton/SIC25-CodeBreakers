import os
import shutil
import random

# Define el directorio raíz donde están las carpetas 1, 2 y 3
root_dir = r"C:\Users\jesus\Downloads\output"

# Definir las rutas de las carpetas
folders = ["0", "1", "2", "3","4","5","6","7","8","9","10","11"]
subfolders = ["images", "labels"]
test_images_path = os.path.join(root_dir, "valid", "image")
test_labels_path = os.path.join(root_dir, "valid", "label")

# Crear las carpetas de test si no existen
os.makedirs(test_images_path, exist_ok=True)
os.makedirs(test_labels_path, exist_ok=True)

# Cantidad de imágenes a extraer por en cada subfolder del folder
num_images = {"0":17 , "1":18, "2":17, "3":18,"4":17,"5":18,"6":17,"7":18,"8":17,"9":18,"10":17,"11":18}
for folder in folders:
    for subfolder in subfolders:
        image_path = os.path.join(root_dir, folder,"images")
        label_path = os.path.join(root_dir, folder, "labels")

        # Obtener todas las imágenes y etiquetas
        all_images = [f for f in os.listdir(image_path) if f.endswith(".jpg")]
        all_labels = [f for f in os.listdir(label_path) if f.endswith(".txt")]

        # Verificar que haya suficientes imágenes para seleccionar
        if len(all_images) >= num_images[folder]:
            # Seleccionar imágenes al azar
            selected_images = random.sample(all_images, num_images[folder])
        
            # Copiar y eliminar imágenes y etiquetas correspondientes
            for image in selected_images:
                image_name = image
                label_name = image.replace(".jpg", ".txt")

                # Rutas completas de la imagen y la etiqueta
                image_src = os.path.join(image_path, image_name)
                label_src = os.path.join(label_path, label_name)

                # Verificar si los archivos existen antes de copiarlos y eliminarlos
                if os.path.exists(image_src) and os.path.exists(label_src):
                    # Copiar imagen
                    shutil.copy(image_src, test_images_path)
                    # Copiar etiqueta correspondiente
                    shutil.copy(label_src, test_labels_path)

                    # Eliminar la imagen y la etiqueta originales
                    os.remove(image_src)
                    os.remove(label_src)
                else:
                    print(f"Archivo no encontrado: {image_src} o {label_src}")
        else:
            print(f"No hay suficientes imágenes en la carpeta {folder}/{subfolder} para seleccionar {num_images[folder]} imágenes.")

print("Imágenes y etiquetas copiadas y eliminadas correctamente.")
