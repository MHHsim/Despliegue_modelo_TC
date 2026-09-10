# Despliegue Modelo — Bank Marketing API

API desarrollada para realizar predicciones sobre el dataset **Bank Marketing**, utilizando modelos de Machine Learning previamente entrenados durante el Bootcamp de Data Science.

La API recibe información de un cliente, realiza el procesamiento necesario, asigna un segmento mediante **KMeans** y genera una predicción mediante un modelo de clasificación.

---


## Descripción del proyecto

La API realiza las siguientes operaciones:

1. Recibe las **15 variables originales** del dataset.
2. Valida los datos recibidos.
3. Convierte las variables numéricas al formato correspondiente.
4. Escala las variables necesarias utilizando un `scaler` previamente entrenado.
5. Asigna un segmento de cliente mediante un modelo **KMeans**.
6. Realiza la predicción final mediante un modelo de clasificación.
7. Devuelve los resultados en formato **JSON**.

### Resultado de la predicción

La API devuelve dos valores:

* `segment`: segmento de cliente asignado por KMeans.
* `prediction`:
       * `0` → el cliente **no contratará** el producto.
       * `1` → el cliente **contratará** el producto.

---

## Estructura del proyecto

```text
Despliegue_modelo_TC/
│
├── app/
│   ├── model/
│   │   ├── __init__.py
│   │   ├── predictor.py
│   │   ├── model_bank_marketing.pkl
│   │   ├── kmeans_segmentacion.pkl
│   │   └── scaler_segmentacion.pkl
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   └── .gitignore
│   │
│   ├── __init__.py
│   └── main.py
│
├── README.md
├── requirements.txt
├── runtime.txt
└── .gitignore
```

---

## Dependencias utilizadas

* Python
* Flask
* Catboost
* Gunicorn
* Pandas
* NumPy
* Scikit-learn
* Render

---

## Flujo de trabajo con Git (Git Flow)

El proyecto sigue un flujo de ramas estructurado:

| Rama | Propósito |
|------|-----------|
| `main` | Código en producción. Solo recibe cambios vía Pull Request. |
| `develop` | Integración de funcionalidades antes de pasar a producción. |
| `feature/nombre` | Desarrollo de una funcionalidad concreta. |
## Instalación y configuración

### 1. Clonar el repositorio

```bash
git clone https://github.com/MHHsim/Despliegue_modelo_TC.git
cd Despliegue_modelo_TC
```

### 2. Crear un entorno virtual

#### Mac / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Instalar las dependencias

```bash
pip install -r requirements.txt
```

---

## Ejecutar la API localmente

Para iniciar la aplicación, ejecuta:

```bash
python -m app.main
```

Por defecto, la API estará disponible en:

```text
http://localhost:5000
```

También puedes acceder utilizando:

```text
http://127.0.0.1:5000
```

---

## Usar la API en línea

La API está desplegada y disponible públicamente en Render:
https://despliegue-modelo-tc.onrender.com

No requiere instalación ni configuración: cualquier persona con conexión a internet puede consultarla directamente.

También puedes acceder utilizando:
requests.get("https://despliegue-modelo-tc.onrender.com")

Manteniendo la misma estructura de tres bloques, es decir, URL principal, forma alternativa de acceso, pero adaptado al hecho de que aquí no hay "puerto" ni "localhost" — solo la URL pública.

Los endpoints que abarca la aplicación se detallan a continuación.

---

## Endpoints

### POST `/predict`

Permite realizar una predicción enviando los datos del cliente en formato JSON.

#### Ejemplo de petición

```json
{
  "age": 42,
  "balance": 1500,
  "day": 5,
  "campaign": 1,
  "previous": 0,
  "pdays": -1,
  "job": "admin",
  "marital": "married",
  "education": "secondary",
  "default": "no",
  "housing": "yes",
  "loan": "no",
  "contact": "cellular",
  "month": "may",
  "poutcome": "unknown"
}
```

#### Respuesta

```json
{
  "prediction": 1,
  "probability": 0.5441,
  "segment": 3
}
```

#### Interpretación

En este ejemplo:

* `prediction: 1` → el modelo predice que el cliente **contratará el producto**.
* `probability: 0.5441` → el modelo asigna una **probabilidad del 54,41 %** a la predicción realizada.
* `segment: 3` → el cliente pertenece al **segmento 3**.

---

### GET `/predict`

También es posible realizar una predicción mediante parámetros enviados directamente en la URL.

#### Ejemplo

```text
/predict?age=42&balance=1500&day=5&campaign=1&previous=0&pdays=-1&job=admin&marital=married&education=secondary&default=no&housing=yes&loan=no&contact=cellular&month=may&poutcome=unknown
```

La API devuelve la predicción en formato JSON con la misma estructura que el endpoint `POST /predict`.

#### Ejemplo de respuesta

```json
{
  "prediction": 1,
  "probability": 0.5441,
  "segment": 3
}
```

#### Interpretación

* `prediction` indica la clase predicha por el modelo.
* `probability` indica la probabilidad asociada a dicha predicción.
* `segment` indica el segmento al que pertenece el cliente.

## Mantenimiento en producción

El plan gratuito de Render duerme la aplicación tras 15 minutos de inactividad. Para evitarlo, se configuró un cron job externo ([cron-job.org](https://cron-job.org)) que realiza una petición `GET` a la URL principal cada 14 minutos.

## Lógica de predicción

Toda la lógica de predicción se encuentra en:

```text
app/model/predictor.py
```

El proceso de inferencia sigue estos pasos:

```text
Datos del cliente
       │
       ▼
Validación de campos
       │
       ▼
Conversión de variables
       │
       ▼
Escalado
       │
       ▼
Segmentación con KMeans
       │
       ▼
Modelo de clasificación
       │
       ▼
Respuesta JSON
```

### GET `/retrain`

Endpoint preparado para demostrar el flujo completo de CI/CD: se mantiene comentado en `main` y se activa mediante un Pull Request desde una rama `feature/` durante la presentación, disparando un redespliegue en Render.

#### Ejemplo de respuesta

```json
{
  "status": "Éxito",
  "message": "Redespliegue en directo completado y modelo actualizado."
}
```

### Modelos utilizados

El proyecto utiliza tres archivos previamente entrenados:

| Archivo                    | Función                                                   |
| -------------------------- | --------------------------------------------------------- |
| `scaler_segmentacion.pkl`  | Escalado de las variables utilizadas para la segmentación |
| `kmeans_segmentacion.pkl`  | Asignación del segmento del cliente                       |
| `model_bank_marketing.pkl` | Predicción final de contratación                          |

---

## Despliegue en Render

La API puede desplegarse en **Render** utilizando **Gunicorn** como servidor de producción.

### Comando de inicio

```bash
gunicorn app.main:app
```

Una vez realizado el despliegue, Render proporcionará una URL pública desde la que se podrá acceder a la API.

---

## Autores

### Claudia

* GitHub: https://github.com/claudiafranzoni
* LinkedIn: https://www.linkedin.com/in/claudia-franzoni-800529196/

### Marta Harana Herrera

* GitHub: https://github.com/MHHsim
* LinkedIn: https://www.linkedin.com/in/marta-harana-herrera-004a84117/

### María Rodríguez Esteras

* GitHub: https://github.com/Mariasares
* LinkedIn: https://www.linkedin.com/in/mar%C3%ADa-rodes-8259403a1/

---

## Notas

Los modelos utilizados por la API:

```text
kmeans_segmentacion.pkl
model_bank_marketing.pkl
scaler_segmentacion.pkl
```

deben estar disponibles en:

```text
app/model/
```

Para que la API funcione correctamente, es necesario mantener la estructura de directorios esperada por `predictor.py`.

---