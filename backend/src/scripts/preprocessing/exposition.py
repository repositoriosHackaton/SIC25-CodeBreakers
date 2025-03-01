from PIL import Image, ImageEnhance
import os
import random

# Rutas de las carpetas de imágenes y etiquetas
image_folder = 'backend/Dollar_Bill_Detection_VEF/test/images'
label_folder = 'backend/Dollar_Bill_Detection_VEF/test/labels'

# Factor de aumento de exposición
exposure_factor = 1.2  # Aumenta la exposición en un 20%

# Clases que se van a modificar
classes_to_modify = {2, 3, 6, 7}

# Porcentaje de imágenes a modificar (30%)
percentage_to_modify = 0.3

# Obtener la lista de imágenes en la carpeta
image_files = [f for f in os.listdir(image_folder) if f.endswith('.jpg') or f.endswith('.png')]

# Filtrar solo las imágenes que pertenecen a las clases a modificar
images_to_process = []
for image_filename in image_files:
    label_filename = os.path.splitext(image_filename)[0] + '.txt'
    label_path = os.path.join(label_folder, label_filename)
    
    if os.path.exists(label_path):
        with open(label_path, 'r') as label_file:
            first_line = label_file.readline().strip()
            class_id = int(first_line.split()[0])
            if class_id in classes_to_modify:
                images_to_process.append(image_filename)

# Calcular el número de imágenes a modificar
total_images = len(images_to_process)
num_images_to_modify = int(total_images * percentage_to_modify)

# Procesar solo el porcentaje especificado de imágenes
for i, image_filename in enumerate(images_to_process):
    if i < num_images_to_modify:
        # Construye la ruta completa de la imagen
        image_path = os.path.join(image_folder, image_filename)
        
        # Construye la ruta del archivo de etiqueta correspondiente
        label_filename = os.path.splitext(image_filename)[0] + '.txt'
        label_path = os.path.join(label_folder, label_filename)
        
        # Abre la imagen
        image = Image.open(image_path)
        
        # Aumenta la exposición
        enhancer = ImageEnhance.Brightness(image)
        image = enhancer.enhance(exposure_factor)
        
        # Crea un nuevo nombre para la imagen modificada
        new_image_filename = os.path.splitext(image_filename)[0] + '_exposure' + os.path.splitext(image_filename)[1]
        new_image_path = os.path.join(image_folder, new_image_filename)
        
        # Guarda la imagen modificada con el nuevo nombre
        image.save(new_image_path)
        print(f'Creada nueva imagen: {new_image_filename}')
        
        # Crea una copia de la etiqueta con el nuevo nombre
        new_label_filename = os.path.splitext(image_filename)[0] + '_exposure.txt'
        new_label_path = os.path.join(label_folder, new_label_filename)
        
        # Copia el contenido de la etiqueta original a la nueva etiqueta
        with open(label_path, 'r') as label_file, open(new_label_path, 'w') as new_label_file:
            new_label_file.write(label_file.read())
        print(f'Creada nueva etiqueta: {new_label_filename}')
    else:
        print(f'No se modifica {image_filename} - Límite de porcentaje alcanzado')

print(f'Proceso completado. Se modificaron {num_images_to_modify} de {total_images} imágenes.')