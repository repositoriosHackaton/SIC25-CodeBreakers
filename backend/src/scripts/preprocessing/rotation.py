import os
import random
from PIL import Image

def rotate_image(image_path, angle):
    with Image.open(image_path) as img:
        return img.rotate(angle, expand=True)

def process_images(input_dir, output_dir, ranges):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    all_images = [f for f in os.listdir(input_dir) if f.endswith((".jpg", ".jpeg", ".png"))]
    num_images_per_range = len(all_images) // len(ranges)  # dividir en partes iguales según el número de rangos

    for idx, angle_range in enumerate(ranges):
        selected_images = random.sample(all_images, num_images_per_range)
        all_images = [img for img in all_images if img not in selected_images]

        for image_name in selected_images:
            image_path = os.path.join(input_dir, image_name)
            angle = random.uniform(*angle_range)
            rotated_image = rotate_image(image_path, angle)

            # Cambiar el nombre del archivo procesado agregando un _2 al final
            base_name, ext = os.path.splitext(image_name)
            new_image_name = f"{base_name}_2{ext}"

            output_image_path = os.path.join(output_dir, new_image_name)
            rotated_image.save(output_image_path)

    print("Procesamiento completado.")

# Configuración
input_dir = r'C:\Users\jesus\Desktop\Clones\cash_reader\backend\src\data\img-data-vef\processed\50\1\back'
output_dir = r'C:\Users\jesus\Desktop\Clones\cash_reader\backend\src\data\img-data-vef\processed\50\1\back2'
ranges = [(-180, -170), (-180, -170)]  # Rango de ángulos en grados, dos ángulos, por lo tanto será la mitad del 100%

process_images(input_dir, output_dir, ranges)
