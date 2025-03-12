import cv2 as cv
import os
import numpy as np
from scipy.spatial.distance import cdist

def callback(input):
    pass

def eliminar_outliers(puntos, umbral_distancia=50):
    """
    Elimina los puntos que están demasiado lejos del centroide.
    :param puntos: Array de coordenadas de puntos (N, 2).
    :param umbral_distancia: Distancia máxima permitida desde el centroide.
    :return: Puntos filtrados.
    """
    if len(puntos) == 0:
        return puntos

    # Calcular el centroide de los puntos
    centroide = np.mean(puntos, axis=0)

    # Calcular la distancia de cada punto al centroide
    distancias = cdist(puntos, [centroide]).flatten()  # Aplanar la matriz de distancias

    # Filtrar los puntos que están dentro del umbral de distancia
    puntos_filtrados = puntos[distancias <= umbral_distancia]

    return puntos_filtrados

def segmentar_por_tamaño(roi, umbral_area=1000):
    """
    Segmenta la ROI por tamaño.
    :param roi: Región de interés (imagen recortada).
    :param umbral_area: Área mínima para considerar una región relevante.
    :return: Máscara binaria de la segmentación y la ROI filtrada.
    """
    # Convertir la ROI a escala de grises
    gray = cv.cvtColor(roi, cv.COLOR_RGB2GRAY)

    # Aplicar umbralización para obtener una máscara binaria
    _, mask = cv.threshold(gray, 0, 255, cv.THRESH_OTSU)

    # Encontrar contornos en la máscara
    contornos, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    # Filtrar contornos por área
    contornos_filtrados = [cnt for cnt in contornos if cv.contourArea(cnt) > umbral_area]

    # Crear una máscara vacía para dibujar los contornos filtrados
    mask_filtrada = np.zeros_like(mask)

    # Dibujar los contornos filtrados en la máscara
    cv.drawContours(mask_filtrada, contornos_filtrados, -1, 255, thickness=cv.FILLED)

    # Si hay contornos filtrados, seleccionar el más grande
    if len(contornos_filtrados) > 0:
        # Encontrar el contorno más grande
        cnt_principal = max(contornos_filtrados, key=cv.contourArea)

        # Crear una máscara solo para el contorno más grande
        mask_principal = np.zeros_like(mask)
        cv.drawContours(mask_principal, [cnt_principal], -1, 255, thickness=cv.FILLED)

        # Aplicar la máscara a la ROI original
        roi_filtrada = cv.bitwise_and(roi, roi, mask=mask_principal)
    else:
        # Si no hay contornos relevantes, devolver la máscara vacía y la ROI original
        roi_filtrada = roi
        mask_principal = np.zeros_like(mask)

    return mask_principal, roi_filtrada

def procesar_imagen(carpeta_imagenes):
    # Obtener la lista de imágenes en la carpeta
    imagenes = [img for img in os.listdir(carpeta_imagenes) if img.endswith(('orign.jpg', 'orign.jpeg'))]
    if not imagenes:
        print("Error: No se encontraron imágenes en la carpeta.")
        return

    # Índice de la imagen actual
    indice_imagen = 0

    # Crear ventanas para Canny, Harris Corner Detection y Segmentación
    cv.namedWindow('Canny')
    cv.namedWindow('Harris Corner Detection')
    cv.namedWindow('Segmentación')

    # Trackbar para el tamaño del kernel del filtro borroso
    cv.createTrackbar('blurKernel', 'Canny', 7, 30, callback)

    # Trackbars para los umbrales de Canny
    cv.createTrackbar('minThres', 'Canny', 250, 500, callback)
    cv.createTrackbar('maxThres', 'Canny', 0, 500, callback)

    # Trackbars para los parámetros de Harris Corner Detection
    cv.createTrackbar('blockSize', 'Harris Corner Detection', 2, 10, callback)  # blockSize (2-10)
    cv.createTrackbar('ksize', 'Harris Corner Detection', 3, 15, callback)      # ksize (3-15, debe ser impar)
    cv.createTrackbar('harrisThres', 'Harris Corner Detection', 0, 100, callback)  # Umbral (1-100)
    cv.createTrackbar('umbralDistancia', 'Harris Corner Detection', 280, 500, callback)  # Umbral de distancia (0-200)
    cv.createTrackbar('umbralArea', 'Harris Corner Detection', 90000, 100000, callback)  # Umbral de área (100-5000)

    while True:
        # Cargar la imagen actual
        img_path = os.path.join(carpeta_imagenes, imagenes[indice_imagen])
        img = cv.imread(img_path)

        # Verifica si la imagen se cargó correctamente
        if img is None:
            print(f"Error: No se pudo cargar la imagen {img_path}.")
            break

        # Obtener los valores de los trackbars para Canny
        minThres = cv.getTrackbarPos('minThres', 'Canny')
        maxThres = cv.getTrackbarPos('maxThres', 'Canny')
        blurKernel = cv.getTrackbarPos('blurKernel', 'Canny')

        # Asegurarse de que el tamaño del kernel sea impar y mayor que 1
        if blurKernel < 1:
            blurKernel = 1
        if blurKernel % 2 == 0:
            blurKernel += 1

        # Aplicar el filtro borroso
        blurredImg = cv.GaussianBlur(img, (blurKernel, blurKernel), 0)

        # Aplicar el filtro de Canny a la imagen borrosa
        cannyEdge = cv.Canny(blurredImg, minThres, maxThres)

        # Mostrar la imagen de Canny en su ventana
        cv.imshow('Canny', cannyEdge)

        # Obtener los valores de los trackbars para Harris Corner Detection
        blockSize = cv.getTrackbarPos('blockSize', 'Harris Corner Detection')
        ksize = cv.getTrackbarPos('ksize', 'Harris Corner Detection')
        harrisThres = cv.getTrackbarPos('harrisThres', 'Harris Corner Detection')
        umbralDistancia = cv.getTrackbarPos('umbralDistancia', 'Harris Corner Detection')
        umbralArea = cv.getTrackbarPos('umbralArea', 'Harris Corner Detection')

        # Asegurarse de que ksize sea impar y mayor que 1
        if ksize < 3:
            ksize = 3
        if ksize % 2 == 0:
            ksize += 1

        # Convertir la imagen de Canny a formato float32 para Harris Corner Detection
        cannyFloat32 = np.float32(cannyEdge)

        # Aplicar Harris Corner Detection a la imagen de Canny
        dst = cv.cornerHarris(cannyFloat32, blockSize, ksize, 0.04)

        # Dilatar el resultado para resaltar las esquinas
        dst = cv.dilate(dst, None)

        # Umbral para identificar las esquinas
        threshold = harrisThres / 100 * dst.max()  # Normalizar el umbral

        # Obtener las coordenadas de los puntos detectados por Harris
        corner_coords = np.column_stack(np.where(dst > threshold))

        # Invertir las coordenadas (fila, columna) a (x, y) para OpenCV
        corner_coords = corner_coords[:, ::-1]

        # Eliminar puntos outsiders
        corner_coords_filtrados = eliminar_outliers(corner_coords, umbral_distancia=umbralDistancia)

        # Verificar si hay suficientes puntos para calcular un rectángulo
        if len(corner_coords_filtrados) >= 4:
            # Calcular el rectángulo alineado con los ejes que cubre todos los puntos
            x, y, w, h = cv.boundingRect(corner_coords_filtrados)

            # Crear una copia de la imagen original para dibujar el rectángulo
            img_rect = img.copy()

            # Dibujar el rectángulo en la imagen original
            cv.rectangle(img_rect, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Rectángulo en verde

            # Mostrar la imagen con el rectángulo detectado
            cv.imshow('Harris Corner Detection', img_rect)

            # Recortar la ROI usando el rectángulo alineado con los ejes
            roi = img[y:y + h, x:x + w]

            # Segmentar la ROI por tamaño
            #mask_segmented, roi_filtrada = segmentar_por_tamaño(roi, umbral_area=umbralArea)

            # Crear una imagen negra del mismo tamaño que la imagen original
            black_image = np.zeros_like(img)

            # Colocar la ROI segmentada en la imagen negra
            # Primero, necesitamos calcular la posición donde colocar la ROI en la imagen negra
            # Para simplificar, colocamos la ROI en el centro de la imagen negra
            x_offset = (black_image.shape[1] - roi.shape[1]) // 2
            y_offset = (black_image.shape[0] - roi.shape[0]) // 2

            # Asegurarse de que la ROI no exceda los límites de la imagen negra
            if x_offset >= 0 and y_offset >= 0:
                black_image[y_offset:y_offset+roi.shape[0], x_offset:x_offset+roi.shape[1]] = roi

            # Mostrar la ROI segmentada en la imagen negra
            cv.imshow('Segmentación', black_image)
        else:
            # Si no hay suficientes puntos, mostrar la imagen original
            cv.imshow('Harris Corner Detection', img)

        # Mostrar el nombre de la imagen actual
        cv.setWindowTitle('Harris Corner Detection', f'Imagen {indice_imagen + 1}/{len(imagenes)}: {imagenes[indice_imagen]}')

        # Esperar a que el usuario presione una tecla
        key = cv.waitKey(1)

        # Navegación entre imágenes
        if key == ord('a'):  # Tecla 'a' para retroceder
            indice_imagen = (indice_imagen - 1) % len(imagenes)
        elif key == ord('d'):  # Tecla 'd' para avanzar
            indice_imagen = (indice_imagen + 1) % len(imagenes)
        elif key == ord('q'):  # Tecla 'q' para salir
            break

    cv.destroyAllWindows()

if __name__ == '__main__':
    # Especifica la carpeta que contiene las imágenes
    carpeta_imagenes = 'backend/src/data/img-API/VEF/Model_9'
    procesar_imagen(carpeta_imagenes)