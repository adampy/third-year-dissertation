from flask import Flask, request
from enum import Enum
import azure_blob
import numpy as np
from keras.models import load_model

app = Flask(__name__)


class Model(Enum):
    auth = "auth"
    image = "image"
    persistence = "persistence"
    recommender = "recommender"
    webui = "webui"

MODELS = {
    Model.auth: {
        "name": "auth_lstm_model-w15.keras",
        "window": 15,
        "model": None
    },
    Model.image: {
        "name": "image_lstm_model-w15.keras",
        "window": 15,
        "model": None
    },
    Model.persistence: {
        "name": "persistence_lstm_model-w15.keras",
        "window": 15,
        "model": None
    },
    Model.recommender: {
        "name": "recommender_lstm_model-w15.keras",
        "window": 15,
        "model": None
    },
    Model.webui: {
        "name": "webui_lstm_model-w15.keras",
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
    horizon = data.get("horizon", 1)
    
    # Parse args
    if not model:
        return "Model not specified", 400
    if not window:
        return "Window not specified", 400
    if model not in [model.value for model in Model]:
        return "Model not found", 404
    if horizon < 1:
        return "Horizon must be >= 1", 400
    
    # Get model and check window
    model = Model(model)
    spec = MODELS[model]
    
    if len(window) != spec["window"]:
        return f"Window size for {model.value} should be {spec['window']}", 400
    
    # Now we need to obtain model if not obtained
    if not spec["model"]:
        azure_blob.load_blob_file(spec["name"])
        spec["model"] = load_model(spec["name"])
        
    # Now we have the model, we can use it to predict
    horizon_values = []
    for i in range(horizon):
        np_window = np.array(window)
        np_window = np_window.reshape(-1, 1, spec["window"])
        prediction = float(spec["model"].predict(np_window, verbose=0)[0][0])
        # return {
        #     "prediction": prediction
        # }
        
        # Append to horizon values, and also the window
        horizon_values.append(prediction)
        window.append(prediction)
        window.pop(0)

    return {
        "horizon": horizon_values
    }
    
    
if __name__ == "__main__":
    app.run(debug=True)