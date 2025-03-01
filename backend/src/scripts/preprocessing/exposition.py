from PIL import Image, ImageEnhance
import os

# Rutas de las carpetas de imágenes y etiquetas
image_folder = 'backend/Dollar_Bill_Detection_VEF/test/images'
label_folder = 'backend/Dollar_Bill_Detection_VEF/test/labels'

# Factor de aumento de exposición
exposure_factor = 1.2  # Aumenta la exposición en un 10%

# Clases que se van a modificar
classes_to_modify = {2, 3, 6, 7}

# Recorre todas las imágenes en la carpeta de imágenes
for image_filename in os.listdir(image_folder):
    if image_filename.endswith('.jpg') or image_filename.endswith('.png'):
        # Construye la ruta completa de la imagen
        image_path = os.path.join(image_folder, image_filename)
        
        # Construye la ruta del archivo de etiqueta correspondiente
        label_filename = os.path.splitext(image_filename)[0] + '.txt'
        label_path = os.path.join(label_folder, label_filename)
        
        # Verifica si el archivo de etiqueta existe
        if os.path.exists(label_path):
            with open(label_path, 'r') as label_file:
                # Lee la primera línea del archivo de etiqueta
                first_line = label_file.readline().strip()
                # Extrae la clase (primer número en la línea)
                class_id = int(first_line.split()[0])
                
                # Si la clase está en las clases a modificar, aumenta la exposición
                if class_id in classes_to_modify:
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
                    print(f'Creada nueva imagen: {new_image_filename} (Clase {class_id})')
                    
                    # Crea una copia de la etiqueta con el nuevo nombre
                    new_label_filename = os.path.splitext(image_filename)[0] + '_exposure.txt'
                    new_label_path = os.path.join(label_folder, new_label_filename)
                    
                    # Copia el contenido de la etiqueta original a la nueva etiqueta
                    with open(new_label_path, 'w') as new_label_file:
                        new_label_file.write(first_line)
                    print(f'Creada nueva etiqueta: {new_label_filename}')
                else:
                    print(f'No se modifica {image_filename} (Clase {class_id})')
        else:
            print(f'No se encontró etiqueta para {image_filename}')

print('Proceso completado.')