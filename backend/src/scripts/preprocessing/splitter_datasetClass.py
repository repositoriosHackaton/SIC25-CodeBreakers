import os
import shutil

def split_dataset_by_class(dataset_dir, classSplit, dir_output):
    """
    Separa las imágenes y labels de un dataset en dos grupos:
      - Imágenes que tienen al menos una etiqueta con el id de clase classSplit se moverán a:
            {dir_output}/class_<classSplit>/images y /labels
      - El resto se moverán a:
            {dir_output}/dataset_splittedClass/images y /labels
    """
    # Directorios de entrada
    images_dir = os.path.join(dataset_dir, "images")
    labels_dir = os.path.join(dataset_dir, "labels")
    
    if not os.path.isdir(images_dir) or not os.path.isdir(labels_dir):
        print("El directorio del dataset debe contener las carpetas 'images' y 'labels'.")
        return

    # Directorios de salida para la clase a separar
    class_folder = os.path.join(dir_output, f"class_{classSplit}")
    class_images_out = os.path.join(class_folder, "images")
    class_labels_out = os.path.join(class_folder, "labels")
    
    # Directorios de salida para el resto del dataset
    others_folder = os.path.join(dir_output, "dataset_splittedClass")
    others_images_out = os.path.join(others_folder, "images")
    others_labels_out = os.path.join(others_folder, "labels")

    # Crear la estructura de carpetas de salida si no existen
    for folder in [class_images_out, class_labels_out, others_images_out, others_labels_out]:
        os.makedirs(folder, exist_ok=True)

    # Listar todas las imágenes (se asume extensión .jpg)
    image_files = [f for f in os.listdir(images_dir) if f.lower().endswith(".jpg")]
    
    for image_file in image_files:
        image_path = os.path.join(images_dir, image_file)
        # Se asume que el archivo label tiene el mismo nombre base y extensión .txt
        label_file = os.path.splitext(image_file)[0] + ".txt"
        label_path = os.path.join(labels_dir, label_file)

        if not os.path.exists(label_path):
            print(f"Advertencia: No se encontró label para {image_file}. Se omite este archivo.")
            continue

        # Leer el archivo de label y determinar si contiene la clase a separar
        include_class = False
        with open(label_path, "r") as f:
            for line in f:
                parts = line.strip().split()
                if parts:
                    try:
                        current_class = int(parts[0])
                        if current_class == classSplit:
                            include_class = True
                            break
                    except ValueError:
                        continue

        # Definir destino según si incluye la clase especificada
        if include_class:
            dest_images = class_images_out
            dest_labels = class_labels_out
        else:
            dest_images = others_images_out
            dest_labels = others_labels_out

        # Mover (o copiar) los archivos al destino correspondiente
        shutil.copy2(image_path, os.path.join(dest_images, image_file))
        shutil.copy2(label_path, os.path.join(dest_labels, label_file))
        print(f"Procesado: {image_file} -> {'class_' + str(classSplit) if include_class else 'dataset_splittedClass'}")

if __name__ == "__main__":
    dataset_dir = input("Ingresa la ruta del directorio del dataset (con 'images' y 'labels'): ").strip()
    classSplit_input = input("Ingresa el id de clase a separar (ej: 0): ").strip()
    dir_output = input("Ingresa la ruta del directorio de salida: ").strip()

    try:
        classSplit = int(classSplit_input)
    except ValueError:
        print("El id de clase debe ser un número entero.")
        exit(1)

    if not os.path.isdir(dataset_dir):
        print("El directorio del dataset no es válido.")
        exit(1)
    if not os.path.isdir(dir_output):
        print("El directorio de salida no es válido.")
        exit(1)

    split_dataset_by_class(dataset_dir, classSplit, dir_output)
