import os
import sys
import json
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont # Para dibujar las cajas

colors = [
    'blue',
    'green',
    'purple',
    'red',
    'black',
]

def log(path, boxes, image):
    file_name = datetime.now().strftime("%d-%m-%y %H:%M:%S")
    image_output_path = f"{path}{file_name}.jpg"
    text_output_path = f"{path}{file_name}.txt"
    try:
        # Guardar texto
        with open(text_output_path, "w") as text_file:
            text_file.write(json.dumps(boxes, indent=4))
        # Guardar imagen
        draw = ImageDraw.Draw(image)
        font = ImageFont.load_default() 
        for detection, color in zip(boxes, colors):
            bbox = detection["bbox"][0]  # Extraer la caja delimitadora
            draw.rectangle(bbox, outline=color, width=3)  # Dibujar un rectángulo

            label = f'{detection["label"]}  |  {float(detection["confidence"]):.4f}'  # Extraer la etiqueta
            text_position = (bbox[0], bbox[1] - 10)
            text_bg_position = (bbox[0], bbox[1] - 10, bbox[2], bbox[1])  # Fondo del texto
            draw.rectangle(text_bg_position, fill=color)  # Fondo rojo
            draw.text(text_position, label, fill="white", font=font)  # Texto blanco
        image.save(image_output_path)

    except Exception as e:
        print(f"Error al guardar el log: {e}")
        return