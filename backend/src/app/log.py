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

<<<<<<< HEAD
def log(path, boxes, image):
    file_name = datetime.now().strftime("%d-%m-%y %H:%M:%S")
    image_output_path = f"{path}{file_name}.jpg"
    text_output_path = f"{path}{file_name}.txt"
    try:
        # Guardar texto
        with open(text_output_path, "w") as text_file:
            text_file.write(json.dumps(boxes, indent=4))
        # Guardar imagen
=======
values = {
    # USD
    'fifty-back'       : '50f-usd',  'fifty-front'       : '50f-usd',
    'five-back'        : '5b-usd',   'five-front'        : '5f-usd',
    'one-back'         : '1b-usd',   'one-front'         : '1f-usd', 
    'ten-back'         : '10b-usd',  'ten-front'         : '10f-usd', 
    'twenty-back'      : '20b-usd',  'twenty-front'      : '20f-usd',
    'one_hundred-back' : '100b-usd', 'one_hundred-front' : '100f-usd',
    # VEF
    'fifty-back-vef'       : '50f-vef',  'fifty-front-vef'       : '50f-vef',
    'five-back-vef'        : '5b-vef',   'five-front-vef'        : '5f-vef',
    'ten-back-vef'         : '10b-vef',  'ten-front-vef'         : '10f-vef', 
    'twenty-back-vef'      : '20b-vef',  'twenty-front-vef'      : '20f-vef',
    'one_hundred-back-vef' : '100b-vef', 'one_hundred-front-vef' : '100f-vef',
    'two_hundred-back-vef' : '100b-vef', 'two_hundred-front-vef' : '100f-vef',
}

async def log(path, boxes, image):
    if not os.path.exists(path):
        os.makedirs(path)
    file_name = datetime.now().strftime("%d-%m-%y_%H_%M_%S")
    value = values[boxes[0]["label"]] # Valor pasado por el diccionario
    orign_image_output_path = f"{path}{value}_{file_name}_orign.jpg"
    boxes_image_output_path = f"{path}{value}_{file_name}_boxes.jpg"
    text_output_path =        f"{path}{value}_{file_name}_json.txt"
    try:
        # Guardar Original
        image.save(orign_image_output_path)
        # Guardar texto
        with open(text_output_path, "w") as text_file:
            text_file.write(json.dumps(boxes, indent=4))
        # Guardar Boxes
>>>>>>> origin/backend
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
<<<<<<< HEAD
        image.save(image_output_path)

    except Exception as e:
        print(f"Error al guardar el log: {e}")
        return
=======
        image.save(boxes_image_output_path)

    except Exception as e:
        print(f"Error al guardar el log: {e}")
        return
>>>>>>> origin/backend
