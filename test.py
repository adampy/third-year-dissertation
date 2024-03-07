import lookback
import azure_blob
from keras.models import load_model
import numpy as np

if __name__ == "__main__":
    total_cpu = [200]

    # Get ML model - all given metrics will be of the same pod, so we can just use the first one
    pod_name = "webui"
    model_name = "webui_lstm_model-w10.keras"
    azure_blob.load_blob_file(model_name) # Download model and store locally
    model = load_model(model_name) # Load from local
    
    # Perform inference
    newest_element = sum(total_cpu) / 1000
    lookback.append_window(pod_name, newest_element, 10)
    window = lookback.get_pod(pod_name)["lookback"]["data"]
    window = np.array(window)
    window = window.reshape(-1, 1, 10)

    prediction = model.predict(window, verbose=0)[0][0] # verbose=0 to suppress TF info from stdout - since we require that only the JSON is placed into this

    print(prediction)