import os
from PIL import Image

def resize(input_img_path: str, output_img_path: str, target_size: tuple()):
    if not os.path.exists(output_img_path): # Si el archivo existe que lo ignore
        with Image.open(input_img_path) as img:
            try:
                resized_img = img.resize(target_size, Image.LANCZOS)
                resized_img.save(output_img_path, format="JPEG", quality=100)
                print(output_img_path)
            except Exception as e:
                print(f"El archivo {input_img_path} da error un '{e}'")
                exit()
            
def resize_group(base_path: str, input_dir: str, output_dir: str, target_size: tuple()):
    from get_struct import get_struct
    
    struct = get_struct(base_path, input_dir, output_dir)

    for input_img_path, output_img_path in zip(struct['input'], struct['output']):
        resize(input_img_path, output_img_path, target_size)

resize_group(
            base_path  = "backend/src/data/img-data-usd/unprocessed/5/",
            input_dir  = "unprocessed",
            output_dir = "processed",
            target_size= (416, 416),
            )