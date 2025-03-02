import cv2
from ultralytics import YOLO

# Cargar el modelo YOLO
model = YOLO(r'C:\Users\jesus\Documents\Proyectos\Cashreader\backend\Dollar_Bill_Detection_VEF\prueba\VEF_Model_10.pt')

# Inicializar la cámara
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("No se pudo abrir la cámara.")
    exit()

while True:
    # Capturar frame por frame
    ret, frame = cap.read()

    if not ret:
        print("No se pudo recibir frame (final de la transmisión?). Saliendo ...")
        break

    # Realizar la predicción
    results = model.predict(frame)

    # Dibujar las detecciones en el frame
    for result in results:
        boxes = result.boxes
        for box in boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cls = int(box.cls[0])
            confidence = box.conf[0]

            # Obtener la etiqueta de la clase
            label = model.names[cls]

            # Dibujar la caja delimitadora y la etiqueta
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
            cv2.putText(frame, f'{label}: {confidence:.2f}', (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    # Mostrar el frame con las detecciones
    cv2.imshow('YOLO Detections', frame)

    # Añadir un pequeño retraso y verificar la tecla presionada
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar la cámara y cerrar ventanas
cap.release()
cv2.destroyAllWindows()
