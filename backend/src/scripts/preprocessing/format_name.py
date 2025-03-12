import os
import random
import string

# Mapeo de prefijos según la clase (índice)
MAPPING = [
    "50b-",
    "50f-",
    "5b-",
    "5f-",
    "1b-",
    "1f-",
    "100b-",
    "100f-",
    "10b-",
    "10f-",
    "20b-",
    "20f-",
    "2b-",
    "2f-"
]

def generate_random_code(k=3):
    """Genera un código aleatorio alfanumérico de longitud k."""
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choices(characters, k=k))

def get_class_index(label_path):
    """
    Lee el archivo de label y devuelve el índice de clase (se asume que la primera línea 
    contiene al menos el índice de clase como primer token). Si falla, retorna None.
    """
    if not os.path.exists(label_path):
        return None
    try:
        with open(label_path, "r") as f:
            line = f.readline().strip()
            if line:
                parts = line.split()
                return int(parts[0])
    except Exception as e:
        print(f"Error leyendo {label_path}: {e}")
    return None

def process_file(image_path, labels_dir):
    """
    Renombra la imagen ubicada en image_path y su correspondiente archivo de label en labels_dir
    según las reglas descritas:
      - Si el nombre contiene "usd": se elimina todo lo anterior a "usd" y se usa el substring
        desde "usd" hasta "_jpg". Luego se le antepone el prefijo obtenido del mapeo (según la clase)
        y se le añade un código aleatorio de 3 caracteres.
      - Si el nombre contiene "IMG": se elimina desde "IMG" (inclusive) hasta "_jpg", se usa la parte
        anterior a "IMG" y se le añade el sufijo "-dtNet" (en lugar de "_jpg"). Luego se antepone el
        prefijo del mapeo y se añade el código aleatorio.
    """
    filename = os.path.basename(image_path)
    directory = os.path.dirname(image_path)
    lower_filename = filename.lower()

    # Construir la ruta del archivo de label (se asume que tiene extensión .txt y mismo base)
    label_filename = os.path.splitext(filename)[0] + ".txt"
    label_path = os.path.join(labels_dir, label_filename)
    class_index = get_class_index(label_path)
    if class_index is None or class_index >= len(MAPPING):
        print(f"Advertencia: No se pudo obtener un índice válido para {filename}. Se usará cadena vacía.")
        mapping_value = ""
    else:
        mapping_value = MAPPING[class_index]

    new_base = None

    if "usd" in lower_filename:
        # Procesar grupo USD:
        pos_usd = lower_filename.find("usd")
        pos_jpg = lower_filename.find("_jpg")
        if pos_usd == -1 or pos_jpg == -1 or pos_jpg <= pos_usd:
            print(f"Formato inesperado en el nombre {filename} para grupo usd.")
            return
        # Extraer el substring desde "usd" hasta justo antes de "_jpg"
        substring = filename[pos_usd:pos_jpg]
        new_base = mapping_value + substring  # Se antepone el mapeo
    elif "img" in filename:
        # Procesar grupo IMG:
        pos_IMG = filename.find("IMG")
        pos_jpg = filename.find("_jpg")
        if pos_IMG == -1 or pos_jpg == -1 or pos_jpg <= pos_IMG:
            print(f"Formato inesperado en el nombre {filename} para grupo IMG.")
            return
        # Tomar la parte antes de "IMG"
        base_before_IMG = filename[:pos_IMG]
        # Se descarta el fragmento desde "IMG" hasta "_jpg"
        # Y se reemplaza la parte "_jpg" por "-dtNet"
        new_base = mapping_value + base_before_IMG + "-dtNet"
    else:
        # Si no pertenece a ninguno de los grupos, se omite
        print(f"El archivo {filename} no pertenece a grupo 'usd' ni 'IMG'.")
        return

    # Añadir código aleatorio para asegurar unicidad
    random_code = generate_random_code(3)
    new_name = new_base + random_code + ".jpg"
    new_image_path = os.path.join(directory, new_name)
    
    # Si el nuevo nombre ya existe, repetir hasta conseguir uno único
    attempts = 0
    while os.path.exists(new_image_path) and attempts < 100:
        random_code = generate_random_code(3)
        new_name = new_base + random_code + ".jpg"
        new_image_path = os.path.join(directory, new_name)
        attempts += 1
    if attempts >= 100:
        print(f"No se pudo generar un nombre único para {filename}.")
        return

    # Renombrar la imagen
    os.rename(image_path, new_image_path)
    print(f"Imagen renombrada: {filename} -> {new_name}")

    # Renombrar el archivo de label (si existe)
    if os.path.exists(label_path):
        new_label_name = os.path.splitext(new_name)[0] + ".txt"
        new_label_path = os.path.join(labels_dir, new_label_name)
        os.rename(label_path, new_label_path)
        print(f"Etiqueta renombrada: {label_filename} -> {new_label_name}")
    else:
        print(f"No se encontró etiqueta para: {filename}")

def process_dataset(dataset_dir):
    """
    Procesa el dataset ubicado en dataset_dir, que debe contener dos carpetas:
    'images' y 'labels'. Recorre todas las imágenes JPG y aplica el renombrado según
    las reglas para archivos que contienen "usd" o "IMG".
    """
    images_dir = os.path.join(dataset_dir, "images")
    labels_dir = os.path.join(dataset_dir, "labels")
    
    if not os.path.isdir(images_dir) or not os.path.isdir(labels_dir):
        print("El directorio debe contener las carpetas 'images' y 'labels'.")
        return

    image_files = [f for f in os.listdir(images_dir) if f.lower().endswith(".jpg")]
    if not image_files:
        print("No se encontraron imágenes JPG en la carpeta 'images'.")
        return

    for image_file in image_files:
        image_path = os.path.join(images_dir, image_file)
        # Procesar solo si el nombre contiene "usd" o "IMG"
        if "usd" in image_file.lower() or "IMG" in image_file:
            process_file(image_path, labels_dir)
        else:
            print(f"Archivo omitido (no pertenece a grupo usd o IMG): {image_file}")

if __name__ == "__main__":
    dataset_dir = input("Ingresa la ruta del directorio del dataset: ").strip()
    if os.path.isdir(dataset_dir):
        process_dataset(dataset_dir)
    else:
        print("Directorio no válido.")


"""
[       
        "50b", 0
        "50f", 1
        "5b", 2
        "5f", 3
        "1b", 4
        "1f", 5
        "100b", 6 
        "100f", 7
        "10b", 8
        "10f", 9
        "20b", 10
        "20f", 11
        "2b", 12
        "2f", 13
]

fifty-back
fifty-front
five-back
five-front
one-back
one-front
one_hundred-back
one_hundred-front
ten-back
ten-front
twenty-back
twenty-front

"""
