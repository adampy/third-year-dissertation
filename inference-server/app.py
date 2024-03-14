from flask import Flask, request
from enum import Enum
import azure_blob
import numpy as np
from keras.models import load_model

app = Flask(__name__)


class Model(Enum):
    auth = "auth"
    db = "db"
    image = "image"
    persistence = "persistence"
    recommender = "recommender"
    registry = "registry"
    webui = "webui"

MODELS = {
    Model.auth: {
        "name": "webui_lstm_model-w10.keras",
        "window": 10,
        "model": None
    },
    Model.db: {
        "name": "webui_lstm_model-w10.keras",
        "window": 10,
        "model": None
    },
    Model.image: {
        "name": "webui_lstm_model-w10.keras",
        "window": 10,
        "model": None
    },
    Model.persistence: {
        "name": "webui_lstm_model-w10.keras",
        "window": 10,
        "model": None
    },
    Model.recommender: {
        "name": "webui_lstm_model-w10.keras",
        "window": 10,
        "model": None
    },
    Model.registry: {
        "name": "webui_lstm_model-w10.keras",
        "window": 10,
        "model": None
    },
    Model.webui: {
        "name": "webui_lstm_model-w10.keras",
        "window": 10,
        "model": None
    }
}


@app.get("/")
def possible_models():
    return {
        "models": [model.value for model in Model]
    }

@app.post("/predict")
def model_predict():
    # Get request body
    data = request.get_json()
    model = data.get("model")
    window = data.get("window")
    
    if not model:
        return "Model not specified", 400
    if not window:
        return "Window not specified", 400
    if model not in [model.value for model in Model]:
        return "Model not found", 404
    
    model = Model(model)
    spec = MODELS[model]
    
    if len(window) != spec["window"]:
        return f"Window size for {model.value} should be {spec['window']}", 400
    
    # Now we need to obtain model if not obtained
    if not spec["model"]:
        azure_blob.load_blob_file(spec["name"])
        spec["model"] = load_model(spec["name"])
        
    # Now we have the model, we can use it to predict
    window = np.array(window)
    window = window.reshape(-1, 1, spec["window"])
    prediction = spec["model"].predict(window, verbose=0)[0][0]
    return {
        "prediction": float(prediction)
    }
    
    
if __name__ == "__main__":
    app.run(debug=True)