import os

def get_struct(inputs_path: str) -> dict(): #TODO Cambiar la estructura de los archivos para mejorar esto
    struct_input = []
    struct_output = []

    for root, dirs, files in os.walk(inputs_path):
        for file_name in files:
            struct_input.append(f"{root}/{file_name}")
            struct_output.append(f"{root.replace("unprocessed", "processed")}/{file_name}") #TODO Cambiar la estructura de los archivos para mejorar esto
    struct = {
        "input":struct_input,
        "output":struct_output,
    }
    return struct