import os
import albumentations as A
import numpy, random, cv2

def random_select(struct: dict, percentage):
    num_to_select= int(len(struct['input']) * percentage / 100)
    id_to_select = random.sample(range(len(struct['input'])), num_to_select)
    
    struct['input']  = [item for i, item in enumerate(struct['input']) if i in id_to_select]
    struct['output'] = [item for i, item in enumerate(struct['output']) if i in id_to_select]

    mixed = list(zip(struct['input'], struct['output']))
    random.shuffle(mixed)
    struct['input'], struct['output'] = zip(*mixed)

    return struct

def divide_select(struct, transformations):
    size_input = len(struct['input'])
    num_of_output = len(transformations)+1 # +1 Por el mix
    
    return [size_input // num_of_output + (1 if i < size_input % num_of_output else 0) for i in range(num_of_output)]


def noise(input_img_path: str, output_img_path: str, transformations):
    #print(transformations)

    input_img = cv2.imread(input_img_path) # Cargar la imagen de entrada
    augmented = transformations(image=input_img) # Aplicar la transformación de ruido
    transformed_img = augmented['image'] # Obtener la imagen transformada
    
    path_list = output_img_path.split(".") 
    output_img_path = path_list[0] + "_augmented." + path_list[1] 

    cv2.imwrite(output_img_path, transformed_img)
    print(f"Imagen transformada guardada en {output_img_path}")

def noise_group(base_path: str, input_dir: str, output_dir: str, q_percentage: int, transformations):
    from get_struct import get_struct
    
    struct = get_struct(base_path, input_dir, output_dir)

    struct = random_select(struct, q_percentage)

    num_of_output = numpy.cumsum(divide_select(struct, transformations))

    num_imgs, index_transform = 0, 0
    for input_img_path, output_img_path in zip(struct['input'], struct['output']):

        if num_imgs >= num_of_output[index_transform]:
            index_transform+=1
        
        if index_transform == len(num_of_output)-1:# El mix y la ultima transformación
            noise(input_img_path, output_img_path, transformations)
        else:
            noise(input_img_path, output_img_path, transformations[index_transform])
       
        num_imgs+=1



noise_group(
            base_path    = "backend/src/data/img-data-vef/",
            input_dir    = "processed",
            output_dir   = "augmentation",
            q_percentage = 5,
            transformations = A.Compose([
                    A.RGBShift(r_shift_limit=20, g_shift_limit=20, b_shift_limit=20, p=1),
                    A.RandomBrightnessContrast(brightness_limit=0.15, contrast_limit=0.25, p=1),
                    A.Blur(blur_limit=4, p=1),
                    A.SaltAndPepper(salt_vs_pepper=(0.4, 0.6), amount=(0.01, 0.06), p=1),
                ])
            )