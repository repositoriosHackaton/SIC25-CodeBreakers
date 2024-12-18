import numpy as np
import cv2

IMAGES = './images/'
FILENAME = "05"

# Función para unir puntos cercanos en un contorno
def simplify_contour(contour, distance_threshold):
    simplified_contour = [contour[0][0]]  # Inicia con el primer punto
    for point in contour[1:]:
        last_point = simplified_contour[-1]
        # Calcular la distancia euclidiana entre el punto actual y el último en la lista
        distance = np.linalg.norm(point[0] - last_point)
        if distance > distance_threshold:
            simplified_contour.append(point[0])  # Agregar si la distancia es mayor al umbral
    return np.array(simplified_contour, dtype="int32")


# Cargar imagen
image = cv2.imread(IMAGES+FILENAME+".jpg")

# Convertir a escala de grises
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


# Aplicar un filtro para reducir el ruido
# blurred = cv2.GaussianBlur(gray, (5, 5), 0)
blurred = cv2.bilateralFilter(gray, 9, 75, 75)


# Detectar bordes con Canny
low_threshold = 300  # Ajustar estos valores según el contraste de la imagen
high_threshold = 25
edges = cv2.Canny(blurred, low_threshold, high_threshold)


# Dilate the image
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))  # Tamaño del kernel ajustable
dilataded = cv2.dilate(edges, kernel, iterations=1)
dilataded = cv2.morphologyEx(dilataded, cv2.MORPH_CLOSE, kernel)


# Mostrar la imagen de bordes
cv2.imshow("Bordes Detectados (Canny)", dilataded)

# Encontrar contornos
contours, _ = cv2.findContours(dilataded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

if contours:
    # Buscar el contorno más grande (suponiendo que es el billete)
    largest_contour = max(contours, key=cv2.contourArea)

    peri = cv2.arcLength(largest_contour, True)
    epsilon = 0.02 * peri
    approx = cv2.approxPolyDP(largest_contour, epsilon, True)

    distance_threshold = 250  # Umbral de distancia
    simplified_contour = simplify_contour(approx, distance_threshold)
    print(len(approx), "->", len(simplified_contour))

    # Dibujar el contorno detectado
    result = image.copy()
    cv2.drawContours(result, [simplified_contour], -1, (0, 255, 0), 2)

    # Mostrar la imagen con el contorno detectado
    cv2.imshow("Billete", image)
    cv2.imshow("Billete gray", gray)
    cv2.imshow("Billete blurred", blurred)
    cv2.imshow("Billete edges", edges)
    cv2.imshow("Billete dilataded", dilataded)
    cv2.imshow("Billete resultado", result)
    cv2.imwrite(IMAGES+"binary_image.jpg", dilataded)
    cv2.imwrite(IMAGES+FILENAME+"_result"+".jpg", result)
else:
    print("No se encontraron contornos.")



from PIL import Image, ImageDraw, ImageOps

PIL_org_image = Image.open(IMAGES+FILENAME+".jpg")
PIL_bin_image = Image.fromarray(dilataded).convert('L')
binary_image = PIL_bin_image.point(lambda p: p > 128 and 255)

bbox = binary_image.getbbox()  # (x_min, y_min, x_max, y_max)

draw = ImageDraw.Draw(PIL_org_image)
draw.rectangle(bbox, outline="green", width=10)
draw = ImageDraw.Draw(PIL_bin_image)
draw.rectangle(bbox, outline="green", width=10)

# Mostrar resultado
PIL_org_image.show()
#PIL_bin_image.show()

cv2.waitKey(0)
cv2.destroyAllWindows()
