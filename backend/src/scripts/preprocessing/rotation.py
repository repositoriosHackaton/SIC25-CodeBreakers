import os
import random
from PIL import Image
"""
def rotate_image(image_path, angle):
    with Image.open(image_path) as img:
        return img.rotate(angle, expand=True)

def process_images(input_dir, output_dir, ranges):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    all_images = [f for f in os.listdir(input_dir) if f.endswith((".jpg", ".jpeg", ".png"))]
    num_images_per_range = len(all_images) // 4  # dividir en partes iguales según el número de rangos

    for idx, angle_range in enumerate(ranges):
        selected_images = all_images # cambiado para seleccionar todas las imagenes
        all_images = [img for img in all_images if img not in selected_images]

        for image_name in selected_images:
            image_path = os.path.join(input_dir, image_name)
            angle = random.uniform(*angle_range)
            rotated_image = rotate_image(image_path, angle)

            # Cambiar el nombre del archivo procesado agregando un _2 al final
            base_name, ext = os.path.splitext(image_name)
            new_image_name = f"{base_name}_{angle_range}{ext}"

            output_image_path = os.path.join(output_dir, new_image_name)
            rotated_image.save(output_image_path)
            print(output_image_path)

    print("Procesamiento completado.")

# Configuración
input_dir = 'backend/src/data/img-data-usd/processed/5/'
output_dir = 'backend/src/data/img-data-usd/processed/5/'
ranges = [(-90,-91), (90,91)]  # Rango de ángulos en grados, dos ángulos, por lo tanto será la mitad del 100%

process_images(input_dir, output_dir, ranges)
"""


def rotate_images_in_directory(directory):
    # Verifica si el directorio existe
    if not os.path.exists(directory):
        print(f"El directorio {directory} no existe.")
        return

    # Recorre todos los archivos en el directorio
    for filename in os.listdir(directory):
        if filename.lower().endswith('.jpg'):
            # Abre la imagen
            image_path = os.path.join(directory, filename)
            with Image.open(image_path) as img:
                # Rotaciones: 90, 180, 270 grados
                for angle in [90, 180, 270]:
                    rotated_img = img.rotate(angle, expand=True)
                    # Guarda la imagen rotada con un nombre nuevo
                    new_filename = f"{os.path.splitext(filename)[0]}_rotated_{angle}.jpg"
                    new_image_path = os.path.join(directory, new_filename)
                    rotated_img.save(new_image_path)
                    print(f"Guardada {new_image_path}")

if __name__ == "__main__":
    # Solicita al usuario el directorio
    directory = 'backend/src/data/img-data-usd/processed/5/'
    rotate_images_in_directory(directory)

