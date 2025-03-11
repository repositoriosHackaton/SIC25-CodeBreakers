import cv2 as cv
import numpy as np
from scipy.spatial.distance import cdist

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

def procesar_imagen(img, blurKernel=7, minThres=250, maxThres=0, blockSize=2, ksize=3, harrisThres=0, umbralDistancia=280):
    """
    Procesa una imagen para detectar esquinas con Harris, segmentar la ROI y devolver la imagen final.
    :param img: Imagen de entrada.
    :param blurKernel: Tamaño del kernel para el filtro borroso.
    :param minThres: Umbral mínimo para Canny.
    :param maxThres: Umbral máximo para Canny.
    :param blockSize: Tamaño del bloque para Harris Corner Detection.
    :param ksize: Tamaño del kernel para Harris Corner Detection.
    :param harrisThres: Umbral para Harris Corner Detection.
    :param umbralDistancia: Umbral de distancia para eliminar outliers.
    :return: Imagen final de la segmentación.
    """

    # Convertir la imagen a un array de NumPy
    if not isinstance(img, np.ndarray):
        img = cv2.cvtColor(np.array(img), cv.COLOR_RGB2BGR) # Convertir a cv2

    # Asegurarse de que el tamaño del kernel sea impar y mayor que 1
    if blurKernel < 1:
        blurKernel = 1
    if blurKernel % 2 == 0:
        blurKernel += 1

    # Aplicar el filtro borroso
    blurredImg = cv.GaussianBlur(img, (blurKernel, blurKernel), 0)

    # Aplicar el filtro de Canny a la imagen borrosa
    cannyEdge = cv.Canny(blurredImg, minThres, maxThres)

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

        # Recortar la ROI usando el rectángulo alineado con los ejes
        roi = img[y:y + h, x:x + w]

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
        return black_image
    else:
        # Si no hay suficientes puntos, mostrar la imagen original
        return img

if __name__ == '__main__':
    # Cargar una imagen
    img = cv.imread('backend/src/data/img-API/USD/Model_12/1f-usd_01-03-25_21_22_34_orign.jpg')

    # Procesar la imagen
    resultado = procesar_imagen(img, blurKernel=5, minThres=250, maxThres=0, blockSize=2, ksize=3, harrisThres=0, umbralDistancia=280)

    # Guardar o mostrar el resultado
    cv.imwrite('resultado_segmentacion.jpg', resultado)
    cv.imshow('Resultado', resultado)
    cv.waitKey(0)
    cv.destroyAllWindows()