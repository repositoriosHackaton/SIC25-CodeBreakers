import os
import random
import shutil

def shuffle_yolo_dataset(dataset_dir, backup=True):
    """
    Desordena (shuffle) un dataset en formato YOLOv8 asegurando que las imágenes y sus etiquetas 
    mantengan su correspondencia. Opcionalmente, crea una copia de seguridad antes de renombrar.
    
    Parámetros:
    - dataset_dir (str): Ruta del dataset que contiene las carpetas 'images' y 'labels'.
    - backup (bool): Si True, crea una copia del dataset original antes de renombrar.
    """
    
    images_dir = os.path.join(dataset_dir, "images")
    labels_dir = os.path.join(dataset_dir, "labels")

    # Verificar que las carpetas existan
    if not os.path.exists(images_dir) or not os.path.exists(labels_dir):
        print("Error: No se encontraron las carpetas 'images' y 'labels' en el directorio especificado.")
        return
    
    # Crear una copia de seguridad si se requiere
    if backup:
        backup_dir = dataset_dir + "_backup"
        if not os.path.exists(backup_dir):
            shutil.copytree(dataset_dir, backup_dir)
            print(f"Copia de seguridad creada en: {backup_dir}")

    # Obtener lista de imágenes y filtrar solo archivos .jpg
    image_files = sorted([f for f in os.listdir(images_dir) if f.endswith('.jpg')])
    
    # Desordenar aleatoriamente
    random.shuffle(image_files)

    # Renombrar archivos de forma secuencial manteniendo correspondencia
    for idx, image_name in enumerate(image_files, start=1):
        old_image_path = os.path.join(images_dir, image_name)
        old_label_path = os.path.join(labels_dir, image_name.replace(".jpg", ".txt"))
        
        new_name = f"{idx:04d}"  # Formato 0001, 0002, etc.
        new_image_path = os.path.join(images_dir, f"{new_name}.jpg")
        new_label_path = os.path.join(labels_dir, f"{new_name}.txt")

        os.rename(old_image_path, new_image_path)
        if os.path.exists(old_label_path):  # Evitar errores si no hay label para una imagen
            os.rename(old_label_path, new_label_path)

    print("Dataset desordenado y renombrado exitosamente.")


shuffle_yolo_dataset("backend/Dollar_Bill_Detection_VEF/dataset.v3/val")
