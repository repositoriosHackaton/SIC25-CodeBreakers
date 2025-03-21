<br/>
<div align="center">
<a href="https://cashreader.netlify.app/"><img src="/frontend/public/favicon.svg" alt="Logo Cash Reader" width="80" height="80" style="vertical-align: middle;"></a>
<h3 align="center"><strong>Cash Reader</strong></h3>
<p align="center">
¡Transforma la manera en que interactúas con el dinero!
<br/>
<br/>
<a href="https://cashreader.netlify.app/"><strong>Visita nuestra página web »</strong></a>
<br/>
<br/>
<a href="https://github.com/repositoriosHackaton/SIC25-CodeBreakers/issues/new?labels=bug&amp;template=bug_report.md">| Reportar Bug |</a>
<a href="https://github.com/repositoriosHackaton/SIC25-CodeBreakers/issues/new?labels=enhancement&amp;&template=feature_request.md"> Solicitar funcionalidad |</a>
</p>

![Contributors](https://img.shields.io/github/contributors/repositoriosHackaton/SIC25-CodeBreakers)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![GitHub stars](https://img.shields.io/github/stars/repositoriosHackaton/SIC25-CodeBreakers)

![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Ultralytics YOLO](https://img.shields.io/badge/YOLO-blue?style=for-the-badge&logo=ultralytics)
![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)

</div>

**Cash Reader** es un proyecto realizado para el módulo de **Inteligencia Artificial** del curso *Samsung Innovation Campus*, y a su vez como proyecto final para la materia Programación III de la *Universidad Marítima del Caribe*.

## Índice de Contenidos
- [💡 ¿Qué es Cash Reader?](#-qué-es-cash-reader)
- [⚙️ Características clave](#️-características-clave)
- [🔧 Tecnologías](#-tecnologías)
- [📸 Imágenes](#-imágenes)
  - [Interfaz Web](#interfaz-web)
  - [Modelo de Clasificación de Bolívares](#modelo-de-clasificación-de-bolívares)
  - [Modelo de Clasificación de Dólares](#modelo-de-clasificación-de-dólares)
- [📜 Licencia](#-licencia)
- [👥 Integrantes del proyecto](#-integrantes-del-proyecto)
- [🎁 Donaciones](#-donaciones)

## 💡 ¿Qué es Cash Reader?
Se trata de un programa que integra:
- Dos modelos avanzados de **clasificación de objetos** para identificar las denominaciones de los billetes de **dólares y bolívares** y un modelo diferenciador entre ambos tipos de moneda.
- **Landing page** donde los usuarios pueden descargar la app (PWA) y conocer informacion general del proyecto.
- **App PWA** desarrollada bajo el cumplimiento del manual de los estandares de accesibilidad (**WCAG 2.0**) integrando un narrador, una interfaz de comandos de voz, una funcion de utilidad para contar de forma asistida y los modelos de IA para la clasificacion de billetes.

## 🦯 ¿Por qué se hizo este proyecto?
Este proyecto se planteó como un programa de asistencia dirigido a personas con **discapacidades visuales**, con el objetivo de brindar una herramienta que les resulte de utilidad y conveniencia en su vida cotidiana, facilitando su autonomía y mejorando su calidad de vida.

## ⚙️ Características clave
- Detección y clasificación de billetes (único modelo compatible en el mercado con el cono monetario actual de Venezuela) 💵.
- Interfaz a traves de una progressive web app (PWA) 🌐.
- 3 Modelos basados en **YOLOv8s** 🎯:
  - Clasificador de Denominación de billetes de Dolares Americanos.
  - Clasificador de Denominación de billetes de Bolivares Venezolanos.
  - Diferenciador entre ambos tipos de divisas.

## 🔧 Tecnologías
- **React:** Para una experiencia web fluida y arquitectura orientada a componentes.
- **FastAPI:** Para la creación de una API robusta.
- **YOLO Ultralytics:** Arquitectura de un Modelo CNN para la detección y clasificación.

## 🗄️ Datasets
- **11 mil fotos** para el modelo de los **dólares**
- **9 mil fotos** para el modelo de los **bolívares**, creada desde 0, todas tomadas por los miembros del equipo
## 📸 Imágenes
### Interfaz Web:
![Video de la landing page](/frontend/src/assets/landing.gif)

### Modelo de Clasificación de Bolívares:
<img src="./backend/src/models/train/VEF_model_13f/val_batch1_pred.jpg" alt="Imagen del Modelo VEF" style="max-width:50%; height:auto;">
<img src="./backend/src/models/train/VEF_model_13f/results.png" alt="Gráficas del modelo de Bolívares" style="max-width:50%; height:auto;">

### Modelo de Clasificación de Dólares:
<img src="./backend/src/models/train/USD_model_plus_01/val_batch1_pred.jpg" alt="Imagen del Modelo USD" style="max-width:50%; height:auto;">
<img src="./backend/src/models/train/USD_model_plus_01/results.png" alt="Gráficas del modelo de Dólares " style="max-width:50%; height:auto;">

## 📜 Licencia
Distribuido bajo la licencia MIT. Consulte [LICENCIA](./LICENSE.txt) para más información.

## 👥 Integrantes del proyecto
- [Francisco Ramos](https://www.linkedin.com/in/francisco-ramos-santos-dev)
- [Joshua Carrera](https://www.linkedin.com/in/joshua-carrera-r/) 
- [Joel Escobar](https://www.linkedin.com/in/joel-escobar/) 
- [Jesús Cabello](https://www.linkedin.com/in/jesus-cabello18/) 
- [Jesús Ramírez](https://www.linkedin.com/in/jesus-ramirez-dev/) 

## 🤝 Agradecimientos
- Pedro Borges: Admin de [Ciegos Venezuela](https://www.ciegosvenezuela.com/). Nos ayudó dándonos feedback de la aplicación desde la perspectiva del usuario final.
- Giancarlos Colasante: Profesor de Samsung.
- Stheisy Pimentel: Tutora de Samsung.
- Jenny Remolina: Profesora de Samsung.
- Álvaro Arauz: Tutor de Samsung.

## 🎁 Donaciones
Si deseas apoyar el proyecto, puedes enviar **USDT** a través de la red **Binance (BSC)**:
**Dirección:** 0xe826bd3f1b387eef0974d57c6b04d047cc443e75  
¡Tu contribución ayuda a impulsar la innovación!
