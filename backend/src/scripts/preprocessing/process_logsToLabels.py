import os
import json
import shutil
from PIL import Image

CLASS_MAPPING_USD = {
    "fifty-back": 0,
    "fifty-front": 1,
    "five-back": 2,
    "five-front": 3,
    "one-back": 4,
    "one-front": 5,
    "ten-back": 6,
    "ten-front": 7,
    "twenty-back": 8,
    "twenty-front": 9,
    "one_hundred-back": 10,
    "one_hundred-front": 11
}

CLASS_MAPPING_VEF = {
    "fifty-back-vef": 0,
    "fifty-front-vef": 1,
    "five-back-vef": 2,
    "five-front-vef": 3,
    "ten-back-vef": 4,
    "ten-front-vef": 5,
    "twenty-back-vef": 6,
    "twenty-front-vef": 7,
    "one_hundred-back-vef": 8,
    "one_hundred-front-vef": 9,
    "two_hundred-back-vef": 10,
    "two_hundred-front-vef": 11
}

def convert_single_image(origin_image_path, source_dir, target_dir):
    # Crear directorios si no existen
    os.makedirs(os.path.join(target_dir, "images"), exist_ok=True)
    os.makedirs(os.path.join(target_dir, "labels"), exist_ok=True)

    try:
        # Obtener nombre base sin _orign
        base_name = os.path.basename(origin_image_path).replace("_orign.jpg", "")
        json_filename = f"{base_name}_json.txt"
        
        # Rutas completas
        src_image_path = os.path.join(source_dir, origin_image_path)
        src_json_path = os.path.join(source_dir, json_filename)
        
        # Destinos
        dst_image_name = f"{base_name}.jpg"
        dst_image_path = os.path.join(target_dir, "images", dst_image_name)
        dst_label_path = os.path.join(target_dir, "labels", f"{base_name}.txt")

        # Copiar y renombrar la imagen
        shutil.copy2(src_image_path, dst_image_path)
        
        # Procesar JSON
        with Image.open(src_image_path) as img:
            img_width, img_height = img.size

        with open(src_json_path, 'r') as f:
            predictions = json.load(f)

        yolo_lines = []
        for prediction in predictions:
            label = prediction["label"]
            bbox = prediction["bbox"][0]
            
            # Conversión a YOLO
            x1, y1, x2, y2 = bbox
            x_center = (x1 + x2) / 2 / img_width
            y_center = (y1 + y2) / 2 / img_height
            width = (x2 - x1) / img_width
            height = (y2 - y1) / img_height

            if (0 <= x_center <= 1 and 0 <= y_center <= 1):
                class_id = CLASS_MAPPING_VEF.get(label)
                if class_id is not None:
                    yolo_line = f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}"
                    yolo_lines.append(yolo_line)

        # Escribir archivo de label
        if yolo_lines:
            with open(dst_label_path, 'w') as f:
                f.write("\n".join(yolo_lines))
                
    except Exception as e:
        print(f"Error procesando {origin_image_path}: {str(e)}")
        # Limpiar archivos en caso de error
        if os.path.exists(dst_image_path):
            os.remove(dst_image_path)
        if os.path.exists(dst_label_path):
            os.remove(dst_label_path)

def convert_dataset(source_dir, target_dir):
    # Listar solo archivos _orign.jpg
    for filename in os.listdir(source_dir):
        if filename.endswith("_orign.jpg"):
            # Saltar archivos _boxes
            if "_boxes" in filename:
                continue
                
            print(f"Procesando: {filename}")
            convert_single_image(filename, source_dir, target_dir)

# Ejemplo de uso
convert_dataset(
    source_dir="./backend/src/data/img-data-vef/process_model_09",
    target_dir="./backend/Dollar_Bill_Detection_VEF/dataset.v2"
)

# 5f-usd_08-03-25_03_59_40_boxes.txt
# ./backend/src/data/img-API/USD/Model_13
# ./backend/Dollar_Bill_Detection_USD/dataset