import os

def get_struct(base_path: str, input_dir, output_dir) -> dict():
    struct_input = []
    struct_output = []

    for root, dirs, files in os.walk(base_path):
        if input_dir in root.split('/'): # Recorremos solamente los archivos que son input
            for file_name in files:
                struct_input.append(f"{root}/{file_name}")
                struct_output.append(f"{root.replace(input_dir, output_dir)}/{file_name}") 
    struct = {
        "input":struct_input,
        "output":struct_output,
    }
    return struct