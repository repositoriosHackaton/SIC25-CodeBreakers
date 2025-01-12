from flask import Flask, jsonify, request
from werkzeug.utils import secure_filename
import numpy as np
from PIL import Image
import cv2
import os
from ultralytics import YOLO

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'backend/src/api/uploads'

# Carga del modelo YOLO
model = YOLO('backend/src/models/Dollar_Model.pt')

@app.route('/detection', methods=['POST'])
def bill_detection():
    # Verificar si la solicitud incluye un archivo de imagen
    if 'image' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        # Guardar temporalmente el archivo
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Preprocesar la imagen
        img = Image.open(file_path).convert("RGB")
        #img = np.array(img)

        # Realizar predicción con el modelo YOLO
        results = model.predict(img)

        # Eliminar el archivo temporal
        os.remove(file_path)

        # Procesar resultados del modelo
        if len(results[0].boxes) > 0:
            # Encontrar la detección con mayor confianza
            highest_conf_box = max(results[0].boxes, key=lambda box: box.conf.item())
            result_data = {
                'label': highest_conf_box.cls.item(),  # Clase detectada
                'confidence': highest_conf_box.conf.item(),  # Confianza
                'bbox': highest_conf_box.xyxy.tolist()  # Coordenadas del cuadro
            }
            return jsonify(result_data), 200
        else:
            # Si no hay detecciones
            return jsonify({'message': 'No objects detected'}), 200

if __name__ == '__main__':
    app.run(debug=True)
