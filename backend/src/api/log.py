import os
import sys
import json
from datetime import datetime

def log(path, text, image):
    file_name = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    image_output_path = f"{path}{file_name}.jpg"
    text_output_path = f"{path}{file_name}.txt"
    try:
        with open(text_output_path, "w") as text_file:
            text_file.write(json.dumps(text, indent=4))
        image.save(image_output_path)
    except Exception as e:
        print(f"Error al guardar el log: {e}")
        return