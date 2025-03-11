import os
import requests
import json
import cv2 as cv
from ROI import procesar_imagen

def enviar_imagen_a_api(imagen_path, api_url):
    """
    Envía una imagen a la API y devuelve la respuesta en formato JSON.
    :param imagen_path: Ruta de la imagen a enviar.
    :param api_url: URL de la API.
    :return: Respuesta de la API en formato JSON.
    """
    try:
        # Abrir la imagen en modo binario
        with open(imagen_path, 'rb') as imagen_file:
            # Enviar la imagen a la API usando una solicitud POST
            headers = {
                "accept": "application/json",             }
            files = {
                'image': (os.path.basename(imagen_path), imagen_file, 'image/png')  # Campo 'image' y tipo MIME
            }
            response = requests.post(api_url, headers=headers, files=files)

            # Verificar si la solicitud fue exitosa
            if response.status_code == 200:
                return response.json()  # Devolver la respuesta JSON
            else:
                print(f"Error: La API devolvió el código {response.status_code} para {imagen_path}.")
                return None
    except Exception as e:
        print(f"Error al enviar {imagen_path} a la API: {e}")
        return None

def procesar_carpeta(carpeta_imagenes, carpeta_salida, api_url):
    """
    Procesa todas las imágenes en una carpeta, las envía a la API y guarda las respuestas en archivos de texto.
    :param carpeta_imagenes: Ruta de la carpeta con las imágenes.
    :param carpeta_salida: Ruta de la carpeta donde se guardarán los archivos de texto.
    :param api_url: URL de la API.
    """
    # Verificar si la carpeta de salida existe, si no, crearla
    if not os.path.exists(carpeta_salida):
        os.makedirs(carpeta_salida)

    # Obtener la lista de imágenes en la carpeta
    imagenes = [img for img in os.listdir(carpeta_imagenes) if img.endswith(('orign.jpg', 'orign.jpeg'))]

    # Procesar cada imagen
    for imagen_nombre in imagenes:
        # Ruta completa de la imagen
        imagen_path = os.path.join(carpeta_imagenes, imagen_nombre)
        imagen = cv.imread(imagen_path)
        resultado = procesar_imagen(imagen)
        cv.imwrite(imagen_path+".tmp.jpg", resultado)


        # Enviar la imagen a la API
        respuesta_json = enviar_imagen_a_api(imagen_path+".tmp.jpg", api_url)

        if respuesta_json:
            # Guardar la respuesta JSON en un archivo de texto
            nombre_salida = os.path.splitext(imagen_nombre)[0] + '.txt'
            salida_path = os.path.join(carpeta_salida, nombre_salida)

            with open(salida_path, 'w') as f:
                json.dump(respuesta_json, f, indent=4)  # Guardar el JSON formateado

            # Ruta save
            imagen_save_path = os.path.join(carpeta_salida, imagen_nombre)
            cv.imwrite(imagen_save_path, resultado)

            print(f"Procesada: {imagen_nombre} -> {nombre_salida}")
        else:
            print(f"Error: No se pudo procesar {imagen_nombre}.")

if __name__ == '__main__':
    # Especificar la carpeta de imágenes, la carpeta de salida y la URL de la API
    carpeta_imagenes = 'backend/src/data/img-API/VEF/Model_6/'
    carpeta_salida = 'backend/src/data/img-API/TESTING/VEF/'
    api_url = 'https://cashreaderapi.share.zrok.io/detection/vef'  # Reemplaza con la URL de tu API

    # Procesar todas las imágenes en la carpeta
    procesar_carpeta(carpeta_imagenes, carpeta_salida, api_url)